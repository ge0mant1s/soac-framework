
import React, { useState, useEffect } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  Chip,
} from '@mui/material';
import {
  Security as SecurityIcon,
  Rule as RuleIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import api from '../services/api';
import { format } from 'date-fns';

const COLORS = ['#f44336', '#ff9800', '#2196f3', '#4caf50'];

const StatCard = ({ title, value, icon, color }) => (
  <Card>
    <CardContent>
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Box>
          <Typography color="textSecondary" gutterBottom variant="body2">
            {title}
          </Typography>
          <Typography variant="h4">{value}</Typography>
        </Box>
        <Box sx={{ color: color, fontSize: 48 }}>
          {icon}
        </Box>
      </Box>
    </CardContent>
  </Card>
);

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await api.get('/dashboard/overview');
      setData(response.data.data);
      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load dashboard data');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  const alertsBySeverity = [
    { name: 'Critical', value: data.alerts.bySeverity.critical },
    { name: 'High', value: data.alerts.bySeverity.high },
    { name: 'Medium', value: data.alerts.bySeverity.medium },
    { name: 'Low', value: data.alerts.bySeverity.low },
  ];

  const alertsByStatus = [
    { name: 'Open', value: data.alerts.byStatus.open },
    { name: 'Investigating', value: data.alerts.byStatus.investigating },
    { name: 'Resolved', value: data.alerts.byStatus.resolved },
    { name: 'False Positive', value: data.alerts.byStatus.false_positive },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard Overview
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Real-time security operations monitoring and analytics
      </Typography>

      {/* Statistics Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Devices"
            value={data.summary.totalDevices}
            icon={<SecurityIcon fontSize="inherit" />}
            color="#1976d2"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Active Rules"
            value={data.summary.enabledRules}
            icon={<RuleIcon fontSize="inherit" />}
            color="#4caf50"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Open Alerts"
            value={data.summary.openAlerts}
            icon={<WarningIcon fontSize="inherit" />}
            color="#ff9800"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Critical Alerts"
            value={data.summary.criticalAlerts}
            icon={<WarningIcon fontSize="inherit" />}
            color="#f44336"
          />
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Alerts by Severity
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={alertsBySeverity}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" fill="#1976d2" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Alerts by Status
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={alertsByStatus}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={(entry) => entry.name}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {alertsByStatus.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Recent Alerts */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Alerts
            </Typography>
            <Box sx={{ maxHeight: 400, overflow: 'auto' }}>
              {data.alerts.recent.map((alert) => (
                <Box
                  key={alert.id}
                  sx={{
                    p: 2,
                    mb: 1,
                    border: '1px solid',
                    borderColor: 'divider',
                    borderRadius: 1,
                    '&:hover': { bgcolor: 'action.hover' },
                  }}
                >
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Box>
                      <Typography variant="subtitle1">{alert.ruleName}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        {format(new Date(alert.detectedAt), 'PPpp')}
                      </Typography>
                    </Box>
                    <Box display="flex" gap={1}>
                      <Chip
                        label={alert.severity}
                        size="small"
                        color={
                          alert.severity === 'Critical' ? 'error' :
                          alert.severity === 'High' ? 'warning' :
                          alert.severity === 'Medium' ? 'info' : 'default'
                        }
                      />
                      <Chip
                        label={alert.status}
                        size="small"
                        variant="outlined"
                      />
                    </Box>
                  </Box>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    Source: {alert.sourceIp} → Dest: {alert.destIp}
                  </Typography>
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>

        {/* Device Status */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Connected Devices
            </Typography>
            {data.devices.map((device) => (
              <Box
                key={device.id}
                sx={{
                  p: 2,
                  mb: 1,
                  border: '1px solid',
                  borderColor: 'divider',
                  borderRadius: 1,
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <Box>
                  <Typography variant="subtitle1">{device.name}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    Type: {device.type}
                  </Typography>
                </Box>
                <Chip
                  icon={<CheckCircleIcon />}
                  label={device.status}
                  size="small"
                  color="success"
                />
              </Box>
            ))}
          </Paper>
        </Grid>

        {/* Rules Summary */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Rules Summary
            </Typography>
            <Box sx={{ p: 2 }}>
              <Box display="flex" justifyContent="space-between" sx={{ mb: 2 }}>
                <Typography>Total Rules</Typography>
                <Typography variant="h6">{data.summary.totalRules}</Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" sx={{ mb: 2 }}>
                <Typography>Palo Alto NGFW</Typography>
                <Typography variant="h6">{data.rules.byDevice.paloalto}</Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" sx={{ mb: 2 }}>
                <Typography>EntraID</Typography>
                <Typography variant="h6">{data.rules.byDevice.entraid}</Typography>
              </Box>
              <Box display="flex" justifyContent="space-between">
                <Typography>Enabled</Typography>
                <Typography variant="h6">{data.summary.enabledRules}</Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
