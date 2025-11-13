
"""
Microsoft Entra ID (Azure AD) API Client
Supports OAuth authentication and Microsoft Graph API integration
"""
import requests
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import time

logger = logging.getLogger(__name__)


class EntraIDClient:
    """
    Client for Microsoft Entra ID (Azure AD) integration
    Uses Microsoft Graph API for sign-in logs, user information, and security policies
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Entra ID client with configuration
        
        Args:
            config: Dictionary containing:
                - tenant_id: Azure AD tenant ID
                - client_id: Application (client) ID
                - client_secret: Client secret
                - graph_api_url: Optional, defaults to https://graph.microsoft.com/v1.0
        """
        self.tenant_id = config.get("tenant_id", "")
        self.client_id = config.get("client_id", "")
        self.client_secret = config.get("client_secret", "")
        self.graph_api_url = config.get("graph_api_url", "https://graph.microsoft.com/v1.0")
        
        if not all([self.tenant_id, self.client_id, self.client_secret]):
            raise ValueError("tenant_id, client_id, and client_secret are required for Entra ID integration")
        
        self.token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        self.access_token = None
        self.token_expires_at = None
        self.session = requests.Session()
    
    def _get_access_token(self) -> Optional[str]:
        """
        Get OAuth access token for Microsoft Graph API
        Caches token until expiration
        
        Returns:
            Access token string or None on failure
        """
        # Return cached token if still valid
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token
        
        try:
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": "https://graph.microsoft.com/.default",
                "grant_type": "client_credentials"
            }
            
            response = requests.post(self.token_url, data=data, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Failed to get access token: {response.status_code} - {response.text}")
                return None
            
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            expires_in = token_data.get("expires_in", 3600)
            
            # Set expiration with 5-minute buffer
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 300)
            
            logger.info("Successfully obtained Entra ID access token")
            return self.access_token
            
        except Exception as e:
            logger.error(f"Error getting access token: {e}", exc_info=True)
            return None
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to Microsoft Entra ID
        
        Returns:
            Dictionary with success status, message, and details
        """
        try:
            start_time = time.time()
            
            # Get access token
            token = self._get_access_token()
            if not token:
                return {
                    "success": False,
                    "message": "Authentication failed",
                    "details": {
                        "error": "Failed to obtain OAuth access token",
                        "suggestion": "Verify tenant_id, client_id, and client_secret are correct"
                    }
                }
            
            # Test API by getting organization info
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            response = self.session.get(
                f"{self.graph_api_url}/organization",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 401:
                return {
                    "success": False,
                    "message": "Authentication failed",
                    "details": {
                        "error": "Token validation failed",
                        "suggestion": "Check application permissions in Azure AD"
                    }
                }
            
            if response.status_code == 403:
                return {
                    "success": False,
                    "message": "Authorization failed",
                    "details": {
                        "error": "Insufficient permissions",
                        "suggestion": "Grant required permissions (Directory.Read.All, AuditLog.Read.All) to the application"
                    }
                }
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": f"API request failed with status {response.status_code}",
                    "details": {
                        "error": response.text[:200],
                        "suggestion": "Check Graph API endpoint and permissions"
                    }
                }
            
            org_data = response.json()
            org_info = {}
            if org_data.get("value"):
                org = org_data["value"][0]
                org_info = {
                    "display_name": org.get("displayName", ""),
                    "tenant_id": org.get("id", ""),
                    "verified_domains": len(org.get("verifiedDomains", []))
                }
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            return {
                "success": True,
                "message": "Successfully connected to Microsoft Entra ID",
                "details": {
                    "organization": org_info,
                    "api_version": "Microsoft Graph v1.0",
                    "latency_ms": latency_ms
                }
            }
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "Connection timeout",
                "details": {
                    "error": "Request timed out after 10 seconds",
                    "suggestion": "Check network connectivity to Microsoft Graph API"
                }
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "Connection error",
                "details": {
                    "error": str(e),
                    "suggestion": "Verify network connectivity to login.microsoftonline.com and graph.microsoft.com"
                }
            }
        except Exception as e:
            logger.error(f"Entra ID connection test failed: {e}", exc_info=True)
            return {
                "success": False,
                "message": "Unexpected error during connection test",
                "details": {
                    "error": str(e),
                    "suggestion": "Check logs for detailed error information"
                }
            }
    
    def get_sign_in_logs(self, hours: int = 24, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch sign-in logs from Entra ID
        
        Args:
            hours: Number of hours to look back
            limit: Maximum number of logs to retrieve
            
        Returns:
            List of sign-in log entries
        """
        try:
            token = self._get_access_token()
            if not token:
                logger.error("Failed to get access token for sign-in logs")
                return []
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Calculate timestamp for filtering
            filter_time = (datetime.utcnow() - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
            
            params = {
                "$filter": f"createdDateTime ge {filter_time}",
                "$top": limit,
                "$orderby": "createdDateTime desc"
            }
            
            response = self.session.get(
                f"{self.graph_api_url}/auditLogs/signIns",
                headers=headers,
                params=params,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch sign-in logs: {response.status_code}")
                return []
            
            data = response.json()
            logs = []
            
            for item in data.get("value", []):
                log = self._parse_sign_in_log(item)
                if log:
                    logs.append(log)
            
            logger.info(f"Fetched {len(logs)} sign-in logs from Entra ID")
            return logs
            
        except Exception as e:
            logger.error(f"Error fetching sign-in logs: {e}", exc_info=True)
            return []
    
    def get_users(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch user information from Entra ID
        
        Args:
            limit: Maximum number of users to retrieve
            
        Returns:
            List of user objects
        """
        try:
            token = self._get_access_token()
            if not token:
                logger.error("Failed to get access token for users")
                return []
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            params = {
                "$top": limit,
                "$select": "id,displayName,userPrincipalName,accountEnabled,createdDateTime"
            }
            
            response = self.session.get(
                f"{self.graph_api_url}/users",
                headers=headers,
                params=params,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch users: {response.status_code}")
                return []
            
            data = response.json()
            users = data.get("value", [])
            
            logger.info(f"Fetched {len(users)} users from Entra ID")
            return users
            
        except Exception as e:
            logger.error(f"Error fetching users: {e}", exc_info=True)
            return []
    
    def get_conditional_access_policies(self) -> List[Dict[str, Any]]:
        """
        Fetch conditional access policies from Entra ID
        
        Returns:
            List of conditional access policies
        """
        try:
            token = self._get_access_token()
            if not token:
                logger.error("Failed to get access token for policies")
                return []
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            response = self.session.get(
                f"{self.graph_api_url}/identity/conditionalAccess/policies",
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch conditional access policies: {response.status_code}")
                return []
            
            data = response.json()
            policies = data.get("value", [])
            
            logger.info(f"Fetched {len(policies)} conditional access policies from Entra ID")
            return policies
            
        except Exception as e:
            logger.error(f"Error fetching conditional access policies: {e}", exc_info=True)
            return []
    
    def get_device_health(self) -> Dict[str, Any]:
        """
        Get Entra ID service health metrics
        
        Returns:
            Dictionary with health metrics
        """
        try:
            token = self._get_access_token()
            if not token:
                return {"status": "unhealthy", "error": "Authentication failed"}
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            response = self.session.get(
                f"{self.graph_api_url}/organization",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "api_version": "Microsoft Graph v1.0",
                    "token_valid": True
                }
            
            return {"status": "unhealthy", "error": f"API returned status {response.status_code}"}
            
        except Exception as e:
            logger.error(f"Error fetching device health: {e}")
            return {"status": "error", "error": str(e)}
    
    def _parse_sign_in_log(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Parse sign-in log entry to normalized format"""
        try:
            return {
                "timestamp": item.get("createdDateTime", ""),
                "user": item.get("userPrincipalName", ""),
                "user_id": item.get("userId", ""),
                "app_display_name": item.get("appDisplayName", ""),
                "ip_address": item.get("ipAddress", ""),
                "location": self._format_location(item.get("location", {})),
                "status": item.get("status", {}).get("errorCode", 0),
                "success": item.get("status", {}).get("errorCode", 0) == 0,
                "device_detail": item.get("deviceDetail", {}),
                "risk_level": item.get("riskLevelDuringSignIn", "none")
            }
        except Exception as e:
            logger.error(f"Error parsing sign-in log: {e}")
            return {}
    
    def _format_location(self, location: Dict[str, Any]) -> str:
        """Format location information"""
        parts = []
        if location.get("city"):
            parts.append(location["city"])
        if location.get("state"):
            parts.append(location["state"])
        if location.get("countryOrRegion"):
            parts.append(location["countryOrRegion"])
        return ", ".join(parts) if parts else "Unknown"
