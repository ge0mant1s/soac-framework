
/**
 * Dashboard page
 */
import React, { useEffect, useState } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  CircularProgress,
  Alert,
  Paper,
} from '@mui/material';
import {
  Security,
  Warning,
  PlayArrow,
  Timer,
  CheckCircle,
  Error,
  Circle,
} from '@mui/icons-material';
import { dashboardAPI } from '../services/api';
import type { DashboardMetrics, DeviceStatusSummary } from '../types';

const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [deviceHealth, setDeviceHealth] = useState<DeviceStatusSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDashboardData();
    
    // Refresh every 30 seconds
    const interval = setInterval(loadDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      setError('');
      const [metricsData, deviceData] = await Promise.all([
        dashboardAPI.getMetrics(),
        dashboardAPI.getDeviceHealth(),
      ]);
      setMetrics(metricsData);
      setDeviceHealth(deviceData);
    } catch (err: any) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical':
        return 'error';
      case 'high':
        return 'warning';
      case 'medium':
        return 'info';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'connected':
        return <CheckCircle color="success" />;
      case 'error':
        return <Error color="error" />;
      case 'disconnected':
        return <Circle color="disabled" />;
      default:
        return <Circle />;
    }
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  if (!metrics) {
    return <Alert severity="info">No dashboard data available</Alert>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mb: 3 }}>
        Real-time overview of your security operations
      </Typography>

      {/* Key Metrics */}
      <Grid container spacing={3}>
        {/* Active Incidents */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="text.secondary" gutterBottom variant="body2">
                    Active Incidents
                  </Typography>
                  <Typography variant="h4">{metrics.active_incidents}</Typography>
                </Box>
                <Security sx={{ fontSize: 40, color: 'primary.main' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Open Investigations */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="text.secondary" gutterBottom variant="body2">
                    Investigations
                  </Typography>
                  <Typography variant="h4">{metrics.open_investigations}</Typography>
                </Box>
                <Warning sx={{ fontSize: 40, color: 'warning.main' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Playbook Executions (24h) */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="text.secondary" gutterBottom variant="body2">
                    Playbooks (24h)
                  </Typography>
                  <Typography variant="h4">{metrics.playbook_executions_24h}</Typography>
                </Box>
                <PlayArrow sx={{ fontSize: 40, color: 'success.main' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* MTTI */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="text.secondary" gutterBottom variant="body2">
                    Avg MTTI
                  </Typography>
                  <Typography variant="h4">{metrics.mtti_average_minutes.toFixed(1)}m</Typography>
                </Box>
                <Timer sx={{ fontSize: 40, color: 'info.main' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Device Health and Incidents by Severity */}
      <Grid container spacing={3} sx={{ mt: 2 }}>
        {/* Device Health */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Device Health
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Grid container spacing={2}>
                  <Grid item xs={4}>
                    <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'success.light', color: 'success.contrastText' }}>
                      <Typography variant="h4">{metrics.device_health.connected}</Typography>
                      <Typography variant="caption">Connected</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={4}>
                    <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'grey.300' }}>
                      <Typography variant="h4">{metrics.device_health.disconnected}</Typography>
                      <Typography variant="caption">Disconnected</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={4}>
                    <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'error.light', color: 'error.contrastText' }}>
                      <Typography variant="h4">{metrics.device_health.error}</Typography>
                      <Typography variant="caption">Error</Typography>
                    </Paper>
                  </Grid>
                </Grid>

                <Box sx={{ mt: 3 }}>
                  {deviceHealth.map((device) => (
                    <Box
                      key={device.id}
                      display="flex"
                      alignItems="center"
                      justifyContent="space-between"
                      sx={{ py: 1, borderBottom: '1px solid', borderColor: 'divider' }}
                    >
                      <Box display="flex" alignItems="center">
                        {getStatusIcon(device.status)}
                        <Box sx={{ ml: 2 }}>
                          <Typography variant="body2">{device.name}</Typography>
                          <Typography variant="caption" color="text.secondary">
                            {device.type.toUpperCase()} • {device.rules_count} rules
                          </Typography>
                        </Box>
                      </Box>
                      <Chip
                        label={device.status}
                        size="small"
                        color={
                          device.status === 'connected'
                            ? 'success'
                            : device.status === 'error'
                            ? 'error'
                            : 'default'
                        }
                      />
                    </Box>
                  ))}
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Incidents by Severity */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Incidents by Severity
              </Typography>
              <Box sx={{ mt: 2 }}>
                {Object.entries(metrics.incidents_by_severity).map(([severity, count]) => (
                  <Box
                    key={severity}
                    display="flex"
                    alignItems="center"
                    justifyContent="space-between"
                    sx={{ py: 2, borderBottom: '1px solid', borderColor: 'divider' }}
                  >
                    <Box display="flex" alignItems="center">
                      <Chip
                        label={severity.toUpperCase()}
                        size="small"
                        color={getSeverityColor(severity) as any}
                        sx={{ minWidth: 80 }}
                      />
                      <Typography variant="body1" sx={{ ml: 2 }}>
                        {count} {count === 1 ? 'incident' : 'incidents'}
                      </Typography>
                    </Box>
                  </Box>
                ))}
              </Box>

              <Box sx={{ mt: 3, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  <strong>Performance Metrics:</strong>
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  • Mean Time to Investigate (MTTI): {metrics.mtti_average_minutes.toFixed(1)} minutes
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  • Mean Time to Detect & Act (MTTDA): {metrics.mttda_average_minutes.toFixed(1)} minutes
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
