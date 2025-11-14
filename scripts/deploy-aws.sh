
#!/bin/bash
# SOaC Framework - AWS Deployment Script
# This script deploys the SOaC Framework to AWS using Terraform

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
AWS_REGION="${AWS_REGION:-us-east-1}"
PROJECT_NAME="soac-framework"
TERRAFORM_DIR="terraform/aws"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}SOaC Framework - AWS Deployment${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v aws &> /dev/null; then
    echo -e "${RED}AWS CLI is not installed. Please install it first.${NC}"
    exit 1
fi

if ! command -v terraform &> /dev/null; then
    echo -e "${RED}Terraform is not installed. Please install it first.${NC}"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install it first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites met${NC}"
echo ""

# Check AWS credentials
echo -e "${YELLOW}Checking AWS credentials...${NC}"
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}AWS credentials not configured. Please run 'aws configure'${NC}"
    exit 1
fi

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo -e "${GREEN}✓ AWS Account: ${AWS_ACCOUNT_ID}${NC}"
echo ""

# Initialize Terraform
echo -e "${YELLOW}Initializing Terraform...${NC}"
cd $TERRAFORM_DIR
terraform init
echo -e "${GREEN}✓ Terraform initialized${NC}"
echo ""

# Plan Terraform deployment
echo -e "${YELLOW}Planning Terraform deployment...${NC}"
terraform plan -out=tfplan
echo ""

# Confirm deployment
read -p "$(echo -e ${YELLOW}Do you want to apply this plan? [y/N]:${NC} )" -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}Deployment cancelled${NC}"
    exit 1
fi

# Apply Terraform
echo -e "${YELLOW}Applying Terraform configuration...${NC}"
terraform apply tfplan
echo -e "${GREEN}✓ Infrastructure deployed${NC}"
echo ""

# Get outputs
ECR_BACKEND_URL=$(terraform output -raw ecr_backend_repository_url)
ECR_FRONTEND_URL=$(terraform output -raw ecr_frontend_repository_url)
ALB_DNS=$(terraform output -raw alb_dns_name)

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Backend ECR Repository: ${GREEN}${ECR_BACKEND_URL}${NC}"
echo -e "Frontend ECR Repository: ${GREEN}${ECR_FRONTEND_URL}${NC}"
echo -e "Application URL: ${GREEN}http://${ALB_DNS}${NC}"
echo ""

# Build and push Docker images
echo -e "${YELLOW}Do you want to build and push Docker images now? [y/N]:${NC}"
read -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Building and pushing Docker images...${NC}"
    
    # Login to ECR
    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
    
    # Build and push backend
    echo -e "${YELLOW}Building backend image...${NC}"
    cd ../../../backend
    docker build -t $ECR_BACKEND_URL:latest .
    docker push $ECR_BACKEND_URL:latest
    echo -e "${GREEN}✓ Backend image pushed${NC}"
    
    # Build and push frontend
    echo -e "${YELLOW}Building frontend image...${NC}"
    cd ../frontend
    docker build -t $ECR_FRONTEND_URL:latest .
    docker push $ECR_FRONTEND_URL:latest
    echo -e "${GREEN}✓ Frontend image pushed${NC}"
    
    echo ""
    echo -e "${GREEN}Docker images built and pushed successfully!${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Next Steps:${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "1. Wait for ECS services to start (5-10 minutes)"
echo "2. Access the application at: http://${ALB_DNS}"
echo "3. Default credentials: admin / admin123"
echo "4. Configure custom domain (optional)"
echo "5. Setup monitoring and alerts"
echo ""
echo -e "${YELLOW}For more information, see: docs/deployment/AWS.md${NC}"
echo ""
