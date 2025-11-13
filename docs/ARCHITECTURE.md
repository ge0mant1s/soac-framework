# SOaC Framework - Architecture Documentation

## Overview

The SOaC (Security Operations as Code) Framework is built on a modern, scalable architecture designed for security operations management, threat detection, and incident response.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                             │
│                     (React Application)                          │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Frontend Layer                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │Dashboard │  │ Devices  │  │  Rules   │  │  Alerts  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐        │
│  │          Authentication Context                     │        │
│  │          API Service Layer                          │        │
│  └────────────────────────────────────────────────────┘        │
└────────────────────────────┬────────────────────────────────────┘
                             │ REST API
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Backend API Layer                          │
│  ┌──────────────────────────────────────────────────┐          │
│  │           Express.js REST API Server              │          │
│  │  ┌─────────┐ ┌─────────┐ ┌──────────┐           │          │
│  │  │  Auth   │ │ Devices │ │  Rules   │           │          │
│  │  │ Routes  │ │ Routes  │ │  Routes  │           │          │
│  │  └─────────┘ └─────────┘ └──────────┘           │          │
│  │  ┌─────────┐ ┌─────────────────────┐            │          │
│  │  │ Alerts  │ │    Dashboard        │            │          │
│  │  │ Routes  │ │    Routes           │            │          │
│  │  └─────────┘ └─────────────────────┘            │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                  │
│  ┌──────────────────────────────────────────────────┐          │
│  │         Middleware Layer                          │          │
│  │  • Authentication (JWT)                           │          │
│  │  • Rate Limiting                                  │          │
│  │  • CORS                                           │          │
│  │  • Helmet Security                                │          │
│  └──────────────────────────────────────────────────┘          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Layer (Phase 1)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Palo Alto   │  │   EntraID    │  │   Alerts     │         │
│  │  Rules JSON  │  │  Rules JSON  │  │   JSON       │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │   Devices    │  │  Statistics  │                            │
│  │    JSON      │  │    JSON      │                            │
│  └──────────────┘  └──────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Frontend Architecture

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Layout.jsx      # Application layout wrapper
│   │   └── ProtectedRoute.jsx  # Route authentication
│   ├── pages/              # Page components
│   │   ├── Dashboard.jsx   # Main dashboard
│   │   ├── Devices.jsx     # Device management
│   │   ├── Rules.jsx       # Detection rules
│   │   ├── Alerts.jsx      # Alert management
│   │   ├── PaloAltoConfig.jsx  # Palo Alto configuration
│   │   └── Login.jsx       # Authentication page
│   ├── context/            # React Context providers
│   │   └── AuthContext.jsx # Authentication state
│   ├── services/           # API communication
│   │   └── api.js          # Axios configuration
│   ├── styles/             # Global styles
│   │   └── global.css      # Application styles
│   ├── App.jsx             # Application root
│   └── main.jsx            # Application entry
├── public/                 # Static assets
├── package.json            # Dependencies
└── vite.config.js          # Vite configuration
```

### Backend Architecture

```
backend/
├── src/
│   ├── routes/             # API route handlers
│   │   ├── auth.js         # Authentication endpoints
│   │   ├── devices.js      # Device management
│   │   ├── rules.js        # Detection rules
│   │   ├── alerts.js       # Alert management
│   │   └── dashboard.js    # Dashboard data
│   ├── middleware/         # Express middleware
│   │   └── auth.js         # JWT authentication
│   ├── controllers/        # Business logic (Phase 2)
│   ├── models/             # Data models (Phase 2)
│   ├── services/           # Service layer (Phase 2)
│   ├── config/             # Configuration (Phase 2)
│   └── server.js           # Application entry
├── tests/                  # Test files
├── package.json            # Dependencies
└── .env.example            # Environment template
```

## Data Flow

### Authentication Flow

```
1. User enters credentials
   ↓
2. Frontend sends POST /api/auth/login
   ↓
3. Backend validates credentials
   ↓
4. Backend generates JWT token
   ↓
5. Frontend stores token in localStorage
   ↓
6. Frontend includes token in Authorization header
   ↓
7. Backend middleware validates token
   ↓
8. Protected route accessed
```

### API Request Flow

```
Browser → Frontend (React)
    ↓
API Service (Axios)
    ↓
HTTP Request (JWT Token)
    ↓
Backend (Express)
    ↓
Authentication Middleware
    ↓
Rate Limiting Middleware
    ↓
Route Handler
    ↓
Data Layer (JSON Files)
    ↓
Response (JSON)
    ↓
Frontend State Update
    ↓
UI Re-render
```

## Security Architecture

### Authentication & Authorization

```
┌──────────────────────────────────────┐
│     Authentication Layer              │
│  ┌────────────────────────────────┐  │
│  │  JWT Token Generation          │  │
│  │  • bcrypt password hashing     │  │
│  │  • Token expiration: 24h       │  │
│  │  • Secure token storage        │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
          ↓
┌──────────────────────────────────────┐
│     Authorization Middleware          │
│  ┌────────────────────────────────┐  │
│  │  Token Validation              │  │
│  │  • Verify JWT signature        │  │
│  │  • Check expiration            │  │
│  │  • Extract user context        │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
          ↓
┌──────────────────────────────────────┐
│     Protected Resources               │
│  • Device management                  │
│  • Rule configuration                 │
│  • Alert management                   │
│  • Dashboard data                     │
└──────────────────────────────────────┘
```

### Security Layers

1. **Transport Security**
   - HTTPS encryption (Production)
   - TLS 1.2+ required

2. **Application Security**
   - JWT authentication
   - bcrypt password hashing (10 rounds)
   - CORS protection
   - Helmet.js security headers
   - Rate limiting

3. **API Security**
   - Token-based authentication
   - Request validation
   - Error handling
   - Logging and monitoring

## Technology Stack

### Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2 | UI framework |
| Material-UI | 5.15 | Component library |
| React Router | 6.20 | Client-side routing |
| Axios | 1.6 | HTTP client |
| Recharts | 2.10 | Data visualization |
| Vite | 5.0 | Build tool |
| date-fns | 2.30 | Date formatting |

### Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Node.js | 18+ | Runtime environment |
| Express | 4.18 | Web framework |
| JWT | 9.0 | Token generation |
| bcryptjs | 2.4 | Password hashing |
| Helmet | 7.1 | Security headers |
| Morgan | 1.10 | HTTP logging |
| CORS | 2.8 | Cross-origin support |
| Rate Limit | 7.1 | API throttling |

## Phase 1 vs Future Phases

### Phase 1 (Current)

- ✅ JSON file-based data storage
- ✅ Mock device integrations
- ✅ Simple authentication
- ✅ Basic CRUD operations
- ✅ Dashboard visualizations

### Phase 2 (Planned)

- 🔄 PostgreSQL database
- 🔄 Real device integrations
- 🔄 Advanced correlation engine
- 🔄 SOAR playbook automation
- 🔄 WebSocket real-time updates

### Phase 3 (Planned)

- 🔮 Elasticsearch for search
- 🔮 Redis caching layer
- 🔮 Machine learning models
- 🔮 Advanced threat intelligence
- 🔮 Multi-tenancy support

## Scalability Considerations

### Horizontal Scaling

```
┌─────────────┐
│Load Balancer│
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──▼──┐ ┌──▼──┐ ┌──────┐
│API 1│ │API 2│ │API N │
└──┬──┘ └──┬──┘ └──┬───┘
   │       │       │
   └───┬───┴───┬───┘
       │       │
   ┌───▼───────▼───┐
   │   Database    │
   └───────────────┘
```

### Performance Optimization

1. **Frontend**
   - Code splitting
   - Lazy loading
   - Asset optimization
   - CDN distribution

2. **Backend**
   - Connection pooling (Phase 2)
   - Caching layer (Phase 2)
   - Query optimization
   - Compression

3. **Data**
   - Indexing strategies
   - Data partitioning
   - Archive policies

## Monitoring & Observability

### Logging Strategy

```
┌─────────────────────────────────────┐
│        Application Logs              │
│  • Request/Response logs             │
│  • Error logs                        │
│  • Security events                   │
│  • Performance metrics               │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│      Log Aggregation                 │
│  • Winston (Node.js)                 │
│  • Morgan (HTTP)                     │
│  • Console (Development)             │
│  • File/Service (Production)         │
└─────────────────────────────────────┘
```

### Metrics Collection

- Request count
- Response time
- Error rate
- CPU/Memory usage
- Active users
- Alert frequency

## Deployment Architecture

### Development

```
localhost:3000 (Frontend) ← → localhost:5000 (Backend)
```

### Production

```
┌──────────────┐
│    Nginx     │ (Reverse Proxy)
│ Port 80/443  │
└──────┬───────┘
       │
   ┌───┴────┐
   │        │
┌──▼───┐ ┌─▼────┐
│React │ │Express│
│ :3000│ │ :5000 │
└──────┘ └───┬───┘
             │
        ┌────▼────┐
        │Data     │
        │Storage  │
        └─────────┘
```

## API Design Principles

### RESTful Architecture

- Resource-based URLs
- HTTP methods (GET, POST, PUT, DELETE)
- Stateless communication
- JSON response format
- Standard status codes

### Response Format

```json
{
  "success": true,
  "data": { ... },
  "count": 10,
  "timestamp": "2025-11-12T..."
}
```

### Error Format

```json
{
  "error": "Error type",
  "message": "Detailed message",
  "timestamp": "2025-11-12T..."
}
```

## Database Schema (Phase 2)

Future database structure:

- **users** - User accounts and authentication
- **devices** - Connected security devices
- **rules** - Detection rule configurations
- **alerts** - Security alerts and incidents
- **audit_logs** - System audit trail
- **integrations** - External service configs

## Integration Points

### Current (Phase 1)

- Palo Alto NGFW (Mock)
- Microsoft EntraID (Mock)

### Planned (Phase 2+)

- CrowdStrike Falcon
- Splunk/SIEM
- ServiceNow
- Threat Intelligence Feeds
- Cloud platforms (AWS, Azure, GCP)

## Conclusion

The SOaC Framework architecture is designed for:

- ✅ **Scalability** - Horizontal and vertical growth
- ✅ **Security** - Multiple security layers
- ✅ **Maintainability** - Clean code organization
- ✅ **Extensibility** - Easy to add new features
- ✅ **Performance** - Optimized for speed
- ✅ **Reliability** - Robust error handling

---

**SOaC Framework Team © 2025**
