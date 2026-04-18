# ─────────────────────────────────────────────────────────────────────────────
# variables.tf
# ─────────────────────────────────────────────────────────────────────────────

variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Prefix used on all resource names and tags"
  type        = string
  default     = "ganesh-devops"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "instance_type" {
  description = "EC2 instance type for Jenkins server"
  type        = string
  default     = "t3.large"
}

variable "key_pair_name" {
  description = "Name of existing AWS key pair for EC2 SSH access"
  type        = string
}

variable "allowed_cidr" {
  description = "Your IP/CIDR allowed to reach Jenkins, SonarQube, Prometheus, Grafana ports"
  type        = string
  default     = "0.0.0.0/0"   # restrict to your IP in production
}
