# 🚀 AWS DevOps CI/CD Pipeline — FastAPI on Kubernetes

<div align="center">

![Architecture](architecture.svg)

**A production-grade CI/CD pipeline built on AWS — Jenkins · Docker · SonarQube · Trivy · ECR · Kubernetes · Terraform · Prometheus · Grafana**

[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?style=flat-square&logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?style=flat-square&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=flat-square&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=flat-square&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![SonarQube](https://img.shields.io/badge/SonarQube-SAST-4E9BCD?style=flat-square&logo=sonarqube&logoColor=white)](https://www.sonarqube.org/)

**Target: 8–10 LPA DevOps Engineer Role**

</div>

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Pipeline Stages](#-pipeline-stages-13-stages)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Service URLs](#-service-urls)
- [Monitoring](#-monitoring)
- [Troubleshooting](#-troubleshooting)
- [Cleanup](#-cleanup)

---

## 🎯 Project Overview

This project demonstrates a **complete, production-grade CI/CD pipeline** running on AWS. A single EC2 instance (Ubuntu 22.04, t3.large) hosts Jenkins, Docker, SonarQube, Trivy, Prometheus, and Grafana. Every code push to GitHub automatically:

1. Scans code for bugs and security issues (SonarQube)
2. Builds a Docker image and scans it for CVEs (Trivy)
3. Pushes the image to AWS ECR
4. Deploys to a Kubernetes cluster via KOPS
5. Runs a smoke test to verify the app is live
6. Sends an email notification with results

Infrastructure is provisioned with **Terraform** (IaC). Metrics are collected by **Prometheus** and visualised on **Grafana** dashboards.

---

## 🏗 Architecture

```
Developer (Windows + PuTTY)
        │
        │  git push
        ▼
    GitHub Repo
        │
        │  webhook trigger
        ▼
┌─────────────────────────────────────────────────┐
│         EC2  Ubuntu 22.04  t3.large             │
│         ap-south-1 (Mumbai)                      │
│                                                  │
│  ┌─────────┐  ┌───────────┐  ┌───────────────┐  │
│  │ Jenkins │  │ SonarQube │  │     Trivy     │  │
│  │  :8080  │  │   :9000   │  │  Image Scan   │  │
│  └────┬────┘  └───────────┘  └───────────────┘  │
│       │                                          │
│  ┌────┴────┐  ┌───────────┐  ┌───────────────┐  │
│  │ Docker  │  │Prometheus │  │    Grafana    │  │
│  │  Build  │  │   :9090   │  │    :3000      │  │
│  └────┬────┘  └───────────┘  └───────────────┘  │
│       │                                          │
│  ┌────┴──────────────────────────────────────┐   │
│  │           TERRAFORM (IaC)                 │   │
│  │  VPC · Subnets · ECR · IAM · S3 · DynoDB  │   │
│  └───────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────┘
                     │
                     │  docker push :build_number
                     ▼
              ┌─────────────┐
              │  AWS ECR    │
              │  Registry   │
              └──────┬──────┘
                     │
                     │  kubectl apply
                     ▼
        ┌────────────────────────┐
        │   Kubernetes Cluster   │
        │        (KOPS)          │
        │                        │
        │  ┌──────────────────┐  │
        │  │   Deployment     │  │
        │  │  replicas: 2     │  │
        │  │  RollingUpdate   │  │
        │  └──────────────────┘  │
        │  ┌──────────────────┐  │
        │  │  LoadBalancer    │  │
        │  │  Service :80     │  │
        │  └──────────────────┘  │
        │  ┌──────────────────┐  │
        │  │  HPA: 2–6 pods   │  │
        │  │  CPU target: 60% │  │
        │  └──────────────────┘  │
        └────────────┬───────────┘
                     │
                     ▼
              🌐 End User
         http://LOAD-BALANCER-URL
```

---

## 🛠 Tech Stack

| Tool | Purpose | Port |
|------|---------|------|
| **Jenkins** | CI/CD orchestration — 13-stage pipeline | 8080 |
| **SonarQube** | Static code analysis (SAST) + Quality Gate | 9000 |
| **Docker** | Container build (multi-stage, non-root user) | — |
| **Trivy** | Docker image CVE scanning | — |
| **AWS ECR** | Private Docker image registry | — |
| **KOPS + K8s** | Kubernetes cluster on AWS EC2 | — |
| **Terraform** | Infrastructure as Code — provisions all AWS resources | — |
| **Prometheus** | Metrics collection (Jenkins + Node + App) | 9090 |
| **Grafana** | Dashboards + alerting | 3000 |
| **FastAPI** | Python web application | 80 |
| **GitHub Actions** | PR validation (Terraform fmt, Python lint, Dockerfile lint) | — |

---

## 📁 Project Structure

```
devops-fastapi-project/
│
├── 📄 Dockerfile                    # Multi-stage build, non-root user, HEALTHCHECK
├── 📄 Jenkinsfile                   # 13-stage declarative pipeline
├── 📄 main.py                       # FastAPI app with / and /health endpoints
├── 📄 form.html                     # Frontend welcome page
├── 📄 requirements.txt              # Pinned Python dependencies
├── 📄 sonar-project.properties      # SonarQube analysis config
├── 📄 README.md                     # This file
├── 📄 .gitignore                    # Excludes secrets, .pem, tfstate
│
├── 📁 kubernetes/
│   └── pod.yaml                     # Deployment + LoadBalancer Service + HPA
│
├── 📁 terraform/
│   ├── main.tf                      # VPC, EC2, ECR, IAM, S3, DynamoDB
│   ├── variables.tf                 # All input variables
│   ├── outputs.tf                   # Prints Jenkins URL, ECR URL after apply
│   ├── locals.tf                    # Shared resource tags
│   ├── terraform.tfvars.example     # Template — copy to terraform.tfvars
│   └── scripts/
│       └── jenkins-setup.sh         # EC2 bootstrap — installs all tools automatically
│
├── 📁 monitoring/
│   ├── prometheus.yml               # Scrape config (Jenkins, Node Exporter, App)
│   ├── alert.rules.yml              # Alerts: CPU>80%, Memory>85%, App Down
│   └── grafana-dashboard.json       # Import into Grafana UI
│
└── 📁 .github/
    └── workflows/
        └── validate.yml             # GitHub Actions: lint on every PR
```

---

## ⚙ Pipeline Stages (13 Stages)

```
GitHub Push
    │
    ├── Stage  1 ── Pull Code from GitHub
    ├── Stage  2 ── Terraform Init        ← only when RUN_TERRAFORM=true
    ├── Stage  3 ── Terraform Plan
    ├── Stage  4 ── Terraform Apply
    ├── Stage  5 ── Terraform Destroy     ← manual confirmation required
    ├── Stage  6 ── SonarQube Analysis    ← SAST scan
    ├── Stage  7 ── Quality Gate          ← BLOCKS pipeline if code quality fails
    ├── Stage  8 ── Build Docker Image    ← multi-stage, tagged :build_number
    ├── Stage  9 ── Trivy Image Scan      ← HIGH/CRITICAL CVE report archived
    ├── Stage 10 ── Push to AWS ECR       ← :build_number + :latest tags
    ├── Stage 11 ── Deploy to Kubernetes  ← kubectl apply + rollout status
    ├── Stage 12 ── Smoke Test            ← curl LoadBalancer URL
    └── Stage 13 ── Email Notification    ← Gmail SMTP success/failure
```

---

## ✅ Prerequisites

- AWS account with IAM user (ECR, EC2, VPC, S3, DynamoDB, IAM permissions)
- Windows laptop with PuTTY and Git Bash installed
- Gmail account with 2-Step Verification enabled (for App Password)
- GitHub account

---

## 🚀 Quick Start

### Step 1 — Launch EC2 on AWS

```
AWS Console → EC2 → Launch Instance
  Name:          greens-jenkins-server
  AMI:           Ubuntu 22.04 LTS
  Instance type: t3.large
  Key pair:      greens-devops-key (.ppk for PuTTY)
  Storage:       30 GB gp3
  Security group ports: 22, 8080, 9000, 9090, 3000, 80
```

### Step 2 — Connect via PuTTY

```
Host: ubuntu@YOUR-EC2-IP
Port: 22
Auth → Credentials: select greens-devops-key.ppk
```

### Step 3 — Install All Tools (run in PuTTY)

```bash
# Java + Jenkins
sudo apt update && sudo apt install fontconfig openjdk-21-jre -y
# (full commands in DevOps_Complete_Guide.docx — Phase 3)
```

### Step 4 — Push Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit - FastAPI DevOps project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/devops-fastapi-project.git
git push -u origin main
```

### Step 5 — Run Terraform

```bash
cd ~/devops-fastapi-project/terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
terraform init
terraform plan
terraform apply
```

### Step 6 — Create Kubernetes Cluster (KOPS)

```bash
kops create cluster \
  --name=greens.k8s.local \
  --state=s3://greens-kops-state \
  --zones=ap-south-1a \
  --node-count=2 \
  --node-size=t3.medium \
  --yes
```

### Step 7 — Trigger Pipeline

```
Jenkins → fastapi-cicd-pipeline → Build with Parameters → Build
```

---

## 🌐 Service URLs

| Service | URL | Login |
|---------|-----|-------|
| Jenkins | `http://EC2-IP:8080` | admin / your password |
| SonarQube | `http://EC2-IP:9000` | admin / your password |
| Prometheus | `http://EC2-IP:9090` | no login |
| Grafana | `http://EC2-IP:3000` | admin / Admin@123 |
| FastAPI App | `http://LOAD-BALANCER-URL` | public |
| App Health | `http://LOAD-BALANCER-URL/health` | returns `{"status":"healthy"}` |

---

## 📊 Monitoring

### Prometheus Scrape Targets

| Job | Target | Metrics |
|-----|--------|---------|
| `jenkins` | `localhost:8080/prometheus` | Build count, duration, queue |
| `node-exporter` | `localhost:9100` | CPU, Memory, Disk, Network |
| `fastapi-app` | `LOAD-BALANCER:80/metrics` | App health, request rate |

### Grafana Dashboards

- **Project Dashboard** — import `monitoring/grafana-dashboard.json`
- **Node Exporter Full** — import from Grafana marketplace, ID: `1860`

### Active Alerts

| Alert | Threshold | Severity |
|-------|-----------|----------|
| High CPU | > 80% for 2 min | Warning |
| High Memory | > 85% for 2 min | Warning |
| Low Disk | > 80% used | Critical |
| App Down | unreachable 1 min | Critical |
| Jenkins Down | unreachable 2 min | Critical |

---

## 🔧 Useful Commands

```bash
# Check all running containers
docker ps

# Restart a service
docker restart sonarqube
docker restart prometheus
docker restart grafana

# Check Kubernetes pods
kubectl get pods
kubectl get svc fastapi-svc
kubectl get hpa

# View pod logs
kubectl logs -l app=fastapi --tail=30

# Reload Prometheus config
curl -X POST http://localhost:9090/-/reload

# Clean Docker images
docker image prune -f
```

---

## 🔍 Troubleshooting

| Problem | Fix |
|---------|-----|
| `docker: permission denied` | `sudo usermod -aG docker jenkins && sudo systemctl restart jenkins` |
| `sonar-scanner: not found` | `source /etc/environment` — check PATH includes `/opt/sonar-scanner/bin` |
| Quality Gate hangs 5 min | SonarQube → Administration → Webhooks → Create → URL: `http://localhost:8080/sonarqube-webhook/` |
| ECR login failed | Check `aws-creds` credential in Jenkins has correct Access Key and Secret |
| `kubectl: no config` | `sudo chown -R jenkins:jenkins /var/lib/jenkins/.kube` |
| Trivy permission denied | `sudo chown -R jenkins:jenkins /var/lib/jenkins/.cache/trivy` |
| Grafana shows No data | Data source URL must be `http://localhost:9090` — click Save & Test |
| SonarQube not loading | Wait 2 min after docker start. Check: `docker logs sonarqube --tail=20` |

---

## 🧹 Cleanup (Avoid AWS Charges)

> ⚠️ Running cost is approximately ₹1,500–2,500/day. Always destroy resources after practice.

```bash
# Step 1 — Delete Kubernetes cluster
kops delete cluster \
  --name=greens.k8s.local \
  --state=s3://greens-kops-state \
  --yes

# Step 2 — Destroy Terraform resources
cd ~/devops-fastapi-project/terraform
terraform destroy

# Step 3 — Stop EC2
# AWS Console → EC2 → Instances → select → Instance state → Stop
```

---

## 📈 Key Improvements Over Basic Setup

| Feature | Basic Project | This Project |
|---------|--------------|--------------|
| Docker image | Single-stage | Multi-stage (smaller + secure) |
| Container user | root | Non-root `appuser` |
| Kubernetes | Raw pod | Deployment + HPA + Probes |
| Deploy strategy | Replace | RollingUpdate (zero downtime) |
| SonarQube | Analysis only | Quality Gate (blocks bad code) |
| Trivy | Console output | Archived as build artifact |
| Infrastructure | Manual ClickOps | Terraform IaC |
| Monitoring | None | Prometheus + Grafana + Alerts |
| Email | Basic | Rich with build details |
| Health check | None | `/health` endpoint + K8s probes |

---

<div align="center">

**Green's Technology — Velachery, Chennai**

*Built with ❤️ for DevOps learners targeting 8–10 LPA roles*

</div>
