/**
 * Rules management page
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
  FormControlLabel,
  Switch,
  Grid,
} from '@mui/material';
import {
  Add,
  Edit,
  Delete,
  ToggleOn,
  ToggleOff,
} from '@mui/icons-material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { deviceAPI, ruleAPI } from '../services/api';
import type { Device, Rule } from '../types';

const Rules: React.FC = () => {
  const [rules, setRules] = useState<Rule[]>([]);
  const [devices, setDevices] = useState<Device[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [openDialog, setOpenDialog] = useState(false);
  const [editingRule, setEditingRule] = useState<Rule | null>(null);
  
  // Form state
  const [formData, setFormData] = useState({
    id: '',
    device_id: '',
    use_case_id: '',
    name: '',
    description: '',
    incident_rule: '',
    severity: 'Medium',
    mitre_tactic: '',
    mitre_technique: '',
    category: '',
    query: '',
    enabled: true,
    status: 'draft',
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setError('');
      const [rulesData, devicesData] = await Promise.all([
        ruleAPI.list(),
        deviceAPI.list(),
      ]);
      setRules(rulesData);
      setDevices(devicesData);
    } catch (err: any) {
      setError('Failed to load data');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpenDialog = (rule?: Rule) => {
    if (rule) {
      setEditingRule(rule);
      setFormData({
        id: rule.id,
        device_id: rule.device_id,
        use_case_id: rule.use_case_id || '',
        name: rule.name,
        description: rule.description || '',
        incident_rule: rule.incident_rule || '',
        severity: rule.severity,
        mitre_tactic: rule.mitre_tactic || '',
        mitre_technique: rule.mitre_technique || '',
        category: rule.category || '',
        query: rule.query,
        enabled: rule.enabled,
        status: rule.status,
      });
    } else {
      setEditingRule(null);
      setFormData({
        id: '',
        device_id: devices.length > 0 ? devices[0].id : '',
        use_case_id: '',
        name: '',
        description: '',
        incident_rule: '',
        severity: 'Medium',
        mitre_tactic: '',
        mitre_technique: '',
        category: '',
        query: '',
        enabled: true,
        status: 'draft',
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingRule(null);
  };

  const handleSave = async () => {
    try {
      setError('');
      if (editingRule) {
        await ruleAPI.update(editingRule.id, formData);
      } else {
        await ruleAPI.create(formData);
      }
      handleCloseDialog();
      await loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save rule');
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this rule?')) {
      return;
    }
    
    try {
      setError('');
      await ruleAPI.delete(id);
      await loadData();
    } catch (err: any) {
      setError('Failed to delete rule');
    }
  };

  const handleToggleStatus = async (id: string, currentEnabled: boolean) => {
    try {
      setError('');
      await ruleAPI.toggleStatus(id, !currentEnabled);
      await loadData();
    } catch (err: any) {
      setError('Failed to toggle rule status');
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'Critical':
        return 'error';
      case 'High':
        return 'warning';
      case 'Medium':
        return 'info';
      case 'Low':
        return 'success';
      default:
        return 'default';
    }
  };

  const getDeviceName = (deviceId: string) => {
    const device = devices.find((d) => d.id === deviceId);
    return device ? device.name : 'Unknown';
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 120 },
    { field: 'name', headerName: 'Name', flex: 1 },
    {
      field: 'device_id',
      headerName: 'Device',
      width: 200,
      valueFormatter: (params) => getDeviceName(params.value),
    },
    {
      field: 'severity',
      headerName: 'Severity',
      width: 100,
      renderCell: (params) => (
        <Chip
          label={params.value}
          size="small"
          color={getSeverityColor(params.value) as any}
        />
      ),
    },
    {
      field: 'mitre_technique',
      headerName: 'MITRE',
      width: 100,
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 100,
      renderCell: (params) => (
        <Chip label={params.value} size="small" />
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
    { field: 'detection_count', headerName: 'Detections', width: 100 },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      renderCell: (params) => (
        <Box>
          <IconButton
            size="small"
            onClick={() => handleToggleStatus(params.row.id, params.row.enabled)}
            title={params.row.enabled ? 'Disable' : 'Enable'}
          >
            {params.row.enabled ? <ToggleOn /> : <ToggleOff />}
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
            Detection Rules
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Manage your security detection rules
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
          disabled={devices.length === 0}
        >
          Add Rule
        </Button>
      </Box>

      {devices.length === 0 && (
        <Alert severity="info" sx={{ mb: 2 }}>
          Please add at least one device before creating rules.
        </Alert>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Card>
        <CardContent>
          <DataGrid
            rows={rules}
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
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingRule ? 'Edit Rule' : 'Add New Rule'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Rule ID"
                value={formData.id}
                onChange={(e) => setFormData({ ...formData, id: e.target.value })}
                margin="normal"
                required
                disabled={!!editingRule}
                helperText="e.g., ENTRAID-001, PALOALTO-001"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth margin="normal" required>
                <InputLabel>Device</InputLabel>
                <Select
                  value={formData.device_id}
                  label="Device"
                  onChange={(e) =>
                    setFormData({ ...formData, device_id: e.target.value })
                  }
                  disabled={!!editingRule}
                >
                  {devices.map((device) => (
                    <MenuItem key={device.id} value={device.id}>
                      {device.name} ({device.type})
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Rule Name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                margin="normal"
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                margin="normal"
                multiline
                rows={2}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Incident Rule"
                value={formData.incident_rule}
                onChange={(e) =>
                  setFormData({ ...formData, incident_rule: e.target.value })
                }
                margin="normal"
                multiline
                rows={2}
                helperText="Correlation logic for creating incidents"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth margin="normal" required>
                <InputLabel>Severity</InputLabel>
                <Select
                  value={formData.severity}
                  label="Severity"
                  onChange={(e) =>
                    setFormData({ ...formData, severity: e.target.value })
                  }
                >
                  <MenuItem value="Critical">Critical</MenuItem>
                  <MenuItem value="High">High</MenuItem>
                  <MenuItem value="Medium">Medium</MenuItem>
                  <MenuItem value="Low">Low</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth margin="normal">
                <InputLabel>Status</InputLabel>
                <Select
                  value={formData.status}
                  label="Status"
                  onChange={(e) =>
                    setFormData({ ...formData, status: e.target.value as any })
                  }
                >
                  <MenuItem value="draft">Draft</MenuItem>
                  <MenuItem value="testing">Testing</MenuItem>
                  <MenuItem value="active">Active</MenuItem>
                  <MenuItem value="disabled">Disabled</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="MITRE Tactic"
                value={formData.mitre_tactic}
                onChange={(e) =>
                  setFormData({ ...formData, mitre_tactic: e.target.value })
                }
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="MITRE Technique"
                value={formData.mitre_technique}
                onChange={(e) =>
                  setFormData({ ...formData, mitre_technique: e.target.value })
                }
                margin="normal"
                helperText="e.g., T1110"
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Category"
                value={formData.category}
                onChange={(e) =>
                  setFormData({ ...formData, category: e.target.value })
                }
                margin="normal"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Query"
                value={formData.query}
                onChange={(e) => setFormData({ ...formData, query: e.target.value })}
                margin="normal"
                multiline
                rows={4}
                required
                helperText="CQL detection query template"
              />
            </Grid>
            <Grid item xs={12}>
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
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSave} variant="contained">
            {editingRule ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Rules;
