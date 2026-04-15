#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# jenkins-setup.sh  –  EC2 user_data bootstrap
# Installs: Java 21, Jenkins, Docker, Trivy, AWS CLI, kubectl
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

echo ">>> Updating packages"
apt-get update -y && apt-get upgrade -y

# ── Java 21 ──────────────────────────────────────────────────────────────────
echo ">>> Installing Java 21"
apt-get install -y fontconfig openjdk-21-jre

# ── Jenkins ───────────────────────────────────────────────────────────────────
echo ">>> Installing Jenkins"
wget -O /etc/apt/keyrings/jenkins-keyring.asc \
    https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] \
    https://pkg.jenkins.io/debian-stable binary/" \
    | tee /etc/apt/sources.list.d/jenkins.list > /dev/null
apt-get update -y
apt-get install -y jenkins
systemctl enable jenkins
systemctl start jenkins

# ── Docker ────────────────────────────────────────────────────────────────────
echo ">>> Installing Docker"
apt-get install -y docker.io
systemctl enable docker
systemctl start docker
usermod -aG docker jenkins
usermod -aG docker ubuntu
chmod 660 /var/run/docker.sock

# ── AWS CLI v2 ────────────────────────────────────────────────────────────────
echo ">>> Installing AWS CLI v2"
apt-get install -y unzip curl
curl -sSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o /tmp/awscliv2.zip
unzip -q /tmp/awscliv2.zip -d /tmp
/tmp/aws/install
rm -rf /tmp/awscliv2.zip /tmp/aws

# ── kubectl ───────────────────────────────────────────────────────────────────
echo ">>> Installing kubectl"
curl -sSL "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    -o /usr/local/bin/kubectl
chmod +x /usr/local/bin/kubectl

# ── Trivy ─────────────────────────────────────────────────────────────────────
echo ">>> Installing Trivy"
apt-get install -y wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key \
    | gpg --dearmor -o /usr/share/keyrings/trivy.gpg
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] \
    https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" \
    | tee /etc/apt/sources.list.d/trivy.list
apt-get update -y
apt-get install -y trivy
mkdir -p /var/lib/jenkins/.cache/trivy/db
chown -R jenkins:jenkins /var/lib/jenkins/.cache

# ── SonarQube (Docker container) ──────────────────────────────────────────────
echo ">>> Starting SonarQube container"
docker run -d \
    --name sonarqube \
    --restart unless-stopped \
    -p 9000:9000 \
    -v sonarqube_data:/opt/sonarqube/data \
    -v sonarqube_logs:/opt/sonarqube/logs \
    sonarqube:lts-community

# ── Prometheus (Docker container) ─────────────────────────────────────────────
echo ">>> Starting Prometheus container"
mkdir -p /opt/prometheus
cat > /opt/prometheus/prometheus.yml << 'PROM'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['localhost:9100']

  - job_name: 'jenkins'
    metrics_path: '/prometheus'
    static_configs:
      - targets: ['localhost:8080']
PROM

docker run -d \
    --name prometheus \
    --restart unless-stopped \
    -p 9090:9090 \
    -v /opt/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
    -v prometheus_data:/prometheus \
    prom/prometheus:latest \
    --config.file=/etc/prometheus/prometheus.yml \
    --storage.tsdb.path=/prometheus \
    --web.enable-lifecycle

# ── Node Exporter (system metrics for Prometheus) ─────────────────────────────
echo ">>> Starting Node Exporter"
docker run -d \
    --name node-exporter \
    --restart unless-stopped \
    -p 9100:9100 \
    --net="host" \
    --pid="host" \
    -v "/:/host:ro,rslave" \
    prom/node-exporter:latest \
    --path.rootfs=/host

# ── Grafana (Docker container) ────────────────────────────────────────────────
echo ">>> Starting Grafana container"
docker run -d \
    --name grafana \
    --restart unless-stopped \
    -p 3000:3000 \
    -v grafana_data:/var/lib/grafana \
    -e GF_SECURITY_ADMIN_PASSWORD=Admin@123 \
    -e GF_USERS_ALLOW_SIGN_UP=false \
    grafana/grafana:latest

echo ">>> Bootstrap complete. Jenkins, SonarQube, Prometheus, Grafana are starting."
echo ">>> Jenkins initial password:"
sleep 60
cat /var/lib/jenkins/secrets/initialAdminPassword || echo "Not ready yet – check in 2 mins"
