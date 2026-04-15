# ─────────────────────────────────────────────────────────────────────────────
# locals.tf  –  shared tags applied to every resource
# ─────────────────────────────────────────────────────────────────────────────

locals {
  common_tags = {
    Project     = var.project_name
    Environment = "dev"
    ManagedBy   = "Terraform"
    Owner       = "greens-technology"
  }
}
