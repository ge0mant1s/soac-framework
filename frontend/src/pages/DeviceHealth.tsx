/**
 * Device Health Dashboard
 * Shows comprehensive health status of all integrated security devices
 */
import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  Button,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Tooltip,
  IconButton,
} from '@mui/material';
import {
  CheckCircle,
  Error,
  Circle,
  Refresh,
  Timeline,
  Cable,
  Sync,
  Info,
} from '@mui/icons-material';
import { deviceAPI } from '../services/api';
import type { Device } from '../types';

const DeviceHealth: React.FC = () => {
  const [devices, setDevices] = useState<Device[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [refreshing, setRefreshing] = useState(false);
  const [testingDevice, setTestingDevice] = useState<string | null>(null);

  useEffect(() => {
    loadDevices();
  }, []);

  const loadDevices = async () => {
    try {
      setError('');
      const data = await deviceAPI.list();
      setDevices(data);
    } catch (err: any) {
      setError('Failed to load devices');
      console.error(err);
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    setRefreshing(true);
    loadDevices();
  };

  const handleTestConnection = async (id: string) => {
    try {
      setTestingDevice(id);
      await deviceAPI.testConnection(id);
      await loadDevices();
    } catch (err: any) {
      console.error('Connection test failed:', err);
    } finally {
      setTestingDevice(null);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected':
        return 'success';
      case 'error':
        return 'error';
      case 'disconnected':
        return 'default';
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

  const getHealthSummary = () => {
    const connected = devices.filter((d) => d.connection_status === 'connected').length;
    const error = devices.filter((d) => d.connection_status === 'error').length;
    const disconnected = devices.filter((d) => d.connection_status === 'disconnected').length;
    const total = devices.length;

    return { connected, error, disconnected, total };
  };

  const formatTimestamp = (timestamp: string | null) => {
    if (!timestamp) return 'Never';
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'Just now';
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  const healthSummary = getHealthSummary();

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Device Health Dashboard
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Monitor the health and connectivity status of all security devices
          </Typography>
        </Box>
        <Button
          variant="outlined"
          startIcon={refreshing ? <CircularProgress size={20} /> : <Refresh />}
          onClick={handleRefresh}
          disabled={refreshing}
        >
          Refresh All
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Health Summary Cards */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <Timeline color="action" sx={{ mr: 1 }} />
                <Typography variant="h6">Total Devices</Typography>
              </Box>
              <Typography variant="h3">{healthSummary.total}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: 'success.light' }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <CheckCircle sx={{ mr: 1, color: 'success.dark' }} />
                <Typography variant="h6" color="success.dark">
                  Connected
                </Typography>
              </Box>
              <Typography variant="h3" color="success.dark">
                {healthSummary.connected}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: 'error.light' }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <Error sx={{ mr: 1, color: 'error.dark' }} />
                <Typography variant="h6" color="error.dark">
                  Error
                </Typography>
              </Box>
              <Typography variant="h3" color="error.dark">
                {healthSummary.error}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: 'grey.200' }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <Circle sx={{ mr: 1, color: 'grey.600' }} />
                <Typography variant="h6" color="grey.700">
                  Disconnected
                </Typography>
              </Box>
              <Typography variant="h3" color="grey.700">
                {healthSummary.disconnected}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Device Health Table */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Device Status Details
          </Typography>
          <TableContainer component={Paper} elevation={0}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Status</TableCell>
                  <TableCell>Device Name</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Enabled</TableCell>
                  <TableCell>Rules</TableCell>
                  <TableCell>Last Tested</TableCell>
                  <TableCell>Last Sync</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {devices.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={8} align="center">
                      <Typography color="text.secondary" py={3}>
                        No devices configured. Add a device to get started.
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  devices.map((device) => (
                    <TableRow key={device.id} hover>
                      <TableCell>
                        <Tooltip title={device.connection_status}>
                          {getStatusIcon(device.connection_status)}
                        </Tooltip>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" fontWeight="medium">
                          {device.name}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip label={device.type.toUpperCase()} size="small" />
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={device.enabled ? 'Yes' : 'No'}
                          size="small"
                          color={device.enabled ? 'success' : 'default'}
                        />
                      </TableCell>
                      <TableCell>
                        <Chip label={device.rules_count} size="small" variant="outlined" />
                      </TableCell>
                      <TableCell>
                        <Tooltip title={device.last_tested || 'Never tested'}>
                          <Typography variant="body2" color="text.secondary">
                            {formatTimestamp(device.last_tested)}
                          </Typography>
                        </Tooltip>
                      </TableCell>
                      <TableCell>
                        <Tooltip title={device.last_sync || 'Never synced'}>
                          <Typography variant="body2" color="text.secondary">
                            {formatTimestamp(device.last_sync)}
                          </Typography>
                        </Tooltip>
                      </TableCell>
                      <TableCell align="right">
                        <Tooltip title="Test Connection">
                          <IconButton
                            size="small"
                            onClick={() => handleTestConnection(device.id)}
                            disabled={testingDevice === device.id}
                          >
                            {testingDevice === device.id ? (
                              <CircularProgress size={20} />
                            ) : (
                              <Cable />
                            )}
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="View Details">
                          <IconButton size="small" href={`/devices`}>
                            <Info />
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Additional Info */}
      <Box mt={3}>
        <Alert severity="info">
          <Typography variant="body2">
            <strong>Health Dashboard Tips:</strong>
            <br />
            • Green (Connected): Device is online and responding to API calls
            <br />
            • Red (Error): Device connection failed - check credentials and network
            <br />
            • Gray (Disconnected): Device hasn't been tested yet
            <br />• Use "Test Connection" to verify device status
          </Typography>
        </Alert>
      </Box>
    </Box>
  );
};

export default DeviceHealth;
