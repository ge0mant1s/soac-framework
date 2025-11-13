
"""
Generic SIEM API Client
Supports Splunk and Elastic (Elasticsearch) SIEM platforms
"""
import requests
import logging
from typing import Dict, Any, List, Optional, Literal
from datetime import datetime, timedelta
import base64

logger = logging.getLogger(__name__)


class SIEMClient:
    """
    Generic SIEM client supporting multiple platforms
    Currently supports: Splunk, Elastic (Elasticsearch)
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize SIEM client with configuration
        
        Args:
            config: Dictionary containing:
                - api_url: Base URL for SIEM API
                - username: Username for authentication
                - password: Password for authentication
                - siem_type: Type of SIEM (splunk or elastic)
                - verify_ssl: Optional, default True
        """
        self.api_url = config.get("api_url", "").rstrip("/")
        self.username = config.get("username", "")
        self.password = config.get("password", "")
        self.siem_type = config.get("siem_type", "splunk").lower()
        self.verify_ssl = config.get("verify_ssl", True)
        
        if not all([self.api_url, self.username, self.password]):
            raise ValueError("api_url, username, and password are required for SIEM integration")
        
        if self.siem_type not in ["splunk", "elastic"]:
            raise ValueError("siem_type must be 'splunk' or 'elastic'")
        
        self.session = requests.Session()
        self.session.verify = self.verify_ssl
        
        # Setup authentication
        if self.siem_type == "splunk":
            self._setup_splunk_auth()
        else:
            self._setup_elastic_auth()
    
    def _setup_splunk_auth(self):
        """Setup Splunk authentication"""
        # Splunk uses token-based auth
        try:
            auth_url = f"{self.api_url}/services/auth/login"
            data = {
                "username": self.username,
                "password": self.password
            }
            
            response = requests.post(auth_url, data=data, verify=self.verify_ssl, timeout=10)
            
            if response.status_code == 200:
                # Extract session key from XML response
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.text)
                session_key = root.find(".//sessionKey")
                if session_key is not None and session_key.text:
                    self.session.headers.update({
                        "Authorization": f"Splunk {session_key.text}"
                    })
                    logger.info("Splunk authentication successful")
        except Exception as e:
            logger.error(f"Splunk authentication setup failed: {e}")
    
    def _setup_elastic_auth(self):
        """Setup Elastic authentication"""
        # Elastic uses basic auth
        auth_str = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
        self.session.headers.update({
            "Authorization": f"Basic {auth_str}",
            "Content-Type": "application/json"
        })
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to SIEM platform
        
        Returns:
            Dictionary with success status, message, and details
        """
        if self.siem_type == "splunk":
            return self._test_splunk_connection()
        else:
            return self._test_elastic_connection()
    
    def _test_splunk_connection(self) -> Dict[str, Any]:
        """Test Splunk connection"""
        try:
            # Try to authenticate
            auth_url = f"{self.api_url}/services/auth/login"
            data = {
                "username": self.username,
                "password": self.password,
                "output_mode": "json"
            }
            
            response = requests.post(auth_url, data=data, verify=self.verify_ssl, timeout=10)
            
            if response.status_code == 401:
                return {
                    "success": False,
                    "message": "Authentication failed",
                    "details": {
                        "error": "Invalid username or password",
                        "suggestion": "Verify your Splunk credentials"
                    }
                }
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": f"Connection failed with status {response.status_code}",
                    "details": {
                        "error": response.text[:200],
                        "suggestion": "Check Splunk API URL and network connectivity"
                    }
                }
            
            # Get server info
            session_key = response.json().get("sessionKey")
            headers = {"Authorization": f"Splunk {session_key}"}
            
            info_response = requests.get(
                f"{self.api_url}/services/server/info?output_mode=json",
                headers=headers,
                verify=self.verify_ssl,
                timeout=10
            )
            
            server_info = {}
            if info_response.status_code == 200:
                info_data = info_response.json()
                entry = info_data.get("entry", [{}])[0]
                content = entry.get("content", {})
                server_info = {
                    "version": content.get("version", ""),
                    "build": content.get("build", ""),
                    "server_name": content.get("serverName", "")
                }
            
            return {
                "success": True,
                "message": "Successfully connected to Splunk",
                "details": {
                    "server_info": server_info,
                    "api_version": "Splunk REST API",
                    "latency_ms": int(response.elapsed.total_seconds() * 1000)
                }
            }
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "Connection timeout",
                "details": {
                    "error": "Request timed out after 10 seconds",
                    "suggestion": "Check network connectivity to Splunk server"
                }
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "Connection error",
                "details": {
                    "error": str(e),
                    "suggestion": "Verify Splunk API URL and network connectivity"
                }
            }
        except Exception as e:
            logger.error(f"Splunk connection test failed: {e}", exc_info=True)
            return {
                "success": False,
                "message": "Unexpected error during connection test",
                "details": {
                    "error": str(e),
                    "suggestion": "Check logs for detailed error information"
                }
            }
    
    def _test_elastic_connection(self) -> Dict[str, Any]:
        """Test Elastic connection"""
        try:
            response = self.session.get(f"{self.api_url}/", timeout=10)
            
            if response.status_code == 401:
                return {
                    "success": False,
                    "message": "Authentication failed",
                    "details": {
                        "error": "Invalid username or password",
                        "suggestion": "Verify your Elasticsearch credentials"
                    }
                }
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": f"Connection failed with status {response.status_code}",
                    "details": {
                        "error": response.text[:200],
                        "suggestion": "Check Elasticsearch API URL and network connectivity"
                    }
                }
            
            cluster_info = response.json()
            
            return {
                "success": True,
                "message": "Successfully connected to Elasticsearch",
                "details": {
                    "cluster_info": {
                        "name": cluster_info.get("cluster_name", ""),
                        "version": cluster_info.get("version", {}).get("number", ""),
                        "tagline": cluster_info.get("tagline", "")
                    },
                    "api_version": "Elasticsearch REST API",
                    "latency_ms": int(response.elapsed.total_seconds() * 1000)
                }
            }
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "Connection timeout",
                "details": {
                    "error": "Request timed out after 10 seconds",
                    "suggestion": "Check network connectivity to Elasticsearch server"
                }
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "Connection error",
                "details": {
                    "error": str(e),
                    "suggestion": "Verify Elasticsearch API URL and network connectivity"
                }
            }
        except Exception as e:
            logger.error(f"Elastic connection test failed: {e}", exc_info=True)
            return {
                "success": False,
                "message": "Unexpected error during connection test",
                "details": {
                    "error": str(e),
                    "suggestion": "Check logs for detailed error information"
                }
            }
    
    def search_events(self, query: str, time_range: str = "24h", limit: int = 100) -> List[Dict[str, Any]]:
        """
        Search for events in SIEM
        
        Args:
            query: Search query in platform-specific format
            time_range: Time range (e.g., "24h", "7d")
            limit: Maximum number of results
            
        Returns:
            List of event dictionaries
        """
        if self.siem_type == "splunk":
            return self._search_splunk(query, time_range, limit)
        else:
            return self._search_elastic(query, time_range, limit)
    
    def _search_splunk(self, query: str, time_range: str, limit: int) -> List[Dict[str, Any]]:
        """Search Splunk for events"""
        try:
            # Create search job
            search_url = f"{self.api_url}/services/search/jobs"
            data = {
                "search": f"search {query}",
                "earliest_time": f"-{time_range}",
                "latest_time": "now",
                "output_mode": "json"
            }
            
            response = self.session.post(search_url, data=data, timeout=30)
            
            if response.status_code != 201:
                logger.error(f"Failed to create Splunk search job: {response.status_code}")
                return []
            
            # Get search job SID
            job_data = response.json()
            sid = job_data.get("sid")
            
            if not sid:
                logger.error("No search job SID returned")
                return []
            
            # Poll for results (simplified - in production, implement proper polling)
            import time
            time.sleep(2)
            
            results_url = f"{self.api_url}/services/search/jobs/{sid}/results"
            params = {"output_mode": "json", "count": limit}
            
            results_response = self.session.get(results_url, params=params, timeout=30)
            
            if results_response.status_code == 200:
                results_data = results_response.json()
                events = results_data.get("results", [])
                logger.info(f"Fetched {len(events)} events from Splunk")
                return events
            
            return []
            
        except Exception as e:
            logger.error(f"Error searching Splunk: {e}", exc_info=True)
            return []
    
    def _search_elastic(self, query: str, time_range: str, limit: int) -> List[Dict[str, Any]]:
        """Search Elasticsearch for events"""
        try:
            # Convert time range to timestamp
            hours = self._parse_time_range(time_range)
            from_time = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
            
            search_body = {
                "query": {
                    "bool": {
                        "must": [
                            {"query_string": {"query": query}},
                            {"range": {"@timestamp": {"gte": from_time}}}
                        ]
                    }
                },
                "size": limit,
                "sort": [{"@timestamp": "desc"}]
            }
            
            response = self.session.post(
                f"{self.api_url}/_search",
                json=search_body,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                hits = data.get("hits", {}).get("hits", [])
                events = [hit["_source"] for hit in hits]
                logger.info(f"Fetched {len(events)} events from Elasticsearch")
                return events
            
            logger.error(f"Elastic search failed: {response.status_code}")
            return []
            
        except Exception as e:
            logger.error(f"Error searching Elasticsearch: {e}", exc_info=True)
            return []
    
    def get_device_health(self) -> Dict[str, Any]:
        """
        Get SIEM health metrics
        
        Returns:
            Dictionary with health metrics
        """
        try:
            if self.siem_type == "splunk":
                response = self.session.get(
                    f"{self.api_url}/services/server/info?output_mode=json",
                    timeout=10
                )
            else:
                response = self.session.get(f"{self.api_url}/_cluster/health", timeout=10)
            
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "siem_type": self.siem_type,
                    "response_time_ms": int(response.elapsed.total_seconds() * 1000)
                }
            
            return {"status": "unhealthy", "error": f"API returned status {response.status_code}"}
            
        except Exception as e:
            logger.error(f"Error fetching device health: {e}")
            return {"status": "error", "error": str(e)}
    
    def _parse_time_range(self, time_range: str) -> int:
        """Parse time range string to hours"""
        try:
            if time_range.endswith("h"):
                return int(time_range[:-1])
            elif time_range.endswith("d"):
                return int(time_range[:-1]) * 24
            else:
                return 24  # Default to 24 hours
        except Exception:
            return 24
