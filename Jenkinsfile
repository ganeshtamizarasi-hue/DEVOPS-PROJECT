pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'SonarQubeServer'
        ECR_REPO         = '145400477094.dkr.ecr.ap-south-1.amazonaws.com/ganesh-devops-repo'
        AWS_REGION       = 'ap-south-1'
        IMAGE_NAME       = 'fastapi-app'
        PATH             = "/opt/sonar-scanner/bin:/usr/local/bin/terraform:$PATH"
        NOTIFY_EMAIL     = 'ganeshtamizarasi@gmail.com'
        TF_DIR           = 'terraform'
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 45, unit: 'MINUTES')
    }

    parameters {
        booleanParam(name: 'RUN_TERRAFORM', defaultValue: false,
            description: 'Apply Terraform changes?')
        booleanParam(name: 'TERRAFORM_DESTROY', defaultValue: false,
            description: 'Destroy infrastructure')
    }

    stages {

        stage('Pull Code From GitHub') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/ganeshtamizarasi-hue/DEVOPS-PROJECT'
            }
        }

        stage('Terraform Init') {
            when { expression { params.RUN_TERRAFORM || params.TERRAFORM_DESTROY } }
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',
                                  credentialsId: 'aws-creds']]) {
                    dir("${TF_DIR}") {
                        sh '''
                            terraform init -input=false
                            terraform validate
                        '''
                    }
                }
            }
        }

        stage('Terraform Plan') {
            when { expression { params.RUN_TERRAFORM } }
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',
                                  credentialsId: 'aws-creds']]) {
                    dir("${TF_DIR}") {
                        sh 'terraform plan -input=false -out=tfplan'
                        archiveArtifacts artifacts: 'tfplan', fingerprint: true
                    }
                }
            }
        }

        stage('Terraform Apply') {
            when { expression { params.RUN_TERRAFORM && !params.TERRAFORM_DESTROY } }
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',
                                  credentialsId: 'aws-creds']]) {
                    dir("${TF_DIR}") {
                        sh 'terraform apply -auto-approve tfplan'
                        script {
                            env.ECR_REPO = sh(
                                script: 'terraform output -raw ecr_repo_url',
                                returnStdout: true
                            ).trim()
                        }
                    }
                }
            }
        }

        stage('Terraform Destroy') {
            when { expression { params.TERRAFORM_DESTROY } }
            steps {
                input message: 'Are you sure?', ok: 'Yes'
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',
                                  credentialsId: 'aws-creds']]) {
                    dir("${TF_DIR}") {
                        sh 'terraform destroy -auto-approve'
                    }
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    sh "sonar-scanner"
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh '''
                    trivy image --exit-code 0 --severity HIGH,CRITICAL \
                    ${IMAGE_NAME}:${BUILD_NUMBER} > trivy-report.txt
                    cat trivy-report.txt
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-report.txt'
                }
            }
        }

        stage('Push to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',
                                  credentialsId: 'aws-creds']]) {
                    sh '''
                        aws ecr get-login-password --region ${AWS_REGION} \
                        | docker login --username AWS --password-stdin ${ECR_REPO}

                        docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${ECR_REPO}:${BUILD_NUMBER}
                        docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${ECR_REPO}:latest

                        docker push ${ECR_REPO}:${BUILD_NUMBER}
                        docker push ${ECR_REPO}:latest
                    '''
                }
            }
        } 

        stage('Create ECR Secret') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',
                                  credentialsId: 'aws-creds']]) {
                    sh '''
                        kubectl delete secret ecr-secret --ignore-not-found=true
                        kubectl create secret docker-registry ecr-secret \
                            --docker-server=${ECR_REPO} \
                            --docker-username=AWS \
                            --docker-password=$(aws ecr get-login-password --region ${AWS_REGION})
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    sed "s|_IMAGE_|${ECR_REPO}:${BUILD_NUMBER}|g" \
                    kubernetes/pod.yaml > deploy-final.yaml

                    kubectl apply -f deploy-final.yaml
                    kubectl rollout status deployment/fastapi-deployment
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    sleep 30
                    LB=$(kubectl get svc fastapi-svc \
                    -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
                    curl -sf http://${LB}/health && echo "PASSED"
                '''
            }
        }

        stage('Update Prometheus Target') {
            steps {
                sh '''
                    LB=$(kubectl get svc fastapi-svc \
                    -o jsonpath="{.status.loadBalancer.ingress[0].hostname}")

                    sed -i "s|localhost:80|${LB}:80|g" /opt/prometheus/prometheus.yml
                    curl -X POST http://localhost:9090/-/reload
                '''
            }
        }
    }

    post {
        success {
            mail to: "${NOTIFY_EMAIL}",
                 subject: "SUCCESS: ${env.JOB_NAME}",
                 body: "Build success: ${env.BUILD_URL}"
        }
        failure {
            mail to: "${NOTIFY_EMAIL}",
                 subject: "FAILED: ${env.JOB_NAME}",
                 body: "Check logs: ${env.BUILD_URL}"
        }
        always {
            sh '''
                docker rmi ${IMAGE_NAME}:${BUILD_NUMBER} || true
                docker rmi ${IMAGE_NAME}:latest || true
                docker rmi ${ECR_REPO}:${BUILD_NUMBER} || true
            '''
        }
    }
}
