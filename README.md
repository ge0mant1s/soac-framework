
# SOaC Framework - Phase 3A

**Security Operations as Code Framework**  
SOaC Framework Team © 2025

---

**🚀 Quick Deploy to Railway**: Deploy in 10 minutes with free hosting → **[Deployment Guide](./RAILWAY_DEPLOYMENT.md)**

---

## Overview

Phase 3A of the SOaC Framework adds **complete device integration and event ingestion** capabilities. This phase creates a full end-to-end security operations pipeline: Device → Events → Detection → Incidents → Response.

### Features

#### Phase 3A (Current) - Device Integration & Event Ingestion
- **🔌 Device Connectors**: Production-ready connectors for Palo Alto, Entra ID, and SIEM
- **📥 Event Ingestion Pipeline**: Background service for automatic event collection
- **🎭 Mock Mode**: Test with realistic mock data without real device credentials
- **⚡ Real-Time Processing**: Events automatically feed into detection engine
- **📊 Event Management**: Browse, filter, and analyze collected events
- **🔍 Event Normalization**: Standardize events from different sources
- **💚 Health Monitoring**: Track device health and connection status
- **📈 Event Statistics**: Analytics on event types, severity, and volume
- **🔄 Auto-Collection**: Configurable background polling (default: 5 minutes)
- **🎯 Manual Collection**: Trigger immediate event collection from UI

#### Phase 3B - Operational Models & Detection Engine
- **🚀 Operational Model Parser**: Parse DOCX operational models into structured detection patterns
- **🧠 Multi-Phase Detection Engine**: Detect complex attacks across multiple stages
- **🔗 Entity Correlation**: Track events by user, computer, IP across time windows
- **⚡ Real-Time Detection**: Process events in real-time with sub-second latency
- **📊 Incident Management**: Create, assign, and track security incidents
- **🤖 Playbook Execution**: Automated response actions based on decision matrix
- **📈 Confidence Scoring**: High/medium/low confidence based on matched phases
- **🎯 5 Pre-Built Models**: Data Theft, Fraud, Malware, DoS, and Intrusion detection

#### Phase 2A - Core Platform
- **Device Integration Management**: Configure and manage PaloAlto NGFW, Microsoft EntraID, and SIEM devices
- **Detection Rules**: Create, edit, and manage security detection rules with MITRE ATT&CK mapping
- **Real-time Dashboard**: Monitor device health, incidents, and playbook executions
- **JWT Authentication**: Secure authentication with role-based access control
- **REST API**: Comprehensive FastAPI backend with OpenAPI documentation

## Technology Stack

### Backend
- **FastAPI**: Modern, high-performance Python web framework
- **PostgreSQL**: Relational database for persistent storage
- **SQLAlchemy**: ORM for database operations
- **JWT**: Token-based authentication
- **Pydantic**: Data validation and settings management

### Frontend
- **React 18**: Modern UI library with hooks
- **TypeScript**: Type-safe JavaScript
- **Material-UI (MUI)**: Professional UI component library
- **Vite**: Fast build tool and dev server
- **Axios**: HTTP client for API requests

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Ports 3000, 8000, and 5432 available

### Installation

1. **Clone or navigate to the repository:**
   ```bash
   cd /home/ubuntu/code_artifacts/soac-framework
   ```

2. **Start the application:**
   ```bash
   docker-compose up --build
   ```

3. **Wait for initialization:**
   - PostgreSQL will start and create the database
   - Backend will initialize with sample data
   - Frontend will build and start

4. **Access the application:**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/api/docs

### Default Credentials

- **Admin User**: 
  - Username: `admin`
  - Password: `admin123`
  
- **Analyst User**:
  - Username: `analyst`
  - Password: `analyst123`

## Sample Data

The application comes pre-loaded with sample data for immediate testing:

### Devices (6 total)
- 2 PaloAlto NGFW devices
- 2 Microsoft EntraID tenants
- 2 SIEM instances (Elastic, Splunk)

### Detection Rules (8 total)
- 3 EntraID authentication rules
- 3 PaloAlto network rules
- 2 SIEM correlation rules

### Incidents (3 total)
- Intrusion chain incident
- Data exfiltration incident
- Ransomware incident

## Application Structure

```
soac-framework/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI application
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── auth.py            # Authentication utilities
│   │   ├── database.py        # Database configuration
│   │   ├── init_db.py         # Database initialization
│   │   ├── integrations/      # ✨ Device API clients (Phase 3A)
│   │   │   ├── paloalto_client.py
│   │   │   ├── entraid_client.py
│   │   │   └── siem_client.py
│   │   ├── services/          # ✨ Business logic (Phase 3A)
│   │   │   └── sync_service.py
│   │   └── routes/            # API endpoints
│   │       ├── auth_routes.py
│   │       ├── device_routes.py
│   │       ├── rule_routes.py
│   │       └── dashboard_routes.py
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile
│   └── entrypoint.sh
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   │   ├── Layout.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   ├── contexts/          # React contexts
│   │   │   └── AuthContext.tsx
│   │   ├── pages/             # Page components
│   │   │   ├── Login.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Devices.tsx
│   │   │   ├── DeviceHealth.tsx  # ✨ New (Phase 3A)
│   │   │   └── Rules.tsx
│   │   ├── services/          # API services
│   │   │   └── api.ts
│   │   ├── types/             # TypeScript types
│   │   │   └── index.ts
│   │   ├── App.tsx            # Main app component
│   │   └── main.tsx           # Entry point
│   ├── package.json           # Node dependencies
│   └── Dockerfile
│
├── docs/                       # Documentation
│   ├── DEVICE_INTEGRATION.md  # Device integration guide (Phase 3A)
│   └── OPERATIONAL_MODELS.md  # 🚀 Detection engine guide (Phase 3B)
│
└── docker-compose.yml         # Docker Compose configuration
```

## Phase 3B: Detection Engine Usage

### Operational Models

The framework includes 5 pre-built operational models:

1. **Data Theft/Exfiltration** - Detects data staging, network transfer, and cloud uploads
2. **Financial Fraud** - Detects account compromise, fraudulent transactions, and data exfil
3. **Malware Infection** - Detects delivery, execution, C2, and persistence
4. **Denial of Service** - Detects network floods, service degradation, and mitigation events
5. **Intrusion Detection** - Detects initial foothold, privilege abuse, and lateral movement

### Using the Detection Engine

#### 1. View Operational Models

Navigate to **Operational Models** page to:
- View all loaded models
- Inspect attack phases and detection logic
- Review response playbooks
- Check correlation patterns

#### 2. Process Security Events

The detection engine automatically processes events from integrated devices. You can also manually submit events:

```bash
curl -X POST http://localhost:8000/api/v1/detection/process-event \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "event": {
      "UserName": "john.doe@company.com",
      "ComputerName": "LAPTOP01",
      "FileName": "sensitive.zip",
      "TargetFileName": "/tmp/sensitive.zip"
    },
    "source": "falcon"
  }'
```

#### 3. View and Manage Incidents

Navigate to **Incidents** page to:
- View all detected incidents
- Filter by status, severity, or time range
- Assign incidents to analysts
- Update incident status
- Execute response playbooks
- View event timeline and details

#### 4. Execute Response Playbooks

Playbooks can be executed manually or automatically:

**Manual execution:**
```bash
curl -X POST http://localhost:8000/api/v1/incidents/INC-12345678/execute-playbook \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mode": "manual"}'
```

**Automated execution:**
Playbooks are automatically executed based on the decision matrix when incidents are created with high confidence.

### Creating Custom Operational Models

1. Create a DOCX file following the template structure (see `docs/OPERATIONAL_MODELS.md`)
2. Upload to `/home/ubuntu/Uploads/` directory
3. Reload models via API or UI:
   ```bash
   curl -X POST http://localhost:8000/api/v1/operational-models/reload \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

For detailed documentation, see: [docs/OPERATIONAL_MODELS.md](docs/OPERATIONAL_MODELS.md)

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout

### Devices
- `GET /api/v1/devices` - List all devices
- `POST /api/v1/devices` - Create device
- `GET /api/v1/devices/{id}` - Get device details
- `PUT /api/v1/devices/{id}` - Update device
- `DELETE /api/v1/devices/{id}` - Delete device
- `POST /api/v1/devices/{id}/test` - Test device connection (✨ real implementation in Phase 3A)
- `POST /api/v1/devices/{id}/sync` - ✨ Sync rules from device (Phase 3A)
- `GET /api/v1/devices/{id}/health` - ✨ Get device health metrics (Phase 3A)

### Rules
- `GET /api/v1/rules` - List all rules (with filters)
- `POST /api/v1/rules` - Create rule
- `GET /api/v1/rules/{id}` - Get rule details
- `PUT /api/v1/rules/{id}` - Update rule
- `DELETE /api/v1/rules/{id}` - Delete rule
- `PATCH /api/v1/rules/{id}/status` - Toggle rule status

### Dashboard
- `GET /api/v1/dashboard/metrics` - Get dashboard metrics
- `GET /api/v1/dashboard/device-health` - Get device health summary

## Phase 3A: Device Integration Features

### Real Device Integration

Phase 3A introduces production-ready API clients that enable real connectivity with security devices:

#### Supported Platforms

**1. Palo Alto Networks NGFW**
- PAN-OS REST API integration
- Security rule synchronization
- Threat log collection
- Device health monitoring
- [Detailed Setup Guide](./docs/DEVICE_INTEGRATION.md#palo-alto-networks-ngfw)

**2. Microsoft Entra ID (Azure AD)**
- OAuth 2.0 authentication
- Microsoft Graph API integration
- Sign-in log retrieval
- User and policy queries
- [Detailed Setup Guide](./docs/DEVICE_INTEGRATION.md#microsoft-entra-id-azure-ad)

**3. SIEM Platforms (Splunk/Elasticsearch)**
- Splunk REST API support
- Elasticsearch REST API support
- Event querying and search
- Index monitoring
- [Detailed Setup Guide](./docs/DEVICE_INTEGRATION.md#siem-splunk--elasticsearch)

### New UI Features

**Device Health Dashboard** (`/device-health`)
- Real-time connection status for all devices
- Health metrics summary (Connected, Error, Disconnected)
- Last tested and last sync timestamps
- Bulk refresh capability
- Quick connection testing

**Enhanced Device Management** (`/devices`)
- **Sync Now** button - Fetch rules from devices
- **Last Sync** column showing sync timestamps
- Real connection status indicators with colors
- Detailed error messages from connection tests
- Loading states for async operations

### Using Device Integration

#### 1. Configure a Device

Add your device credentials via the UI:
1. Navigate to **Devices** page
2. Click **Add Device**
3. Select device type and enter credentials
4. Click **Create**

#### 2. Test Connection

Verify connectivity:
- Click the **Test Connection** (🔌) button
- View detailed connection results
- Check for any configuration issues

#### 3. Sync Rules

Fetch rules from the device:
- Click the **Sync Now** (🔄) button
- Rules are automatically fetched and normalized
- View sync statistics (created/updated counts)

#### 4. Monitor Health

Track device status:
- Visit the **Device Health** dashboard
- View real-time connection status
- Monitor sync frequency and success rates

### Configuration

Device credentials can be configured via:
- **UI** (recommended): Devices page
- **Environment Variables**: See `backend/.env.example`
- **API**: POST to `/api/v1/devices`

For detailed device setup instructions, see [Device Integration Guide](./docs/DEVICE_INTEGRATION.md).

## Development

### Backend Development

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### Database Management

```bash
# Access PostgreSQL
docker-compose exec postgres psql -U soac_user -d soac_db

# Reset database
docker-compose down -v
docker-compose up --build
```

## Configuration

### Backend Configuration (.env)
```env
DATABASE_URL=postgresql://soac_user:soac_password@postgres:5432/soac_db
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

### Frontend Configuration (.env)
```env
VITE_API_BASE_URL=http://localhost:8000
```

## Troubleshooting

### Port Already in Use
```bash
# Check what's using the port
sudo lsof -i :3000
sudo lsof -i :8000
sudo lsof -i :5432

# Stop Docker containers
docker-compose down
```

### Database Connection Issues
```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Backend Not Starting
```bash
# Check backend logs
docker-compose logs backend

# Rebuild backend
docker-compose up --build backend
```

### Frontend Not Loading
```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose up --build frontend

# Clear node_modules
rm -rf frontend/node_modules
docker-compose up --build frontend
```

## Security Notes

⚠️ **Important Security Considerations:**

1. **Default Credentials**: Change default admin credentials in production
2. **Secret Key**: Use a strong, unique secret key in production
3. **Database Password**: Change database password in production
4. **CORS**: Configure CORS settings appropriately for production
5. **HTTPS**: Use HTTPS in production environments
6. **Credentials Storage**: Device credentials are stored in the database - consider using a secrets manager in production

## 🚂 Quick Deploy to Railway (Recommended)

**Deploy to Railway.app in under 10 minutes!** ⚡

Railway.app is a free cloud platform that provides:
- ✅ **$5 free credit monthly** (no credit card required)
- ✅ **Automatic HTTPS** and SSL certificates
- ✅ **PostgreSQL database** included
- ✅ **GitHub integration** for auto-deploy
- ✅ **No local Docker needed**

### Quick Deploy Steps

1. **Fork this repository** to your GitHub account

2. **Sign up for Railway**: [railway.app](https://railway.app)

3. **Deploy in 3 clicks**:
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `soac-framework` repository

4. **Add PostgreSQL database**:
   - In your Railway project, click "+ New"
   - Select "Database" → "PostgreSQL"
   - Railway auto-configures `DATABASE_URL`

5. **Configure environment variables**:
   
   **Backend Service**:
   ```env
   SECRET_KEY=<generate-a-random-64-char-string>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   ENVIRONMENT=production
   FRONTEND_URL=<your-frontend-railway-url>
   MOCK_MODE=true
   ```
   
   **Frontend Service**:
   ```env
   VITE_API_BASE_URL=<your-backend-railway-url>
   ```

6. **Generate domains** and access your application!

### 📚 Detailed Railway Deployment Guide

For step-by-step instructions with screenshots, troubleshooting, and advanced configuration:

**👉 See [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md)**

The guide includes:
- Complete setup walkthrough
- Environment variables reference
- Troubleshooting common issues
- Custom domain setup
- Auto-deploy from GitHub
- Cost management tips

### Railway Deployment Files

All necessary files for Railway deployment are included:
- ✅ `railway.json` / `railway.toml` - Railway configuration
- ✅ `backend/Dockerfile.railway` - Production-optimized backend
- ✅ `frontend/Dockerfile.railway` - Production-optimized frontend
- ✅ `backend/entrypoint.railway.sh` - Railway startup script
- ✅ `.env.production.example` - Environment variables template
- ✅ `deploy-to-railway.sh` - CLI deployment script
- ✅ `.github/workflows/railway-deploy.yml` - Auto-deploy workflow

### Default Login After Railway Deployment

- **Admin**: username: `admin`, password: `admin123`
- **Analyst**: username: `analyst`, password: `analyst123`

⚠️ **Change passwords immediately after first login!**

---

## Production Deployment (Other Platforms)

For deployment to AWS, Azure, GCP, or on-premises servers:

1. **Update environment variables** in `.env` files
2. **Use production-ready database** (managed PostgreSQL service)
3. **Enable HTTPS** with SSL certificates
4. **Set up proper logging** and monitoring
5. **Configure backup** strategy for database
6. **Use secrets management** (AWS Secrets Manager, Azure Key Vault, etc.)
7. **Build frontend for production**:
   ```bash
   cd frontend
   npm run build
   ```
8. **Use production WSGI server** (Gunicorn) for backend
9. **Set up reverse proxy** (nginx) for serving static files

**For detailed deployment guides, see [DEPLOYMENT.md](./DEPLOYMENT.md)**

## Support

For questions or issues, please contact the SOaC Framework Team.

## License

© 2025 SOaC Framework Team. All rights reserved.

---

**Note**: This is a development/testing environment. Please follow security best practices when deploying to production.

## Important Localhost Notice

**⚠️ This localhost refers to localhost of the computer that I'm using to run the application, not your local machine. To access it locally or remotely, you'll need to deploy the application on your own system.**

Follow the installation instructions above to deploy on your own machine or server.
