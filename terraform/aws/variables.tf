
# AWS Region
variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

# Project name
variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "soac-framework"
}

# Environment
variable "environment" {
  description = "Environment (development, staging, production)"
  type        = string
  default     = "production"
}

# VPC Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

# RDS Configuration
variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

# ECS Backend Configuration
variable "backend_cpu" {
  description = "CPU units for backend container (256, 512, 1024, 2048, 4096)"
  type        = string
  default     = "512"
}

variable "backend_memory" {
  description = "Memory for backend container in MB (512, 1024, 2048, 4096, 8192)"
  type        = string
  default     = "1024"
}

variable "backend_desired_count" {
  description = "Desired number of backend tasks"
  type        = number
  default     = 2
}

variable "backend_min_count" {
  description = "Minimum number of backend tasks for auto-scaling"
  type        = number
  default     = 2
}

variable "backend_max_count" {
  description = "Maximum number of backend tasks for auto-scaling"
  type        = number
  default     = 4
}

# ECS Frontend Configuration
variable "frontend_cpu" {
  description = "CPU units for frontend container"
  type        = string
  default     = "256"
}

variable "frontend_memory" {
  description = "Memory for frontend container in MB"
  type        = string
  default     = "512"
}

variable "frontend_desired_count" {
  description = "Desired number of frontend tasks"
  type        = number
  default     = 2
}

# Domain Configuration
variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = ""
}

variable "certificate_arn" {
  description = "ARN of SSL certificate in ACM"
  type        = string
  default     = ""
}

# Tags
variable "tags" {
  description = "Additional tags for resources"
  type        = map(string)
  default     = {}
}
