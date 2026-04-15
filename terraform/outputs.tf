# ─────────────────────────────────────────────────────────────────────────────
# outputs.tf
# ─────────────────────────────────────────────────────────────────────────────

output "jenkins_public_ip" {
  description = "Public IP of the Jenkins EC2 instance"
  value       = aws_eip.jenkins.public_ip
}

output "jenkins_url" {
  description = "Jenkins web UI URL"
  value       = "http://${aws_eip.jenkins.public_ip}:8080"
}

output "sonarqube_url" {
  description = "SonarQube URL (runs as Docker container on Jenkins EC2)"
  value       = "http://${aws_eip.jenkins.public_ip}:9000"
}

output "prometheus_url" {
  description = "Prometheus URL"
  value       = "http://${aws_eip.jenkins.public_ip}:9090"
}

output "grafana_url" {
  description = "Grafana URL (default login: admin / admin)"
  value       = "http://${aws_eip.jenkins.public_ip}:3000"
}

output "ecr_repo_url" {
  description = "ECR repository URL – use this in your Jenkinsfile ECR_REPO"
  value       = aws_ecr_repository.app.repository_url
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}
