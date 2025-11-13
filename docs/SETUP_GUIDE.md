# SOaC Framework - Complete Setup Guide

This guide provides step-by-step instructions for setting up the SOaC Framework in various environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Development Setup](#development-setup)
3. [Production Setup](#production-setup)
4. [Configuration](#configuration)
5. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Node.js**: Version 18.x or higher
- **npm**: Version 9.x or higher
- **RAM**: Minimum 4GB, Recommended 8GB
- **Disk Space**: 500MB free space

### Software Dependencies

```bash
# Check Node.js version
node --version  # Should be v18.0.0 or higher

# Check npm version
npm --version   # Should be 9.0.0 or higher

# Install Git (if not already installed)
# Ubuntu/Debian
sudo apt-get install git

# macOS (using Homebrew)
brew install git

# Windows
# Download from https://git-scm.com/download/win
```

## Development Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/ge0mant1s/soac-framework.git
cd soac-framework
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
npm install

# Copy environment configuration
cp .env.example .env

# (Optional) Edit .env file with your preferred settings
nano .env

# Start the backend server
npm start
```

**Expected Output:**
```
╔═══════════════════════════════════════════════════════════╗
║     SOaC Framework API Server - Phase 1                  ║
║     Security Operations as Code                           ║
╚═══════════════════════════════════════════════════════════╝

🚀 Server running on port 5000
🌍 Environment: development
📊 Health check: http://localhost:5000/health
📚 API Base URL: http://localhost:5000/api

⚠️  Using mock data for Phase 1 development
```

### Step 3: Frontend Setup

Open a **new terminal window** and run:

```bash
# Navigate to frontend directory from project root
cd soac-framework/frontend

# Install dependencies
npm install

# Copy environment configuration
cp .env.example .env

# Start the development server
npm start
```

**Expected Output:**
```
  VITE v5.0.8  ready in 1234 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

### Step 4: Access the Application

1. Open your browser to **http://localhost:3000**
2. You should see the login page
3. Use the default credentials:
   - **Username**: `admin`
   - **Password**: `admin123`

## Production Setup

### Step 1: Environment Configuration

**Backend (.env):**
```env
PORT=5000
NODE_ENV=production
JWT_SECRET=GENERATE_A_STRONG_RANDOM_SECRET_HERE
JWT_EXPIRES_IN=24h
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_secure_password
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100
CORS_ORIGIN=https://your-domain.com
```

**Frontend (.env):**
```env
VITE_API_BASE_URL=https://your-api-domain.com/api
VITE_APP_NAME=SOaC Framework
VITE_APP_VERSION=1.0.0
```

### Step 2: Build for Production

**Build Frontend:**
```bash
cd frontend
npm run build
```

This creates a `build` directory with optimized production files.

**Backend Production Mode:**
```bash
cd backend
NODE_ENV=production npm start
```

### Step 3: Deploy with PM2 (Recommended)

```bash
# Install PM2 globally
npm install -g pm2

# Start backend with PM2
cd backend
pm2 start src/server.js --name soac-backend

# Serve frontend with a static server
cd ../frontend
npm install -g serve
pm2 start serve --name soac-frontend -- -s build -l 3000

# Save PM2 configuration
pm2 save
pm2 startup
```

### Step 4: Set Up Reverse Proxy (Nginx)

```nginx
# /etc/nginx/sites-available/soac-framework

server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/soac-framework /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 5: SSL/TLS Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Configuration

### Backend Configuration

**JWT Secret Generation:**
```bash
node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"
```

**Environment Variables:**

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| PORT | Backend server port | 5000 | No |
| NODE_ENV | Environment mode | development | No |
| JWT_SECRET | JWT signing key | - | Yes |
| JWT_EXPIRES_IN | Token expiration | 24h | No |
| ADMIN_USERNAME | Admin username | admin | Yes |
| ADMIN_PASSWORD | Admin password | - | Yes |
| RATE_LIMIT_WINDOW_MS | Rate limit window | 900000 | No |
| RATE_LIMIT_MAX_REQUESTS | Max requests per window | 100 | No |
| CORS_ORIGIN | Allowed origins | * | No |

### Frontend Configuration

**Environment Variables:**

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| VITE_API_BASE_URL | Backend API URL | http://localhost:5000/api | Yes |
| VITE_APP_NAME | Application name | SOaC Framework | No |
| VITE_APP_VERSION | Application version | 1.0.0 | No |

### Database Configuration (Future Phases)

Phase 1 uses JSON files for data storage. Future phases will integrate:
- PostgreSQL for relational data
- MongoDB for document storage
- Redis for caching
- Elasticsearch for search

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Error:** `EADDRINUSE: address already in use :::5000`

**Solution:**
```bash
# Find process using port 5000
lsof -ti:5000

# Kill the process
kill -9 $(lsof -ti:5000)

# Or change port in .env file
PORT=5001
```

#### 2. Module Not Found

**Error:** `Cannot find module 'express'`

**Solution:**
```bash
# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall dependencies
npm install
```

#### 3. CORS Errors

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
```bash
# In backend .env file, set:
CORS_ORIGIN=http://localhost:3000

# Or for development, allow all origins:
CORS_ORIGIN=*
```

#### 4. JWT Verification Failed

**Error:** `Invalid token`

**Solution:**
```bash
# Clear localStorage in browser console:
localStorage.clear()

# Or generate a new JWT secret and restart backend
```

#### 5. Cannot Connect to API

**Error:** `Network Error` or `ERR_CONNECTION_REFUSED`

**Solution:**
1. Verify backend is running: `curl http://localhost:5000/health`
2. Check firewall settings
3. Verify VITE_API_BASE_URL in frontend .env

### Health Check

```bash
# Backend health check
curl http://localhost:5000/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-11-12T...",
  "version": "1.0.0",
  "service": "SOaC Framework API"
}
```

### Logs

**Backend Logs:**
```bash
# PM2 logs
pm2 logs soac-backend

# Direct logs (development)
npm start  # Logs will appear in console
```

**Frontend Logs:**
```bash
# Browser console (F12)
# PM2 logs
pm2 logs soac-frontend
```

## Performance Optimization

### Backend

1. **Enable Compression:**
   ```bash
   npm install compression
   ```
   Add to `server.js`:
   ```javascript
   const compression = require('compression');
   app.use(compression());
   ```

2. **Use Production Node:**
   ```bash
   NODE_ENV=production npm start
   ```

### Frontend

1. **Build Optimization:**
   ```bash
   npm run build
   ```

2. **Enable Caching:**
   Configure nginx with proper cache headers

3. **CDN Integration:**
   Serve static assets from CDN

## Monitoring

### PM2 Monitoring

```bash
# Monitor all processes
pm2 monit

# View process status
pm2 status

# View logs
pm2 logs
```

### Application Monitoring

Consider integrating:
- **New Relic** - Application performance monitoring
- **Sentry** - Error tracking
- **Prometheus + Grafana** - Metrics and visualization

## Backup and Recovery

### Data Backup

```bash
# Backup mock data
cp -r data/mock data/backup_$(date +%Y%m%d)

# Automated backup script
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf $BACKUP_DIR/soac_backup_$DATE.tar.gz data/mock
```

### Configuration Backup

```bash
# Backup environment files
cp backend/.env backend/.env.backup
cp frontend/.env frontend/.env.backup
```

## Security Hardening

1. **Change Default Credentials**
2. **Use Strong JWT Secrets**
3. **Enable HTTPS**
4. **Configure Firewall Rules**
5. **Regular Security Updates**
6. **Implement Rate Limiting**
7. **Enable Security Headers**
8. **Regular Backups**

## Next Steps

After successful setup:

1. ✅ Verify all endpoints are working
2. ✅ Change default credentials
3. ✅ Configure proper environment variables
4. ✅ Set up monitoring
5. ✅ Review security settings
6. ✅ Plan for Phase 2 integrations

## Support

For additional help:
- Check [API Reference](API_REFERENCE.md)
- Review [Architecture](ARCHITECTURE.md)
- Create an issue on GitHub
- Contact support@soacframework.local

---

**SOaC Framework Team © 2025**
