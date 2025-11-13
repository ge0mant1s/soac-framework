import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  CircularProgress,
  Alert,
  Button,
  Tooltip,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Sync as SyncIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';
import api from '../services/api';
import { format } from 'date-fns';

const Devices = () => {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [syncing, setSyncing] = useState({});

  useEffect(() => {
    fetchDevices();
  }, []);

  const fetchDevices = async () => {
    try {
      setLoading(true);
      const response = await api.get('/devices');
      setDevices(response.data.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load devices');
    } finally {
      setLoading(false);
    }
  };

  const handleSync = async (deviceId) => {
    try {
      setSyncing({ ...syncing, [deviceId]: true });
      await api.post(`/devices/${deviceId}/sync`);
      await fetchDevices();
      setSyncing({ ...syncing, [deviceId]: false });
    } catch (err) {
      console.error('Sync failed:', err);
      setSyncing({ ...syncing, [deviceId]: false });
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Device Management
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Manage and monitor connected security devices
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<RefreshIcon />}
          onClick={fetchDevices}
        >
          Refresh
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Device Name</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>IP Address</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Rules Count</TableCell>
                <TableCell>Last Sync</TableCell>
                <TableCell align="center">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {devices.map((device) => (
                <TableRow key={device.id} hover>
                  <TableCell>
                    <Typography variant="subtitle2">{device.name}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {device.description}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={device.type}
                      size="small"
                      variant="outlined"
                    />
                  </TableCell>
                  <TableCell>{device.ipAddress}</TableCell>
                  <TableCell>
                    <Chip
                      icon={<CheckCircleIcon />}
                      label={device.status}
                      size="small"
                      color={device.status === 'active' ? 'success' : 'default'}
                    />
                  </TableCell>
                  <TableCell>{device.rulesCount}</TableCell>
                  <TableCell>
                    <Typography variant="caption">
                      {format(new Date(device.lastSync), 'PPpp')}
                    </Typography>
                  </TableCell>
                  <TableCell align="center">
                    <Tooltip title="Sync Rules">
                      <IconButton
                        color="primary"
                        onClick={() => handleSync(device.id)}
                        disabled={syncing[device.id]}
                      >
                        {syncing[device.id] ? (
                          <CircularProgress size={24} />
                        ) : (
                          <SyncIcon />
                        )}
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
};

export default Devices;
