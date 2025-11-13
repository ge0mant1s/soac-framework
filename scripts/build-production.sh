
#!/bin/bash

###############################################################################
# SOaC Framework - Production Build Script
# 
# This script builds the production version of the SOaC Framework,
# creating optimized frontend assets and preparing backend for deployment.
#
# Usage: ./scripts/build-production.sh
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
BUILD_DIR="$PROJECT_ROOT/build"

###############################################################################
# Helper Functions
###############################################################################

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

###############################################################################
# Build Functions
###############################################################################

check_environment() {
    print_header "Checking Environment"
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js first."
        exit 1
    fi
    print_success "Node.js: $(node --version)"
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm first."
        exit 1
    fi
    print_success "npm: $(npm --version)"
    
    # Check project structure
    if [ ! -d "$PROJECT_ROOT/backend" ] || [ ! -d "$PROJECT_ROOT/frontend" ]; then
        print_error "Project structure is invalid. Missing backend or frontend directory."
        exit 1
    fi
    print_success "Project structure verified"
}

clean_build() {
    print_header "Cleaning Previous Builds"
    
    # Remove old build directory
    if [ -d "$BUILD_DIR" ]; then
        print_info "Removing old build directory..."
        rm -rf "$BUILD_DIR"
        print_success "Old build removed"
    fi
    
    # Clean frontend dist
    if [ -d "$PROJECT_ROOT/frontend/dist" ]; then
        print_info "Cleaning frontend dist..."
        rm -rf "$PROJECT_ROOT/frontend/dist"
        print_success "Frontend dist cleaned"
    fi
    
    # Create new build directory
    mkdir -p "$BUILD_DIR"
    print_success "Build directory created"
}

check_env_files() {
    print_header "Checking Environment Files"
    
    # Check backend .env
    if [ ! -f "$PROJECT_ROOT/backend/.env" ]; then
        print_warning "Backend .env file not found. Creating from example..."
        cp "$PROJECT_ROOT/backend/.env.example" "$PROJECT_ROOT/backend/.env"
        print_warning "Please configure backend/.env for production!"
    else
        print_success "Backend .env found"
    fi
    
    # Check frontend .env
    if [ ! -f "$PROJECT_ROOT/frontend/.env" ]; then
        print_warning "Frontend .env file not found. Creating from example..."
        cp "$PROJECT_ROOT/frontend/.env.example" "$PROJECT_ROOT/frontend/.env"
        print_warning "Please configure frontend/.env for production!"
    else
        print_success "Frontend .env found"
    fi
    
    # Check for production settings
    print_info "\nVerifying production settings..."
    if grep -q "NODE_ENV=development" "$PROJECT_ROOT/backend/.env"; then
        print_warning "Backend is set to development mode!"
        print_warning "Remember to set NODE_ENV=production"
    fi
    
    if grep -q "localhost" "$PROJECT_ROOT/frontend/.env"; then
        print_warning "Frontend is pointing to localhost!"
        print_warning "Remember to set VITE_API_BASE_URL to production URL"
    fi
}

install_dependencies() {
    print_header "Installing Dependencies"
    
    # Backend dependencies
    print_info "Installing backend dependencies..."
    cd "$PROJECT_ROOT/backend"
    npm install --production
    print_success "Backend dependencies installed"
    
    # Frontend dependencies
    print_info "Installing frontend dependencies..."
    cd "$PROJECT_ROOT/frontend"
    npm install
    print_success "Frontend dependencies installed"
    
    cd "$PROJECT_ROOT"
}

build_frontend() {
    print_header "Building Frontend"
    
    cd "$PROJECT_ROOT/frontend"
    
    print_info "Running Vite build..."
    npm run build
    
    if [ ! -d "dist" ]; then
        print_error "Frontend build failed - dist directory not created"
        exit 1
    fi
    
    print_success "Frontend built successfully"
    
    # Show build stats
    print_info "\nBuild statistics:"
    du -sh dist
    echo ""
    ls -lh dist/
    
    cd "$PROJECT_ROOT"
}

prepare_backend() {
    print_header "Preparing Backend"
    
    print_info "Copying backend files to build directory..."
    
    # Create backend directory in build
    mkdir -p "$BUILD_DIR/backend"
    
    # Copy necessary files
    cp -r "$PROJECT_ROOT/backend/src" "$BUILD_DIR/backend/"
    cp "$PROJECT_ROOT/backend/package.json" "$BUILD_DIR/backend/"
    cp "$PROJECT_ROOT/backend/.env.example" "$BUILD_DIR/backend/"
    
    # Copy .env if it exists
    if [ -f "$PROJECT_ROOT/backend/.env" ]; then
        print_warning "Copying .env file - ensure sensitive data is secured!"
        cp "$PROJECT_ROOT/backend/.env" "$BUILD_DIR/backend/.env.production"
    fi
    
    print_success "Backend files prepared"
}

copy_frontend() {
    print_header "Copying Frontend Build"
    
    print_info "Copying frontend dist to build directory..."
    
    # Create frontend directory in build
    mkdir -p "$BUILD_DIR/frontend"
    
    # Copy built files
    cp -r "$PROJECT_ROOT/frontend/dist"/* "$BUILD_DIR/frontend/"
    
    print_success "Frontend files copied"
}

create_deployment_files() {
    print_header "Creating Deployment Files"
    
    # Create README for build
    cat > "$BUILD_DIR/README.md" << 'EOF'
# SOaC Framework - Production Build

This directory contains the production build of the SOaC Framework.

## Deployment Instructions

### Backend Deployment

1. Upload `backend/` directory to your server
2. Install dependencies: `npm install --production`
3. Configure `.env` file with production settings
4. Start server: `node src/server.js` or use PM2

### Frontend Deployment

1. Upload contents of `frontend/` directory to your web server root
2. Ensure `.htaccess` is configured for React Router (see docs)
3. Verify all assets are accessible

### Environment Configuration

#### Backend (.env)
- Set `NODE_ENV=production`
- Update `CORS_ORIGIN` to your production domain
- Change `JWT_SECRET` to a secure value
- Update admin credentials

#### Frontend
- Ensure `VITE_API_BASE_URL` points to production API
- Rebuild if environment changes: `npm run build`

## Support

For detailed deployment instructions, see:
- DEPLOYMENT.md
- docs/ONECOM_DEPLOYMENT.md
- docs/MAC_DEPLOYMENT.md

Repository: https://github.com/ge0mant1s/soac-framework
EOF
    
    print_success "README.md created in build directory"
    
    # Create .htaccess for frontend
    cat > "$BUILD_DIR/frontend/.htaccess" << 'EOF'
# SOaC Framework - Frontend .htaccess

RewriteEngine On

# If file or directory exists, serve it directly
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d

# Don't rewrite API requests
RewriteCond %{REQUEST_URI} !^/api/

# Redirect all other requests to index.html
RewriteRule . /index.html [L]

# Security Headers
<IfModule mod_headers.c>
    Header set X-Content-Type-Options "nosniff"
    Header set X-Frame-Options "SAMEORIGIN"
    Header set X-XSS-Protection "1; mode=block"
</IfModule>

# Enable compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
</IfModule>

# Browser caching
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
    ExpiresByType text/html "access plus 1 hour"
</IfModule>
EOF
    
    print_success ".htaccess created for frontend"
}

create_archive() {
    print_header "Creating Deployment Archive"
    
    cd "$PROJECT_ROOT"
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    ARCHIVE_NAME="soac-framework-production-$TIMESTAMP.tar.gz"
    
    print_info "Creating archive: $ARCHIVE_NAME"
    tar -czf "$ARCHIVE_NAME" -C "$BUILD_DIR" .
    
    if [ -f "$ARCHIVE_NAME" ]; then
        print_success "Archive created: $ARCHIVE_NAME"
        print_info "Archive size: $(du -h $ARCHIVE_NAME | cut -f1)"
    else
        print_error "Failed to create archive"
        exit 1
    fi
}

print_summary() {
    print_header "Build Summary"
    
    echo -e "${GREEN}Production build completed successfully! 🎉${NC}\n"
    
    echo -e "${BLUE}Build Location:${NC}"
    echo "   $BUILD_DIR"
    echo ""
    
    echo -e "${BLUE}Build Contents:${NC}"
    tree -L 2 "$BUILD_DIR" 2>/dev/null || ls -la "$BUILD_DIR"
    echo ""
    
    echo -e "${BLUE}Build Size:${NC}"
    du -sh "$BUILD_DIR"
    echo ""
    
    echo -e "${YELLOW}⚠ Important Next Steps:${NC}\n"
    
    echo "1. Review and update environment files:"
    echo "   - Set NODE_ENV=production in backend/.env"
    echo "   - Update CORS_ORIGIN to production domain"
    echo "   - Change JWT_SECRET"
    echo "   - Update admin credentials"
    echo "   - Set production API URL in frontend"
    echo ""
    
    echo "2. Test the build locally before deploying:"
    echo "   cd build/backend && npm install && node src/server.js"
    echo ""
    
    echo "3. Deploy to your hosting provider:"
    echo "   - See DEPLOYMENT.md for detailed instructions"
    echo "   - Backend: Upload build/backend/ directory"
    echo "   - Frontend: Upload build/frontend/ contents"
    echo ""
    
    echo "4. Verify deployment:"
    echo "   - Test API health: https://yourdomain.com/api/health"
    echo "   - Test frontend: https://yourdomain.com"
    echo "   - Test login functionality"
    echo ""
    
    echo -e "${BLUE}Documentation:${NC}"
    echo "   - $BUILD_DIR/README.md"
    echo "   - $PROJECT_ROOT/DEPLOYMENT.md"
    echo "   - $PROJECT_ROOT/docs/ONECOM_DEPLOYMENT.md"
    echo ""
}

###############################################################################
# Main Execution
###############################################################################

main() {
    clear
    
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║                                                       ║"
    echo "║        SOaC Framework - Production Build Script       ║"
    echo "║         Security Operations as Code - Phase 2         ║"
    echo "║                                                       ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo -e "${NC}\n"
    
    print_info "This script will build the production version of SOaC Framework."
    print_warning "Make sure to configure environment variables before deploying!\n"
    
    read -p "Press Enter to continue or Ctrl+C to cancel..."
    
    # Run build steps
    check_environment
    clean_build
    check_env_files
    install_dependencies
    build_frontend
    prepare_backend
    copy_frontend
    create_deployment_files
    create_archive
    
    # Print summary
    print_summary
}

# Run main function
main "$@"
