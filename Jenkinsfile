pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'SonarQubeServer'
        ECR_REPO         = '813270451126.dkr.ecr.ap-south-1.amazonaws.com/myrepo'
        AWS_REGION       = 'ap-south-1'
        IMAGE_NAME       = 'fastapi-app'
        PATH             = "/opt/sonar-scanner/bin:/usr/local/bin/terraform:$PATH"
        NOTIFY_EMAIL     = 'shankygcpdevops@gmail.com'
        TF_DIR           = 'terraform'
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 45, unit: 'MINUTES')
    }

    parameters {
        booleanParam(
            name:         'RUN_TERRAFORM',
            defaultValue: false,
            description:  'Apply Terraform changes? (only tick when infra has changed)'
        )
        booleanParam(
            name:         'TERRAFORM_DESTROY',
            defaultValue: false,
            description:  'DANGER: destroy all Terraform-managed infrastructure'
        )
    }

    stages {

        // ── 1. Pull source ────────────────────────────────────────────────
        stage('Pull Code From GitHub') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/shankysai/devopsproject170525.git'
            }
        }

        // ── 2. Terraform Init ─────────────────────────────────────────────
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

        // ── 3. Terraform Plan ─────────────────────────────────────────────
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

        // ── 4. Terraform Apply ────────────────────────────────────────────
        stage('Terraform Apply') {
            when { expression { params.RUN_TERRAFORM && !params.TERRAFORM_DESTROY } }
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',
                                  credentialsId: 'aws-creds']]) {
                    dir("${TF_DIR}") {
                        sh 'terraform apply -input=false -auto-approve tfplan'
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

        // ── 5. Terraform Destroy (manual confirm) ─────────────────────────
        stage('Terraform Destroy') {
            when { expression { params.TERRAFORM_DESTROY } }
            steps {
                input message: 'Are you SURE you want to destroy all infrastructure?', ok: 'Yes, destroy it'
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',
                                  credentialsId: 'aws-creds']]) {
                    dir("${TF_DIR}") {
                        sh 'terraform destroy -input=false -auto-approve'
                    }
                }
            }
        }

        // ── 6. Static code analysis ───────────────────────────────────────
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    sh 'sonar-scanner'
                }
            }
        }

        // ── 7. Quality Gate ───────────────────────────────────────────────
        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        // ── 8. Build Docker image ─────────────────────────────────────────
        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                        --build-arg BUILD_NUMBER=${BUILD_NUMBER} \
                        -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                        -t ${IMAGE_NAME}:latest \
                        .
                '''
            }
        }

        // ── 9. Trivy image security scan ──────────────────────────────────
        stage('Image Security Scan') {
            steps {
                sh '''
                    trivy image \
                        --exit-code 0 \
                        --severity HIGH,CRITICAL \
                        --format table \
                        ${IMAGE_NAME}:${BUILD_NUMBER} > trivy-report.txt
                    cat trivy-report.txt
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-report.txt', fingerprint: true
                }
            }
        }

        // ── 10. Push to AWS ECR ───────────────────────────────────────────
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

        // ── 11. Deploy to Kubernetes ──────────────────────────────────────
        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    sed "s|_IMAGE_|${ECR_REPO}:${BUILD_NUMBER}|g" pod.yaml > deploy-final.yaml
                    kubectl apply -f deploy-final.yaml
                    kubectl rollout status deployment/fastapi-deployment --timeout=120s
                '''
            }
        }

        // ── 12. Smoke test ────────────────────────────────────────────────
        stage('Smoke Test') {
            steps {
                sh '''
                    sleep 15
                    LB_HOST=$(kubectl get svc fastapi-svc \
                        -o jsonpath="{.status.loadBalancer.ingress[0].hostname}")
                    echo "Load balancer: $LB_HOST"
                    curl -sf http://${LB_HOST} | grep -q "Welcome" \
                        && echo "Smoke test PASSED" \
                        || (echo "Smoke test FAILED" && exit 1)
                '''
            }
        }

        // ── 13. Update Prometheus scrape target with live LB host ─────────
        stage('Update Prometheus Target') {
            steps {
                sh '''
                    LB_HOST=$(kubectl get svc fastapi-svc \
                        -o jsonpath="{.status.loadBalancer.ingress[0].hostname}")
                    sed -i "s|localhost:80|${LB_HOST}:80|g" /opt/prometheus/prometheus.yml
                    curl -sX POST http://localhost:9090/-/reload \
                        && echo "Prometheus config reloaded" \
                        || echo "Prometheus reload skipped"
                '''
            }
        }

    } // end stages

    post {
        success {
            mail to: "${NOTIFY_EMAIL}",
                 subject: "SUCCESS: ${env.JOB_NAME} [#${env.BUILD_NUMBER}]",
                 body: """\
Build #${env.BUILD_NUMBER} of ${env.JOB_NAME} completed successfully.

Image pushed  : ${ECR_REPO}:${env.BUILD_NUMBER}
Build URL     : ${env.BUILD_URL}
Duration      : ${currentBuild.durationString}

Monitoring:
  Prometheus  : http://<EC2-IP>:9090
  Grafana     : http://<EC2-IP>:3000  (admin / Admin@123)
"""
        }
        failure {
            mail to: "${NOTIFY_EMAIL}",
                 subject: "FAILURE: ${env.JOB_NAME} [#${env.BUILD_NUMBER}]",
                 body: """\
Build #${env.BUILD_NUMBER} of ${env.JOB_NAME} has FAILED.

Stage that failed : ${env.STAGE_NAME}
Build URL         : ${env.BUILD_URL}
Please check the console output for details.
"""
        }
        always {
            sh '''
                docker rmi ${IMAGE_NAME}:${BUILD_NUMBER} || true
                docker rmi ${IMAGE_NAME}:latest          || true
                docker rmi ${ECR_REPO}:${BUILD_NUMBER}   || true
            '''
        }
    }
}
