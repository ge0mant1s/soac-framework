#!/bin/bash

# SOaC Framework - Quick Start Script
# This script helps you get started with SOaC Framework

set -e

echo "=========================================="
echo "  SOaC Framework - Quick Start"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo "Creating .env file from .env.example..."
    
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ Created .env file${NC}"
        echo ""
        echo -e "${YELLOW}IMPORTANT: Please edit .env file and update the following:${NC}"
        echo "  - POSTGRES_PASSWORD"
        echo "  - REDIS_PASSWORD"
        echo "  - SECRET_KEY"
        echo "  - JWT_SECRET_KEY"
        echo "  - Platform API keys (if needed)"
        echo ""
        read -p "Press Enter after updating .env file..."
    else
        echo -e "${RED}Error: .env.example file not found${NC}"
        exit 1
    fi
fi

# Check if config.yaml exists
if [ ! -f config/config.yaml ]; then
    echo -e "${YELLOW}Warning: config/config.yaml not found${NC}"
    
    if [ -f config/config.example.yaml ]; then
        echo "Creating config.yaml from config.example.yaml..."
        cp config/config.example.yaml config/config.yaml
        echo -e "${GREEN}✓ Created config.yaml${NC}"
        echo ""
        echo -e "${YELLOW}Note: You can customize config.yaml later${NC}"
        echo ""
    fi
fi

# Stop any existing containers
echo "Stopping any existing SOaC containers..."
docker-compose down 2>/dev/null || docker compose down 2>/dev/null || true

# Pull latest images
echo ""
echo "Pulling required Docker images..."
docker-compose pull 2>/dev/null || docker compose pull 2>/dev/null

# Build custom images
echo ""
echo "Building SOaC Framework images..."
docker-compose build 2>/dev/null || docker compose build

# Start services
echo ""
echo "Starting SOaC Framework services..."
docker-compose up -d 2>/dev/null || docker compose up -d

# Wait for services to be healthy
echo ""
echo "Waiting for services to be ready..."
sleep 10

# Check service health
echo ""
echo "Checking service health..."

# Check PostgreSQL
if docker-compose ps postgres 2>/dev/null | grep -q "Up" || docker compose ps postgres 2>/dev/null | grep -q "Up"; then
    echo -e "${GREEN}✓ PostgreSQL is running${NC}"
else
    echo -e "${RED}✗ PostgreSQL failed to start${NC}"
fi

# Check Redis
if docker-compose ps redis 2>/dev/null | grep -q "Up" || docker compose ps redis 2>/dev/null | grep -q "Up"; then
    echo -e "${GREEN}✓ Redis is running${NC}"
else
    echo -e "${RED}✗ Redis failed to start${NC}"
fi

# Check API
if docker-compose ps api 2>/dev/null | grep -q "Up" || docker compose ps api 2>/dev/null | grep -q "Up"; then
    echo -e "${GREEN}✓ API Server is running${NC}"
else
    echo -e "${RED}✗ API Server failed to start${NC}"
fi

# Test API health endpoint
echo ""
echo "Testing API health endpoint..."
sleep 5

if curl -f http://localhost:5000/api/health &> /dev/null; then
    echo -e "${GREEN}✓ API is responding${NC}"
else
    echo -e "${YELLOW}⚠ API is not responding yet (may need more time to start)${NC}"
fi

# Display access information
echo ""
echo "=========================================="
echo -e "${GREEN}  SOaC Framework is running!${NC}"
echo "=========================================="
echo ""
echo "Access Information:"
echo "  • API Server: http://localhost:5000"
echo "  • API Health: http://localhost:5000/api/health"
echo "  • API Docs: http://localhost:5000/api/docs"
echo ""
echo "Useful Commands:"
echo "  • View logs: docker-compose logs -f"
echo "  • Stop services: docker-compose down"
echo "  • Restart services: docker-compose restart"
echo "  • View status: docker-compose ps"
echo ""
echo "Next Steps:"
echo "  1. Test the API: curl http://localhost:5000/api/health"
echo "  2. Create an incident: curl -X POST http://localhost:5000/api/incidents"
echo "  3. Read the documentation: cat docs/architecture/overview.md"
echo ""
echo "For more information, visit: https://github.com/ge0mant1s/soac-framework"
echo ""