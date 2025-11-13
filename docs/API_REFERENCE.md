# SOaC Framework - API Reference

Complete API documentation for the SOaC Framework backend.

## Base URL

```
Development: http://localhost:5000/api
Production: https://your-domain.com/api
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

---

## Authentication Endpoints

### POST /api/auth/login

Login and receive JWT token.

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin",
    "email": "admin@soacframework.local"
  }
}
```

**Error (401 Unauthorized):**
```json
{
  "error": "Authentication failed",
  "message": "Invalid credentials"
}
```

### POST /api/auth/verify

Verify JWT token validity.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "valid": true,
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

---

## Device Endpoints

### GET /api/devices

Get all devices.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "id": "device-001",
      "name": "PaloAlto-NGFW-Primary",
      "type": "paloalto_ngfw",
      "ipAddress": "192.168.1.10",
      "status": "active",
      "lastSync": "2025-11-12T10:30:00.000Z",
      "rulesCount": 12,
      "description": "Primary Palo Alto Next-Generation Firewall"
    }
  ]
}
```

### GET /api/devices/:id

Get device by ID.

**Parameters:**
- `id` (path): Device identifier

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "device-001",
    "name": "PaloAlto-NGFW-Primary",
    "type": "paloalto_ngfw",
    "ipAddress": "192.168.1.10",
    "status": "active",
    "lastSync": "2025-11-12T10:30:00.000Z",
    "rulesCount": 12,
    "description": "Primary Palo Alto Next-Generation Firewall"
  }
}
```

### POST /api/devices/:id/sync

Sync device rules.

**Parameters:**
- `id` (path): Device identifier

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Device PaloAlto-NGFW-Primary synced successfully",
  "data": {
    "deviceId": "device-001",
    "syncedAt": "2025-11-12T11:00:00.000Z",
    "status": "completed"
  }
}
```

---

## Rules Endpoints

### GET /api/rules

Get all detection rules.

**Query Parameters:**
- `type` (optional): Filter by device type (`paloalto` or `entraid`)

**Examples:**
```
GET /api/rules
GET /api/rules?type=paloalto
GET /api/rules?type=entraid
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 28,
  "data": [
    {
      "id": "PA-001",
      "useCase": "Intrusion",
      "detectionRule": "Hosts repeatedly connecting to the same external IP...",
      "incidentRule": "Pattern sustained across multiple hosts...",
      "severity": "High",
      "mitreTactic": "Command and Control",
      "mitreTechnique": "T1071.001 (Web Protocols)",
      "category": "Beaconing",
      "cqlQuery": "#repo = paloalto\n| event.panw.panos.action = allow...",
      "enabled": true,
      "createdAt": "2025-10-15T10:00:00.000Z",
      "lastModified": "2025-11-12T10:00:00.000Z"
    }
  ]
}
```

### GET /api/rules/:id

Get rule by ID.

**Parameters:**
- `id` (path): Rule identifier (e.g., PA-001, EA-001)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "PA-001",
    "useCase": "Intrusion",
    "detectionRule": "Hosts repeatedly connecting to the same external IP...",
    "incidentRule": "Pattern sustained across multiple hosts...",
    "severity": "High",
    "mitreTactic": "Command and Control",
    "mitreTechnique": "T1071.001 (Web Protocols)",
    "category": "Beaconing",
    "cqlQuery": "#repo = paloalto\n| event.panw.panos.action = allow...",
    "enabled": true,
    "createdAt": "2025-10-15T10:00:00.000Z",
    "lastModified": "2025-11-12T10:00:00.000Z"
  }
}
```

### PUT /api/rules/:id

Update rule.

**Parameters:**
- `id` (path): Rule identifier

**Request:**
```json
{
  "detectionRule": "Updated detection logic",
  "severity": "Critical",
  "enabled": false
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Rule updated successfully",
  "data": {
    "id": "PA-001",
    "useCase": "Intrusion",
    "detectionRule": "Updated detection logic",
    "severity": "Critical",
    "enabled": false,
    "lastModified": "2025-11-12T11:30:00.000Z"
  }
}
```

### POST /api/rules/:id/toggle

Toggle rule enabled/disabled state.

**Parameters:**
- `id` (path): Rule identifier

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Rule enabled successfully",
  "data": {
    "id": "PA-001",
    "enabled": true,
    "lastModified": "2025-11-12T11:35:00.000Z"
  }
}
```

### GET /api/rules/stats/summary

Get rules statistics.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "total": 28,
    "enabled": 26,
    "disabled": 2,
    "byDevice": {
      "paloalto": 12,
      "entraid": 16
    },
    "bySeverity": {
      "critical": 3,
      "high": 15,
      "medium": 8,
      "low": 2
    }
  }
}
```

---

## Alerts Endpoints

### GET /api/alerts

Get all alerts with optional filtering.

**Query Parameters:**
- `status` (optional): Filter by status (`open`, `investigating`, `resolved`, `false_positive`)
- `severity` (optional): Filter by severity (`Critical`, `High`, `Medium`, `Low`)
- `limit` (optional): Limit results (integer)

**Examples:**
```
GET /api/alerts
GET /api/alerts?status=open
GET /api/alerts?severity=Critical
GET /api/alerts?status=open&severity=High&limit=10
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 20,
  "data": [
    {
      "id": "alert-0001",
      "ruleId": "PA-001",
      "ruleName": "Hosts repeatedly connecting to the same external IP...",
      "severity": "High",
      "status": "open",
      "detectedAt": "2025-11-12T09:15:00.000Z",
      "sourceIp": "192.168.1.100",
      "destIp": "10.0.1.50",
      "userName": "user15@soacframework.local",
      "deviceName": "PaloAlto-NGFW-Primary",
      "mitreTactic": "Command and Control",
      "mitreTechnique": "T1071.001 (Web Protocols)"
    }
  ]
}
```

### GET /api/alerts/:id

Get alert by ID.

**Parameters:**
- `id` (path): Alert identifier

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "alert-0001",
    "ruleId": "PA-001",
    "ruleName": "Hosts repeatedly connecting to the same external IP...",
    "severity": "High",
    "status": "open",
    "detectedAt": "2025-11-12T09:15:00.000Z",
    "sourceIp": "192.168.1.100",
    "destIp": "10.0.1.50",
    "userName": "user15@soacframework.local",
    "deviceName": "PaloAlto-NGFW-Primary",
    "mitreTactic": "Command and Control",
    "mitreTechnique": "T1071.001 (Web Protocols)"
  }
}
```

### PUT /api/alerts/:id/status

Update alert status.

**Parameters:**
- `id` (path): Alert identifier

**Request:**
```json
{
  "status": "resolved",
  "comment": "False positive - legitimate backup service"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Alert status updated successfully",
  "data": {
    "id": "alert-0001",
    "status": "resolved",
    "updatedAt": "2025-11-12T11:45:00.000Z",
    "updatedBy": "admin",
    "comment": "False positive - legitimate backup service"
  }
}
```

### GET /api/alerts/stats/summary

Get alert statistics.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "total": 20,
    "byStatus": {
      "open": 5,
      "investigating": 3,
      "resolved": 10,
      "false_positive": 2
    },
    "bySeverity": {
      "critical": 2,
      "high": 8,
      "medium": 7,
      "low": 3
    },
    "recentAlerts": [
      {
        "id": "alert-0020",
        "severity": "Critical",
        "detectedAt": "2025-11-12T11:30:00.000Z"
      }
    ]
  }
}
```

---

## Dashboard Endpoints

### GET /api/dashboard/overview

Get complete dashboard overview.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "summary": {
      "totalDevices": 2,
      "activeDevices": 2,
      "totalRules": 28,
      "enabledRules": 26,
      "totalAlerts": 20,
      "openAlerts": 5,
      "criticalAlerts": 2
    },
    "alerts": {
      "byStatus": {
        "open": 5,
        "investigating": 3,
        "resolved": 10,
        "false_positive": 2
      },
      "bySeverity": {
        "critical": 2,
        "high": 8,
        "medium": 7,
        "low": 3
      },
      "recent": [...]
    },
    "rules": {
      "byDevice": {
        "paloalto": 12,
        "entraid": 16
      },
      "bySeverity": {
        "critical": 3,
        "high": 15,
        "medium": 8,
        "low": 2
      }
    },
    "devices": [...],
    "timestamp": "2025-11-12T12:00:00.000Z"
  }
}
```

### GET /api/dashboard/threat-landscape

Get threat landscape data.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "byTactic": [
      {
        "tactic": "Command and Control",
        "count": 8
      },
      {
        "tactic": "Credential Access",
        "count": 6
      }
    ],
    "byTechnique": [
      {
        "technique": "T1071.001 (Web Protocols)",
        "count": 5
      },
      {
        "technique": "T1110 (Brute Force)",
        "count": 4
      }
    ],
    "totalThreats": 20,
    "uniqueTactics": 8,
    "uniqueTechniques": 15
  }
}
```

---

## Health Check

### GET /health

Check API health status (no authentication required).

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-12T12:00:00.000Z",
  "version": "1.0.0",
  "service": "SOaC Framework API"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request",
  "message": "Missing required parameters",
  "timestamp": "2025-11-12T12:00:00.000Z"
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication required",
  "message": "No token provided",
  "timestamp": "2025-11-12T12:00:00.000Z"
}
```

### 403 Forbidden
```json
{
  "error": "Invalid token",
  "message": "Token verification failed",
  "timestamp": "2025-11-12T12:00:00.000Z"
}
```

### 404 Not Found
```json
{
  "error": "Not found",
  "message": "Resource not found",
  "timestamp": "2025-11-12T12:00:00.000Z"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred",
  "timestamp": "2025-11-12T12:00:00.000Z"
}
```

---

## Rate Limiting

- **Window**: 15 minutes (900,000 ms)
- **Max Requests**: 100 per window
- **Response when exceeded**:
```json
{
  "error": "Too many requests",
  "message": "Rate limit exceeded. Please try again later.",
  "retryAfter": 300
}
```

---

## Best Practices

### Authentication
1. Always include Authorization header with Bearer token
2. Store tokens securely (never in source code)
3. Handle token expiration gracefully
4. Clear tokens on logout

### Error Handling
1. Check response status codes
2. Parse error messages
3. Implement retry logic for transient errors
4. Log errors for debugging

### Performance
1. Use query parameters for filtering
2. Implement pagination for large datasets
3. Cache responses when appropriate
4. Use compression for large payloads

### Security
1. Always use HTTPS in production
2. Validate and sanitize input
3. Never expose sensitive data in URLs
4. Implement proper CORS configuration

---

## Code Examples

### JavaScript (Axios)
```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';
const token = localStorage.getItem('token');

// Login
const login = async () => {
  const response = await axios.post(`${API_BASE_URL}/auth/login`, {
    username: 'admin',
    password: 'admin123'
  });
  localStorage.setItem('token', response.data.token);
};

// Get devices
const getDevices = async () => {
  const response = await axios.get(`${API_BASE_URL}/devices`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return response.data.data;
};
```

### Python (requests)
```python
import requests

API_BASE_URL = 'http://localhost:5000/api'

# Login
response = requests.post(f'{API_BASE_URL}/auth/login', json={
    'username': 'admin',
    'password': 'admin123'
})
token = response.json()['token']

# Get devices
headers = {'Authorization': f'Bearer {token}'}
response = requests.get(f'{API_BASE_URL}/devices', headers=headers)
devices = response.json()['data']
```

### cURL
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Get devices (replace <token> with actual token)
curl -X GET http://localhost:5000/api/devices \
  -H "Authorization: Bearer <token>"
```

---

**SOaC Framework Team © 2025**
