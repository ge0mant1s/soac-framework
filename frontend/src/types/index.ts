
/**
 * Type definitions for the SOaC Framework
 */

export interface User {
  id: string;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface Device {
  id: string;
  name: string;
  type: 'paloalto' | 'entraid' | 'siem';
  enabled: boolean;
  config: Record<string, any>;
  connection_status: 'connected' | 'disconnected' | 'error';
  last_tested: string | null;
  last_sync: string | null;
  last_connected: string | null;
  health_status: 'healthy' | 'unhealthy' | 'unknown' | 'error';
  event_count: number;
  rules_count: number;
  created_at: string;
  updated_at: string;
}

export interface Rule {
  id: string;
  device_id: string;
  use_case_id: string | null;
  name: string;
  description: string | null;
  incident_rule: string | null;
  severity: 'Critical' | 'High' | 'Medium' | 'Low';
  mitre_tactic: string | null;
  mitre_technique: string | null;
  category: string | null;
  query: string;
  enabled: boolean;
  status: 'draft' | 'testing' | 'active' | 'disabled';
  false_positive_rate: number | null;
  detection_count: number;
  created_at: string;
  updated_at: string;
}

export interface DashboardMetrics {
  active_incidents: number;
  open_investigations: number;
  playbook_executions_24h: number;
  mtti_average_minutes: number;
  mttda_average_minutes: number;
  device_health: {
    connected: number;
    disconnected: number;
    error: number;
  };
  incidents_by_severity: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
}

export interface DeviceStatusSummary {
  id: string;
  name: string;
  type: string;
  status: string;
  last_tested: string | null;
  rules_count: number;
}

export interface ConnectionTestResult {
  success: boolean;
  message: string;
  details?: Record<string, any>;
}

export interface SyncResult {
  success: boolean;
  message: string;
  rules_synced: number;
  rules_created: number;
  rules_updated: number;
  last_sync: string | null;
  error?: string;
}

export interface HealthResult {
  success: boolean;
  message: string;
  health: Record<string, any>;
}

export interface APIError {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
  timestamp: string;
}

export interface Event {
  id: string;
  device_id: string;
  timestamp: string;
  event_type: string | null;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info' | null;
  raw_data: Record<string, any>;
  normalized_data: Record<string, any> | null;
  processed: boolean;
  detection_results: Record<string, any> | null;
  created_at: string;
}

export interface EventListResponse {
  total: number;
  events: Event[];
  page: number;
  page_size: number;
}

export interface EventStatsResponse {
  total_events: number;
  events_by_type: Record<string, number>;
  events_by_severity: Record<string, number>;
  events_by_device: Record<string, number>;
  processed_events: number;
  unprocessed_events: number;
}

export interface EventCollectionRequest {
  hours?: number;
  limit?: number;
}

export interface EventCollectionResponse {
  success: boolean;
  device_id: string;
  events_collected: number;
  events_stored: number;
  message?: string;
  error?: string;
}
