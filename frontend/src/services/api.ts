
/**
 * API service for making HTTP requests
 */
import axios, { AxiosError } from 'axios';
import type { LoginResponse, Device, Rule, DashboardMetrics, DeviceStatusSummary, ConnectionTestResult, SyncResult, HealthResult } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Token expired or invalid, redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ============= Auth API =============

export const authAPI = {
  login: async (username: string, password: string): Promise<LoginResponse> => {
    const response = await api.post<LoginResponse>('/api/v1/auth/login', {
      username,
      password,
    });
    return response.data;
  },

  logout: async (): Promise<void> => {
    await api.post('/api/v1/auth/logout');
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },
};

// ============= Device API =============

export const deviceAPI = {
  list: async (): Promise<Device[]> => {
    const response = await api.get<Device[]>('/api/v1/devices');
    return response.data;
  },

  get: async (id: string): Promise<Device> => {
    const response = await api.get<Device>(`/api/v1/devices/${id}`);
    return response.data;
  },

  create: async (device: Partial<Device>): Promise<Device> => {
    const response = await api.post<Device>('/api/v1/devices', device);
    return response.data;
  },

  update: async (id: string, device: Partial<Device>): Promise<Device> => {
    const response = await api.put<Device>(`/api/v1/devices/${id}`, device);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/api/v1/devices/${id}`);
  },

  testConnection: async (id: string): Promise<ConnectionTestResult> => {
    const response = await api.post<ConnectionTestResult>(`/api/v1/devices/${id}/test`);
    return response.data;
  },

  sync: async (id: string): Promise<SyncResult> => {
    const response = await api.post<SyncResult>(`/api/v1/devices/${id}/sync`);
    return response.data;
  },

  getHealth: async (id: string): Promise<HealthResult> => {
    const response = await api.get<HealthResult>(`/api/v1/devices/${id}/health`);
    return response.data;
  },
};

// ============= Rule API =============

export const ruleAPI = {
  list: async (params?: { device_id?: string; severity?: string; status?: string }): Promise<Rule[]> => {
    const response = await api.get<Rule[]>('/api/v1/rules', { params });
    return response.data;
  },

  get: async (id: string): Promise<Rule> => {
    const response = await api.get<Rule>(`/api/v1/rules/${id}`);
    return response.data;
  },

  create: async (rule: Partial<Rule>): Promise<Rule> => {
    const response = await api.post<Rule>('/api/v1/rules', rule);
    return response.data;
  },

  update: async (id: string, rule: Partial<Rule>): Promise<Rule> => {
    const response = await api.put<Rule>(`/api/v1/rules/${id}`, rule);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/api/v1/rules/${id}`);
  },

  toggleStatus: async (id: string, enabled: boolean): Promise<void> => {
    await api.patch(`/api/v1/rules/${id}/status`, { enabled });
  },
};

// ============= Dashboard API =============

export const dashboardAPI = {
  getMetrics: async (): Promise<DashboardMetrics> => {
    const response = await api.get<DashboardMetrics>('/api/v1/dashboard/metrics');
    return response.data;
  },

  getDeviceHealth: async (): Promise<DeviceStatusSummary[]> => {
    const response = await api.get<DeviceStatusSummary[]>('/api/v1/dashboard/device-health');
    return response.data;
  },
};

export default api;
