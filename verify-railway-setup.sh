#!/bin/bash

# ============================================
# SOaC Framework - Railway Setup Verification
# ============================================
# This script verifies that all Railway deployment
# files are present and properly configured.
#
# Usage: ./verify-railway-setup.sh
# ============================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0
WARNINGS=0

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
    ((PASSED++))
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    ((FAILED++))
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
    ((WARNINGS++))
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

check_file() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ]; then
        print_success "$description exists: $file"
        return 0
    else
        print_error "$description missing: $file"
        return 1
    fi
}

check_executable() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ] && [ -x "$file" ]; then
        print_success "$description is executable: $file"
        return 0
    elif [ -f "$file" ]; then
        print_warning "$description exists but not executable: $file"
        echo "         Run: chmod +x $file"
        return 1
    else
        print_error "$description missing: $file"
        return 1
    fi
}

check_file_content() {
    local file=$1
    local pattern=$2
    local description=$3
    
    if [ -f "$file" ]; then
        if grep -q "$pattern" "$file"; then
            print_success "$description configured in $file"
            return 0
        else
            print_warning "$description not found in $file"
            return 1
        fi
    else
        print_error "File $file not found"
        return 1
    fi
}

main() {
    clear
    print_header "SOaC Framework - Railway Setup Verification"
    
    # Check if we're in the right directory
    if [ ! -f "README.md" ]; then
        print_error "Not in SOaC Framework root directory!"
        echo "Please run this script from the root of the repository."
        exit 1
    fi
    
    print_info "Checking Railway deployment files..."
    echo ""
    
    # Check Railway configuration files
    print_header "Railway Configuration Files"
    check_file "railway.json" "Railway JSON config"
    check_file "railway.toml" "Railway TOML config"
    check_file ".env.production.example" "Production environment template"
    
    # Check backend files
    print_header "Backend Deployment Files"
    check_file "backend/Dockerfile.railway" "Backend Railway Dockerfile"
    check_file "backend/entrypoint.railway.sh" "Backend entrypoint script"
    check_executable "backend/entrypoint.railway.sh" "Backend entrypoint script"
    check_file "backend/requirements.txt" "Backend requirements"
    check_file "backend/app/config.py" "Backend configuration"
    check_file "backend/app/main.py" "Backend main application"
    check_file "backend/app/init_db.py" "Database initialization script"
    
    # Check frontend files
    print_header "Frontend Deployment Files"
    check_file "frontend/Dockerfile.railway" "Frontend Railway Dockerfile"
    check_file "frontend/nginx.conf" "Nginx configuration"
    check_file "frontend/package.json" "Frontend package.json"
    check_file "frontend/vite.config.ts" "Vite configuration"
    
    # Check documentation
    print_header "Documentation Files"
    check_file "RAILWAY_DEPLOYMENT.md" "Railway deployment guide"
    check_file "RAILWAY_CHECKLIST.md" "Railway deployment checklist"
    check_file "README.md" "Main README"
    check_file "DEPLOYMENT.md" "General deployment guide"
    
    # Check deployment scripts
    print_header "Deployment Scripts"
    check_executable "deploy-to-railway.sh" "Railway deployment script"
    
    # Check GitHub Actions
    print_header "GitHub Actions"
    check_file ".github/workflows/railway-deploy.yml" "Railway deploy workflow"
    
    # Check Docker configurations
    print_header "Docker Configurations"
    check_file_content "backend/Dockerfile.railway" "HEALTHCHECK" "Backend health check"
    check_file_content "frontend/Dockerfile.railway" "HEALTHCHECK" "Frontend health check"
    check_file_content "backend/Dockerfile.railway" "gunicorn" "Gunicorn server"
    check_file_content "frontend/Dockerfile.railway" "nginx" "Nginx server"
    
    # Check configuration
    print_header "Configuration Verification"
    check_file_content "backend/app/config.py" "cors_origins" "CORS configuration"
    check_file_content "backend/app/main.py" "health" "Health check endpoint"
    check_file_content "backend/entrypoint.railway.sh" "DATABASE_URL" "Database URL handling"
    
    # Check environment variables template
    print_header "Environment Variables Template"
    check_file_content ".env.production.example" "SECRET_KEY" "SECRET_KEY documented"
    check_file_content ".env.production.example" "DATABASE_URL" "DATABASE_URL documented"
    check_file_content ".env.production.example" "FRONTEND_URL" "FRONTEND_URL documented"
    check_file_content ".env.production.example" "VITE_API_BASE_URL" "VITE_API_BASE_URL documented"
    
    # Summary
    print_header "Verification Summary"
    echo ""
    echo -e "${GREEN}Passed:   $PASSED${NC}"
    echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
    echo -e "${RED}Failed:   $FAILED${NC}"
    echo ""
    
    if [ $FAILED -eq 0 ]; then
        print_success "All critical files present!"
        echo ""
        print_info "Your SOaC Framework is ready for Railway deployment!"
        echo ""
        echo "Next steps:"
        echo "  1. Review RAILWAY_DEPLOYMENT.md for deployment instructions"
        echo "  2. Fork/push this repository to your GitHub account"
        echo "  3. Create a Railway account at railway.app"
        echo "  4. Deploy using Railway UI or run: ./deploy-to-railway.sh"
        echo ""
        exit 0
    else
        print_error "Some critical files are missing!"
        echo ""
        print_info "Please ensure all required files are present before deploying."
        echo "See RAILWAY_DEPLOYMENT.md for details on required files."
        echo ""
        exit 1
    fi
}

# Run main function
main
