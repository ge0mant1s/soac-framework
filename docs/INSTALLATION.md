
# Installation Guide

This guide provides detailed instructions for installing the SOaC Framework in different environments.

## Table of Contents

- [System Requirements](#system-requirements)
- [Pre-Installation Checklist](#pre-installation-checklist)
- [Installation Methods](#installation-methods)
  - [Docker Compose (Recommended)](#docker-compose-recommended)
  - [Manual Installation](#manual-installation)
  - [Kubernetes](#kubernetes)
  - [Cloud Platforms](#cloud-platforms)
- [Post-Installation](#post-installation)
- [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements (Development/Testing)
- **CPU**: 2 cores
- **RAM**: 4 GB
- **Disk**: 20 GB free space
- **OS**: Linux, macOS, or Windows (with WSL2)
- **Software**:
  - Docker 20.10+ and Docker Compose 2.0+
  - OR Python 3.11+ and Node.js 18+

### Recommended Requirements (Production)
- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Disk**: 50+ GB SSD
- **OS**: Linux (Ubuntu 22.04 LTS or RHEL 8+)
- **Software**:
  - Docker 24.0+ and Docker Compose 2.20+
  - OR Kubernetes 1.26+

### Network Requirements
- **Inbound Ports**:
  - 3000 (Frontend)
  - 8000 (Backend API)
- **Outbound Access**:
  - Internet access for device integrations
  - Access to security device APIs (Palo Alto, Entra ID, etc.)

---

## Pre-Installation Checklist

Before installing, ensure you have:

- [ ] System meets minimum requirements
- [ ] Docker and Docker Compose installed (for Docker installation)
- [ ] Python 3.11+ installed (for manual installation)
- [ ] Node.js 18+ and npm installed (for manual installation)
- [ ] PostgreSQL 14+ installed (for manual installation)
- [ ] Git installed
- [ ] Sufficient disk space (20 GB minimum)
- [ ] Network connectivity to security devices (if integrating)
- [ ] Admin/root access (for some installation methods)

---

## Installation Methods

### Docker Compose (Recommended)

Docker Compose is the easiest way to get started with SOaC Framework.

#### Step 1: Clone the Repository

```bash
git clone https://github.com/ge0mant1s/soac-framework.git
cd soac-framework
```

#### Step 2: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit environment variables
nano .env
```

**Minimum configuration:**
```env
# Database
DATABASE_URL=postgresql://soac_user:soac_password@postgres:5432/soac_db

# Backend
SECRET_KEY=your-secret-key-change-this-in-production-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development

# Frontend
VITE_API_BASE_URL=http://localhost:8000

# Optional: Enable mock mode for testing without real devices
MOCK_MODE=true
```

#### Step 3: Start the Application

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

#### Step 4: Verify Installation

Wait for all services to start (2-3 minutes). You should see:
```
frontend-1  | ➜  Local:   http://localhost:3000/
backend-1   | INFO: Application startup complete.
postgres-1  | database system is ready to accept connections
```

Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

**Default credentials:**
- Username: `admin`
- Password: `admin123`

#### Step 5: Stop the Application

```bash
# Stop services
docker-compose down

# Stop and remove volumes (complete reset)
docker-compose down -v
```

---

### Manual Installation

For development or when Docker is not available.

#### Step 1: Install Prerequisites

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip nodejs npm postgresql-14
```

**macOS (using Homebrew):**
```bash
brew install python@3.11 node postgresql@14
```

**Windows:**
- Install Python 3.11+ from python.org
- Install Node.js 18+ from nodejs.org
- Install PostgreSQL 14+ from postgresql.org

#### Step 2: Clone Repository

```bash
git clone https://github.com/ge0mant1s/soac-framework.git
cd soac-framework
```

#### Step 3: Setup PostgreSQL

```bash
# Start PostgreSQL
sudo systemctl start postgresql  # Linux
brew services start postgresql@14  # macOS

# Create database and user
sudo -u postgres psql
```

```sql
CREATE USER soac_user WITH PASSWORD 'soac_password';
CREATE DATABASE soac_db OWNER soac_user;
GRANT ALL PRIVILEGES ON DATABASE soac_db TO soac_user;
\q
```

#### Step 4: Setup Backend

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://soac_user:soac_password@localhost:5432/soac_db
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(64))")
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
MOCK_MODE=true
EOF

# Initialize database
python -m app.init_db

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend should now be running at http://localhost:8000

#### Step 5: Setup Frontend

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cat > .env << EOF
VITE_API_BASE_URL=http://localhost:8000
EOF

# Start development server
npm run dev
```

Frontend should now be running at http://localhost:3000

#### Step 6: Verify Installation

Visit http://localhost:3000 and login with:
- Username: `admin`
- Password: `admin123`

---

### Kubernetes

For production deployments with high availability.

#### Prerequisites

- Kubernetes cluster (1.26+)
- kubectl configured
- Helm 3+ (optional, for easier deployment)

#### Step 1: Clone Repository

```bash
git clone https://github.com/ge0mant1s/soac-framework.git
cd soac-framework/k8s
```

#### Step 2: Create Namespace

```bash
kubectl create namespace soac-framework
```

#### Step 3: Create Secrets

```bash
# Generate secret key
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(64))")

# Create Kubernetes secret
kubectl create secret generic soac-secrets \
  --from-literal=database-url="postgresql://soac_user:soac_password@postgres:5432/soac_db" \
  --from-literal=secret-key="$SECRET_KEY" \
  --from-literal=postgres-password="soac_password" \
  -n soac-framework
```

#### Step 4: Deploy PostgreSQL

```bash
kubectl apply -f postgres-statefulset.yaml -n soac-framework
kubectl apply -f postgres-service.yaml -n soac-framework

# Wait for PostgreSQL to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n soac-framework --timeout=300s
```

#### Step 5: Deploy Backend

```bash
kubectl apply -f backend-deployment.yaml -n soac-framework
kubectl apply -f backend-service.yaml -n soac-framework

# Wait for backend to be ready
kubectl wait --for=condition=ready pod -l app=backend -n soac-framework --timeout=300s
```

#### Step 6: Deploy Frontend

```bash
kubectl apply -f frontend-deployment.yaml -n soac-framework
kubectl apply -f frontend-service.yaml -n soac-framework

# Wait for frontend to be ready
kubectl wait --for=condition=ready pod -l app=frontend -n soac-framework --timeout=300s
```

#### Step 7: Setup Ingress (Optional)

```bash
# Install nginx ingress controller (if not already installed)
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# Deploy ingress
kubectl apply -f ingress.yaml -n soac-framework

# Get external IP
kubectl get ingress -n soac-framework
```

#### Step 8: Verify Deployment

```bash
# Check all pods are running
kubectl get pods -n soac-framework

# Check services
kubectl get services -n soac-framework

# View logs
kubectl logs -l app=backend -n soac-framework --tail=50
kubectl logs -l app=frontend -n soac-framework --tail=50
```

Access the application using the ingress hostname or port-forward:
```bash
kubectl port-forward -n soac-framework svc/frontend 3000:80
kubectl port-forward -n soac-framework svc/backend 8000:80
```

---

### Cloud Platforms

#### Railway.app (Free Tier)

1. **Fork the repository** on GitHub

2. **Sign up** at [railway.app](https://railway.app)

3. **Create new project** from GitHub repo

4. **Add PostgreSQL database**:
   - Click "+ New"
   - Select "Database" → "PostgreSQL"

5. **Configure environment variables**:
   
   **Backend service:**
   ```
   SECRET_KEY=<generate-random-64-char-string>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   ENVIRONMENT=production
   FRONTEND_URL=https://your-frontend-url.up.railway.app
   MOCK_MODE=true
   ```
   
   **Frontend service:**
   ```
   VITE_API_BASE_URL=https://your-backend-url.up.railway.app
   ```

6. **Deploy** - Railway automatically builds and deploys

**See:** [Railway Deployment Guide](../RAILWAY_DEPLOYMENT.md)

#### AWS

```bash
# Deploy using CloudFormation
cd scripts
./deploy-aws.sh
```

**See:** [AWS Deployment Guide](./deployment/AWS.md)

#### Azure

```bash
# Deploy using Azure CLI
cd scripts
./deploy-azure.sh
```

**See:** [Azure Deployment Guide](./deployment/AZURE.md)

---

## Post-Installation

### Change Default Passwords

**Important:** Change all default passwords immediately!

```bash
# Using the API
curl -X POST http://localhost:8000/api/v1/auth/change-password \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "old_password": "admin123",
    "new_password": "your-new-strong-password"
  }'
```

Or use the UI: Settings → Change Password

### Configure Device Integrations

1. Navigate to **Devices** page
2. Click **Add Device**
3. Select device type and enter credentials
4. Click **Test Connection** to verify
5. Click **Create**

**See:** [Device Integration Guide](./DEVICE_INTEGRATION.md)

### Import Operational Models

Operational models are pre-loaded by default. To add custom models:

1. Create DOCX file following the template
2. Upload to `/data/operational_models/`
3. Reload models via API or restart backend

**See:** [Operational Models Guide](./OPERATIONAL_MODELS.md)

### Setup Monitoring

Configure monitoring and alerting:

```bash
# For Prometheus/Grafana
kubectl apply -f k8s/monitoring/

# Access Grafana
kubectl port-forward -n monitoring svc/grafana 3001:80
```

**See:** [Monitoring Guide](./MONITORING.md)

---

## Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Check what's using the port
sudo lsof -i :3000
sudo lsof -i :8000
sudo lsof -i :5432

# Stop the process
sudo kill -9 <PID>
```

#### Docker Compose Fails to Start

```bash
# Check Docker daemon is running
sudo systemctl status docker

# Check logs
docker-compose logs

# Rebuild images
docker-compose build --no-cache
docker-compose up
```

#### Database Connection Error

```bash
# Check PostgreSQL is running
docker-compose ps

# Check database logs
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up
```

#### Frontend Can't Connect to Backend

1. Verify backend is running: `curl http://localhost:8000/health`
2. Check `VITE_API_BASE_URL` in frontend `.env`
3. Check browser console for CORS errors
4. Verify `FRONTEND_URL` in backend `.env`

#### Permission Denied Errors

```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or run with sudo
sudo docker-compose up
```

### Getting Help

If you encounter issues not covered here:

1. Check [Troubleshooting Guide](./TROUBLESHOOTING.md)
2. Search [GitHub Issues](https://github.com/ge0mant1s/soac-framework/issues)
3. Create a new issue with:
   - Installation method used
   - Operating system and version
   - Error messages and logs
   - Steps to reproduce

---

## Next Steps

After installation:

1. ✅ Change default passwords
2. ✅ Configure device integrations
3. ✅ Review operational models
4. ✅ Setup monitoring
5. ✅ Configure backups
6. ✅ Review security settings

**Continue to:**
- [Quick Start Guide](../QUICKSTART.md) - Learn the basics
- [Configuration Guide](./CONFIGURATION.md) - Advanced configuration
- [Device Integration](./DEVICE_INTEGRATION.md) - Connect security devices
- [User Guide](./USER_GUIDE.md) - Using the platform

---

*For production deployment best practices, see [Deployment Guide](./DEPLOYMENT.md)*
