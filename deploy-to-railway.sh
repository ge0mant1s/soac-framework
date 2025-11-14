#!/bin/bash

# ============================================
# SOaC Framework - Railway Deployment Script
# ============================================
# This script helps you deploy SOaC Framework to Railway.app
# using the Railway CLI tool.
#
# Usage:
#   ./deploy-to-railway.sh
#
# Prerequisites:
#   - Railway CLI installed
#   - Railway account
#   - Git repository initialized
# ============================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to generate random secret key
generate_secret() {
    if command_exists openssl; then
        openssl rand -hex 32
    elif command_exists python3; then
        python3 -c "import secrets; print(secrets.token_hex(32))"
    else
        # Fallback to reading from /dev/urandom
        cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1
    fi
}

# Main deployment script
main() {
    clear
    print_header "SOaC Framework - Railway Deployment Script"
    
    # Step 1: Check prerequisites
    print_info "Step 1: Checking prerequisites..."
    
    # Check if git is installed
    if ! command_exists git; then
        print_error "Git is not installed. Please install Git first."
        exit 1
    fi
    print_success "Git is installed"
    
    # Check if railway CLI is installed
    if ! command_exists railway; then
        print_warning "Railway CLI is not installed."
        echo ""
        print_info "Installing Railway CLI..."
        
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if command_exists brew; then
                brew install railway
            else
                print_error "Homebrew not found. Please install Railway CLI manually:"
                echo "  npm i -g @railway/cli"
                echo "  OR"
                echo "  Visit: https://docs.railway.app/develop/cli"
                exit 1
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            if command_exists npm; then
                npm i -g @railway/cli
            else
                print_error "npm not found. Please install Railway CLI manually:"
                echo "  npm i -g @railway/cli"
                echo "  OR"
                echo "  Visit: https://docs.railway.app/develop/cli"
                exit 1
            fi
        else
            print_error "Unsupported OS. Please install Railway CLI manually:"
            echo "  npm i -g @railway/cli"
            echo "  OR"
            echo "  Visit: https://docs.railway.app/develop/cli"
            exit 1
        fi
        
        if command_exists railway; then
            print_success "Railway CLI installed successfully"
        else
            print_error "Railway CLI installation failed. Please install manually."
            exit 1
        fi
    else
        print_success "Railway CLI is installed"
    fi
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a git repository. Please initialize git first:"
        echo "  git init"
        echo "  git add ."
        echo "  git commit -m 'Initial commit'"
        exit 1
    fi
    print_success "Git repository detected"
    
    # Step 2: Login to Railway
    print_header "Step 2: Railway Authentication"
    
    print_info "Checking Railway authentication..."
    if railway whoami > /dev/null 2>&1; then
        print_success "Already logged in to Railway"
        RAILWAY_USER=$(railway whoami)
        print_info "Logged in as: $RAILWAY_USER"
    else
        print_info "Please login to Railway..."
        railway login
        
        if railway whoami > /dev/null 2>&1; then
            print_success "Successfully logged in to Railway"
        else
            print_error "Railway login failed. Please try again."
            exit 1
        fi
    fi
    
    # Step 3: Initialize Railway project
    print_header "Step 3: Initialize Railway Project"
    
    print_info "Creating new Railway project..."
    echo ""
    print_warning "Please choose a name for your project (or press Enter for default):"
    read -p "Project name: " PROJECT_NAME
    
    if [ -z "$PROJECT_NAME" ]; then
        PROJECT_NAME="soac-framework"
    fi
    
    railway init --name "$PROJECT_NAME"
    
    if [ $? -eq 0 ]; then
        print_success "Railway project created: $PROJECT_NAME"
    else
        print_error "Failed to create Railway project"
        exit 1
    fi
    
    # Step 4: Add PostgreSQL database
    print_header "Step 4: Add PostgreSQL Database"
    
    print_info "Adding PostgreSQL database to project..."
    railway add --database postgresql
    
    if [ $? -eq 0 ]; then
        print_success "PostgreSQL database added successfully"
    else
        print_warning "Failed to add database. You can add it manually in Railway dashboard."
    fi
    
    # Step 5: Generate and set environment variables
    print_header "Step 5: Configure Environment Variables"
    
    print_info "Generating secure SECRET_KEY..."
    SECRET_KEY=$(generate_secret)
    print_success "SECRET_KEY generated"
    
    print_info "Setting backend environment variables..."
    
    # Set environment variables
    railway variables set SECRET_KEY="$SECRET_KEY"
    railway variables set ALGORITHM="HS256"
    railway variables set ACCESS_TOKEN_EXPIRE_MINUTES="1440"
    railway variables set ENVIRONMENT="production"
    railway variables set MOCK_MODE="true"
    railway variables set ENABLE_BACKGROUND_COLLECTION="true"
    railway variables set EVENT_COLLECTION_INTERVAL="300"
    
    print_success "Environment variables set"
    
    # Step 6: Create services
    print_header "Step 6: Create Backend and Frontend Services"
    
    print_info "Creating backend service..."
    print_warning "You'll need to manually configure services in Railway dashboard:"
    echo ""
    echo "  1. Go to your Railway project dashboard"
    echo "  2. Click '+ New Service'"
    echo "  3. Select 'GitHub Repo' and connect your repository"
    echo ""
    echo "  For Backend Service:"
    echo "    - Root Directory: backend"
    echo "    - Dockerfile Path: Dockerfile.railway"
    echo ""
    echo "  For Frontend Service:"
    echo "    - Root Directory: frontend"
    echo "    - Dockerfile Path: Dockerfile.railway"
    echo ""
    
    # Step 7: Deploy
    print_header "Step 7: Deploy to Railway"
    
    print_info "Ready to deploy?"
    read -p "Press Enter to deploy, or Ctrl+C to cancel..."
    
    print_info "Deploying to Railway..."
    railway up
    
    if [ $? -eq 0 ]; then
        print_success "Deployment initiated successfully!"
    else
        print_error "Deployment failed. Check Railway dashboard for details."
        exit 1
    fi
    
    # Step 8: Get deployment URLs
    print_header "Step 8: Deployment Complete!"
    
    print_success "SOaC Framework is deploying to Railway!"
    echo ""
    print_info "Next steps:"
    echo ""
    echo "  1. Open Railway dashboard:"
    echo "     railway open"
    echo ""
    echo "  2. Wait for deployment to complete (2-5 minutes)"
    echo ""
    echo "  3. Generate domains for both services:"
    echo "     - Go to each service → Settings → Networking → Generate Domain"
    echo ""
    echo "  4. Update environment variables with generated URLs:"
    echo "     Backend:"
    echo "       FRONTEND_URL=https://your-frontend-url.railway.app"
    echo ""
    echo "     Frontend:"
    echo "       VITE_API_BASE_URL=https://your-backend-url.railway.app"
    echo ""
    echo "  5. Access your application:"
    echo "     - Frontend: https://your-frontend-url.railway.app"
    echo "     - Backend API: https://your-backend-url.railway.app/docs"
    echo ""
    echo "  6. Login with default credentials:"
    echo "     - Username: admin"
    echo "     - Password: admin123"
    echo "     ⚠️  Change password after first login!"
    echo ""
    
    print_info "Useful commands:"
    echo "  railway open         - Open Railway dashboard"
    echo "  railway logs         - View deployment logs"
    echo "  railway status       - Check deployment status"
    echo "  railway variables    - View environment variables"
    echo "  railway up           - Deploy again"
    echo ""
    
    print_success "Deployment complete! 🎉"
    echo ""
    print_info "For detailed documentation, see: RAILWAY_DEPLOYMENT.md"
    echo ""
}

# Run main function
main
