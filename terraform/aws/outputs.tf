
# Outputs for AWS deployment

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.main.dns_name
}

output "alb_url" {
  description = "URL of the Application Load Balancer"
  value       = "http://${aws_lb.main.dns_name}"
}

output "rds_endpoint" {
  description = "Endpoint of the RDS instance"
  value       = aws_db_instance.postgresql.endpoint
  sensitive   = true
}

output "rds_database_name" {
  description = "Name of the RDS database"
  value       = aws_db_instance.postgresql.db_name
}

output "ecr_backend_repository_url" {
  description = "URL of the backend ECR repository"
  value       = aws_ecr_repository.backend.repository_url
}

output "ecr_frontend_repository_url" {
  description = "URL of the frontend ECR repository"
  value       = aws_ecr_repository.frontend.repository_url
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.main.name
}

output "ecs_backend_service_name" {
  description = "Name of the backend ECS service"
  value       = aws_ecs_service.backend.name
}

output "ecs_frontend_service_name" {
  description = "Name of the frontend ECS service"
  value       = aws_ecs_service.frontend.name
}

output "secrets_manager_secret_arn" {
  description = "ARN of the Secrets Manager secret"
  value       = aws_secretsmanager_secret.db_credentials.arn
}

output "cloudwatch_log_group_backend" {
  description = "CloudWatch log group for backend"
  value       = aws_cloudwatch_log_group.backend.name
}

output "cloudwatch_log_group_frontend" {
  description = "CloudWatch log group for frontend"
  value       = aws_cloudwatch_log_group.frontend.name
}

output "deployment_instructions" {
  description = "Instructions for deploying the application"
  value       = <<-EOT
    SOaC Framework deployed successfully!
    
    Access the application at: http://${aws_lb.main.dns_name}
    
    Next steps:
    1. Push Docker images to ECR:
       - Backend: ${aws_ecr_repository.backend.repository_url}
       - Frontend: ${aws_ecr_repository.frontend.repository_url}
    
    2. Update ECS services to use the new images
    
    3. Configure Route53 DNS (if using custom domain)
    
    4. Access the database credentials from Secrets Manager:
       aws secretsmanager get-secret-value --secret-id ${aws_secretsmanager_secret.db_credentials.name}
    
    5. Monitor logs in CloudWatch:
       - Backend: ${aws_cloudwatch_log_group.backend.name}
       - Frontend: ${aws_cloudwatch_log_group.frontend.name}
  EOT
}
