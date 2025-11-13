/**
 * Devices management page
 */
import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  IconButton,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  CircularProgress,
  Grid,
  FormControlLabel,
  Switch,
} from '@mui/material';
import {
  Add,
  Edit,
  Delete,
  Cable,
  CheckCircle,
  Error,
  Circle,
  Sync,
} from '@mui/icons-material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { deviceAPI } from '../services/api';
import type { Device } from '../types';

const Devices: React.FC = () => {
  const [devices, setDevices] = useState<Device[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [openDialog, setOpenDialog] = useState(false);
  const [editingDevice, setEditingDevice] = useState<Device | null>(null);
  const [testingDevice, setTestingDevice] = useState<string | null>(null);
  const [syncingDevice, setSyncingDevice] = useState<string | null>(null);
  
  // Form state
  const [formData, setFormData] = useState({
    name: '',
    type: 'paloalto',
    enabled: true,
    config: {
      api_url: '',
      api_key: '',
      username: '',
      password: '',
      tenant_id: '',
      client_id: '',
      client_secret: '',
    },
  });

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
    }
  };

  const handleOpenDialog = (device?: Device) => {
    if (device) {
      setEditingDevice(device);
      setFormData({
        name: device.name,
        type: device.type,
        enabled: device.enabled,
        config: device.config,
      });
    } else {
      setEditingDevice(null);
      setFormData({
        name: '',
        type: 'paloalto',
        enabled: true,
        config: {
          api_url: '',
          api_key: '',
          username: '',
          password: '',
          tenant_id: '',
          client_id: '',
          client_secret: '',
        },
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingDevice(null);
  };

  const handleSave = async () => {
    try {
      setError('');
      if (editingDevice) {
        await deviceAPI.update(editingDevice.id, formData);
      } else {
        await deviceAPI.create(formData);
      }
      handleCloseDialog();
      await loadDevices();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save device');
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this device?')) {
      return;
    }
    
    try {
      setError('');
      await deviceAPI.delete(id);
      await loadDevices();
    } catch (err: any) {
      setError('Failed to delete device');
    }
  };

  const handleTestConnection = async (id: string) => {
    try {
      setTestingDevice(id);
      setError('');
      const result = await deviceAPI.testConnection(id);
      if (result.success) {
        alert(`Connection successful!\n\n${result.message}`);
      } else {
        alert(`Connection failed!\n\n${result.message}`);
      }
      await loadDevices();
    } catch (err: any) {
      setError('Failed to test connection');
    } finally {
      setTestingDevice(null);
    }
  };

  const handleSyncDevice = async (id: string) => {
    try {
      setSyncingDevice(id);
      setError('');
      const result = await deviceAPI.sync(id);
      if (result.success) {
        alert(
          `Sync successful!\n\n${result.message}\n\nRules Created: ${result.rules_created}\nRules Updated: ${result.rules_updated}\nTotal Synced: ${result.rules_synced}`
        );
      } else {
        alert(`Sync failed!\n\n${result.message}`);
      }
      await loadDevices();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to sync device');
    } finally {
      setSyncingDevice(null);
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

  const columns: GridColDef[] = [
    {
      field: 'status',
      headerName: 'Status',
      width: 100,
      renderCell: (params) => (
        <Box display="flex" alignItems="center">
          {getStatusIcon(params.row.connection_status)}
        </Box>
      ),
    },
    { field: 'name', headerName: 'Name', flex: 1 },
    {
      field: 'type',
      headerName: 'Type',
      width: 120,
      renderCell: (params) => (
        <Chip label={params.value.toUpperCase()} size="small" />
      ),
    },
    {
      field: 'enabled',
      headerName: 'Enabled',
      width: 100,
      renderCell: (params) => (
        <Chip
          label={params.value ? 'Yes' : 'No'}
          size="small"
          color={params.value ? 'success' : 'default'}
        />
      ),
    },
    { field: 'rules_count', headerName: 'Rules', width: 80 },
    {
      field: 'last_tested',
      headerName: 'Last Tested',
      width: 160,
      valueFormatter: (params) =>
        params.value ? new Date(params.value).toLocaleString() : 'Never',
    },
    {
      field: 'last_sync',
      headerName: 'Last Sync',
      width: 160,
      valueFormatter: (params) =>
        params.value ? new Date(params.value).toLocaleString() : 'Never',
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 250,
      sortable: false,
      renderCell: (params) => (
        <Box>
          <IconButton
            size="small"
            onClick={() => handleTestConnection(params.row.id)}
            disabled={testingDevice === params.row.id}
            title="Test Connection"
          >
            {testingDevice === params.row.id ? (
              <CircularProgress size={20} />
            ) : (
              <Cable />
            )}
          </IconButton>
          <IconButton
            size="small"
            onClick={() => handleSyncDevice(params.row.id)}
            disabled={syncingDevice === params.row.id || !params.row.enabled}
            title="Sync Now"
            color="primary"
          >
            {syncingDevice === params.row.id ? (
              <CircularProgress size={20} />
            ) : (
              <Sync />
            )}
          </IconButton>
          <IconButton
            size="small"
            onClick={() => handleOpenDialog(params.row)}
            title="Edit"
          >
            <Edit />
          </IconButton>
          <IconButton
            size="small"
            onClick={() => handleDelete(params.row.id)}
            title="Delete"
          >
            <Delete />
          </IconButton>
        </Box>
      ),
    },
  ];

  const renderConfigFields = () => {
    switch (formData.type) {
      case 'paloalto':
        return (
          <>
            <TextField
              fullWidth
              label="API URL"
              value={formData.config.api_url || ''}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  config: { ...formData.config, api_url: e.target.value },
                })
              }
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="API Key"
              type="password"
              value={formData.config.api_key || ''}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  config: { ...formData.config, api_key: e.target.value },
                })
              }
              margin="normal"
              required
            />
          </>
        );
      case 'entraid':
        return (
          <>
            <TextField
              fullWidth
              label="Tenant ID"
              value={formData.config.tenant_id || ''}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  config: { ...formData.config, tenant_id: e.target.value },
                })
              }
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Client ID"
              value={formData.config.client_id || ''}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  config: { ...formData.config, client_id: e.target.value },
                })
              }
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Client Secret"
              type="password"
              value={formData.config.client_secret || ''}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  config: { ...formData.config, client_secret: e.target.value },
                })
              }
              margin="normal"
              required
            />
          </>
        );
      case 'siem':
        return (
          <>
            <TextField
              fullWidth
              label="API URL"
              value={formData.config.api_url || ''}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  config: { ...formData.config, api_url: e.target.value },
                })
              }
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Username"
              value={formData.config.username || ''}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  config: { ...formData.config, username: e.target.value },
                })
              }
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Password"
              type="password"
              value={formData.config.password || ''}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  config: { ...formData.config, password: e.target.value },
                })
              }
              margin="normal"
              required
            />
          </>
        );
      default:
        return null;
    }
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Devices
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Manage your security device integrations
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
        >
          Add Device
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Card>
        <CardContent>
          <DataGrid
            rows={devices}
            columns={columns}
            autoHeight
            pageSizeOptions={[10, 25, 50]}
            initialState={{
              pagination: { paginationModel: { pageSize: 10 } },
            }}
            disableRowSelectionOnClick
          />
        </CardContent>
      </Card>

      {/* Add/Edit Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingDevice ? 'Edit Device' : 'Add New Device'}
        </DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Device Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            margin="normal"
            required
          />
          <FormControl fullWidth margin="normal" required>
            <InputLabel>Device Type</InputLabel>
            <Select
              value={formData.type}
              label="Device Type"
              onChange={(e) =>
                setFormData({ ...formData, type: e.target.value as any })
              }
              disabled={!!editingDevice}
            >
              <MenuItem value="paloalto">Palo Alto NGFW</MenuItem>
              <MenuItem value="entraid">Microsoft EntraID</MenuItem>
              <MenuItem value="siem">SIEM (Elastic/Splunk)</MenuItem>
            </Select>
          </FormControl>

          {renderConfigFields()}

          <FormControlLabel
            control={
              <Switch
                checked={formData.enabled}
                onChange={(e) =>
                  setFormData({ ...formData, enabled: e.target.checked })
                }
              />
            }
            label="Enabled"
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSave} variant="contained">
            {editingDevice ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Devices;
