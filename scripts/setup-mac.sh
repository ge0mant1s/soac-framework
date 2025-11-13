
#!/bin/bash

###############################################################################
# SOaC Framework - Mac Setup Script
# 
# This script automates the setup of the SOaC Framework on macOS.
# It checks prerequisites, installs dependencies, and configures the
# development environment.
#
# Usage: ./scripts/setup-mac.sh
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

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

###############################################################################
# Main Setup Functions
###############################################################################

check_macos() {
    print_header "Checking macOS Version"
    
    if [[ "$OSTYPE" != "darwin"* ]]; then
        print_error "This script is designed for macOS only."
        exit 1
    fi
    
    macos_version=$(sw_vers -productVersion)
    print_success "macOS version: $macos_version"
}

check_homebrew() {
    print_header "Checking Homebrew"
    
    if command_exists brew; then
        brew_version=$(brew --version | head -n1)
        print_success "Homebrew installed: $brew_version"
        print_info "Updating Homebrew..."
        brew update || print_warning "Homebrew update failed, continuing..."
    else
        print_warning "Homebrew not found. Installing..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add Homebrew to PATH for Apple Silicon
        if [[ $(uname -m) == "arm64" ]]; then
            echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/opt/homebrew/bin/brew shellenv)"
        fi
        
        print_success "Homebrew installed successfully"
    fi
}

check_node() {
    print_header "Checking Node.js"
    
    if command_exists node; then
        node_version=$(node --version)
        required_version="v18"
        
        if [[ "$node_version" == "$required_version"* ]] || [[ "$node_version" > "$required_version" ]]; then
            print_success "Node.js installed: $node_version"
            print_success "npm version: $(npm --version)"
        else
            print_warning "Node.js version $node_version is too old. Upgrading to LTS..."
            brew upgrade node
        fi
    else
        print_warning "Node.js not found. Installing..."
        brew install node
        print_success "Node.js installed: $(node --version)"
        print_success "npm version: $(npm --version)"
    fi
}

check_git() {
    print_header "Checking Git"
    
    if command_exists git; then
        git_version=$(git --version)
        print_success "$git_version"
    else
        print_warning "Git not found. Installing..."
        brew install git
        print_success "Git installed: $(git --version)"
    fi
}

setup_backend() {
    print_header "Setting Up Backend"
    
    cd "$PROJECT_ROOT/backend"
    
    print_info "Installing backend dependencies..."
    npm install
    print_success "Backend dependencies installed"
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        print_info "Creating backend .env file..."
        cp .env.example .env
        print_success "Backend .env file created"
        print_warning "Please edit backend/.env with your configuration"
    else
        print_info "Backend .env file already exists"
    fi
    
    cd "$PROJECT_ROOT"
}

setup_frontend() {
    print_header "Setting Up Frontend"
    
    cd "$PROJECT_ROOT/frontend"
    
    print_info "Installing frontend dependencies..."
    npm install
    print_success "Frontend dependencies installed"
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        print_info "Creating frontend .env file..."
        cp .env.example .env
        print_success "Frontend .env file created"
    else
        print_info "Frontend .env file already exists"
    fi
    
    cd "$PROJECT_ROOT"
}

verify_installation() {
    print_header "Verifying Installation"
    
    print_info "Checking backend structure..."
    if [ -d "$PROJECT_ROOT/backend/node_modules" ]; then
        print_success "Backend node_modules found"
    else
        print_error "Backend node_modules missing"
    fi
    
    if [ -f "$PROJECT_ROOT/backend/.env" ]; then
        print_success "Backend .env found"
    else
        print_error "Backend .env missing"
    fi
    
    print_info "Checking frontend structure..."
    if [ -d "$PROJECT_ROOT/frontend/node_modules" ]; then
        print_success "Frontend node_modules found"
    else
        print_error "Frontend node_modules missing"
    fi
    
    if [ -f "$PROJECT_ROOT/frontend/.env" ]; then
        print_success "Frontend .env found"
    else
        print_error "Frontend .env missing"
    fi
}

print_next_steps() {
    print_header "Setup Complete! 🎉"
    
    echo -e "${GREEN}The SOaC Framework has been set up successfully!${NC}\n"
    
    echo -e "${BLUE}Next Steps:${NC}\n"
    
    echo "1. Configure environment variables:"
    echo -e "   ${YELLOW}nano backend/.env${NC}"
    echo -e "   ${YELLOW}nano frontend/.env${NC}\n"
    
    echo "2. Start the backend (in one terminal):"
    echo -e "   ${YELLOW}cd backend${NC}"
    echo -e "   ${YELLOW}npm run dev${NC}\n"
    
    echo "3. Start the frontend (in another terminal):"
    echo -e "   ${YELLOW}cd frontend${NC}"
    echo -e "   ${YELLOW}npm run dev${NC}\n"
    
    echo "4. Access the application:"
    echo -e "   ${YELLOW}Frontend: http://localhost:3000${NC}"
    echo -e "   ${YELLOW}Backend: http://localhost:5000/api${NC}\n"
    
    echo "5. Login with default credentials:"
    echo -e "   ${YELLOW}Username: admin${NC}"
    echo -e "   ${YELLOW}Password: admin123${NC}"
    echo -e "   ${RED}⚠ Change these in production!${NC}\n"
    
    echo -e "${BLUE}Documentation:${NC}"
    echo "   - DEPLOYMENT.md - Complete deployment guide"
    echo "   - docs/MAC_DEPLOYMENT.md - Detailed Mac setup guide"
    echo "   - README.md - Project overview\n"
    
    echo -e "${BLUE}Need help?${NC}"
    echo "   - GitHub: https://github.com/ge0mant1s/soac-framework"
    echo "   - Issues: https://github.com/ge0mant1s/soac-framework/issues\n"
}

###############################################################################
# Main Execution
###############################################################################

main() {
    clear
    
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║                                                       ║"
    echo "║           SOaC Framework - Mac Setup Script          ║"
    echo "║         Security Operations as Code - Phase 2         ║"
    echo "║                                                       ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo -e "${NC}\n"
    
    print_info "This script will set up the SOaC Framework on your Mac."
    print_info "It will check prerequisites and install dependencies.\n"
    
    read -p "Press Enter to continue or Ctrl+C to cancel..."
    
    # Check system
    check_macos
    
    # Check and install prerequisites
    check_homebrew
    check_node
    check_git
    
    # Setup project
    setup_backend
    setup_frontend
    
    # Verify
    verify_installation
    
    # Print next steps
    print_next_steps
}

# Run main function
main "$@"
