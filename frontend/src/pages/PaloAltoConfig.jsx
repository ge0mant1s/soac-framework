import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  Button,
  Divider,
  Chip,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import {
  Security as SecurityIcon,
  CheckCircle as CheckCircleIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import api from '../services/api';
import { format } from 'date-fns';

const PaloAltoConfig = () => {
  const [rules, setRules] = useState([]);
  const [device, setDevice] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Fetch Palo Alto rules
      const rulesResponse = await api.get('/rules?type=paloalto');
      setRules(rulesResponse.data.data);
      
      // Fetch device info
      const devicesResponse = await api.get('/devices');
      const paloAltoDevice = devicesResponse.data.data.find(
        d => d.type === 'paloalto_ngfw'
      );
      setDevice(paloAltoDevice);
      
      setError(null);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load configuration');
    } finally {
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

  const enabledRules = rules.filter(r => r.enabled);
  const rulesBySeverity = {
    critical: rules.filter(r => r.severity === 'Critical').length,
    high: rules.filter(r => r.severity === 'High').length,
    medium: rules.filter(r => r.severity === 'Medium').length,
    low: rules.filter(r => r.severity === 'Low').length,
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Palo Alto NGFW Configuration
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Manage and monitor Palo Alto Next-Generation Firewall integration
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<RefreshIcon />}
          onClick={fetchData}
        >
          Refresh
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Device Status */}
      {device && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Box display="flex" alignItems="center" sx={{ mb: 2 }}>
            <SecurityIcon sx={{ fontSize: 40, mr: 2, color: 'primary.main' }} />
            <Box>
              <Typography variant="h5">{device.name}</Typography>
              <Typography variant="body2" color="text.secondary">
                {device.description}
              </Typography>
            </Box>
          </Box>
          <Divider sx={{ my: 2 }} />
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="caption" color="text.secondary">Status</Typography>
              <Box display="flex" alignItems="center" sx={{ mt: 1 }}>
                <CheckCircleIcon color="success" sx={{ mr: 1 }} />
                <Typography variant="body1">{device.status}</Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="caption" color="text.secondary">IP Address</Typography>
              <Typography variant="body1" sx={{ mt: 1 }}>{device.ipAddress}</Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="caption" color="text.secondary">Last Sync</Typography>
              <Typography variant="body1" sx={{ mt: 1 }}>
                {format(new Date(device.lastSync), 'PPp')}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="caption" color="text.secondary">Rules Count</Typography>
              <Typography variant="body1" sx={{ mt: 1 }}>{device.rulesCount}</Typography>
            </Grid>
          </Grid>
        </Paper>
      )}

      {/* Statistics */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Rules
              </Typography>
              <Typography variant="h3">{rules.length}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Enabled Rules
              </Typography>
              <Typography variant="h3" color="success.main">{enabledRules.length}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Critical Rules
              </Typography>
              <Typography variant="h3" color="error.main">{rulesBySeverity.critical}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                High Priority
              </Typography>
              <Typography variant="h3" color="warning.main">{rulesBySeverity.high}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Rules by Use Case */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Detection Rules by Use Case
        </Typography>
        <Divider sx={{ mb: 2 }} />
        <List>
          {rules.map((rule) => (
            <ListItem
              key={rule.id}
              sx={{
                border: '1px solid',
                borderColor: 'divider',
                borderRadius: 1,
                mb: 1,
              }}
            >
              <ListItemText
                primary={
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Box>
                      <Typography variant="subtitle1">{rule.useCase}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        {rule.detectionRule}
                      </Typography>
                    </Box>
                    <Box display="flex" gap={1}>
                      <Chip
                        label={rule.severity}
                        size="small"
                        color={
                          rule.severity === 'Critical' ? 'error' :
                          rule.severity === 'High' ? 'warning' :
                          rule.severity === 'Medium' ? 'info' : 'default'
                        }
                      />
                      <Chip
                        label={rule.enabled ? 'Enabled' : 'Disabled'}
                        size="small"
                        color={rule.enabled ? 'success' : 'default'}
                        variant="outlined"
                      />
                    </Box>
                  </Box>
                }
                secondary={
                  <Box sx={{ mt: 1 }}>
                    <Chip label={rule.mitreTactic} size="small" sx={{ mr: 1 }} />
                    <Chip label={rule.mitreTechnique} size="small" />
                  </Box>
                }
              />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Box>
  );
};

export default PaloAltoConfig;
