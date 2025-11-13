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
  Tabs,
  Tab,
  Switch,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Visibility as ViewIcon,
  Edit as EditIcon,
} from '@mui/icons-material';
import api from '../services/api';
import { format } from 'date-fns';

const Rules = () => {
  const [rules, setRules] = useState([]);
  const [filteredRules, setFilteredRules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tabValue, setTabValue] = useState(0);
  const [selectedRule, setSelectedRule] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    fetchRules();
  }, []);

  useEffect(() => {
    filterRules();
  }, [tabValue, rules]);

  const fetchRules = async () => {
    try {
      setLoading(true);
      const response = await api.get('/rules');
      setRules(response.data.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load rules');
    } finally {
      setLoading(false);
    }
  };

  const filterRules = () => {
    if (tabValue === 0) {
      setFilteredRules(rules);
    } else if (tabValue === 1) {
      setFilteredRules(rules.filter(r => r.id.startsWith('PA-')));
    } else if (tabValue === 2) {
      setFilteredRules(rules.filter(r => r.id.startsWith('EA-')));
    }
  };

  const handleToggleRule = async (ruleId) => {
    try {
      await api.post(`/rules/${ruleId}/toggle`);
      await fetchRules();
    } catch (err) {
      console.error('Toggle failed:', err);
    }
  };

  const handleViewRule = (rule) => {
    setSelectedRule(rule);
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setSelectedRule(null);
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
            Detection Rules
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Manage security detection rules across all devices
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<RefreshIcon />}
          onClick={fetchRules}
        >
          Refresh
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Paper sx={{ mb: 2 }}>
        <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)}>
          <Tab label={`All Rules (${rules.length})`} />
          <Tab label={`Palo Alto (${rules.filter(r => r.id.startsWith('PA-')).length})`} />
          <Tab label={`EntraID (${rules.filter(r => r.id.startsWith('EA-')).length})`} />
        </Tabs>
      </Paper>

      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Rule ID</TableCell>
                <TableCell>Use Case</TableCell>
                <TableCell>Detection Rule</TableCell>
                <TableCell>Severity</TableCell>
                <TableCell>MITRE Technique</TableCell>
                <TableCell>Enabled</TableCell>
                <TableCell align="center">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredRules.map((rule) => (
                <TableRow key={rule.id} hover>
                  <TableCell>
                    <Chip label={rule.id} size="small" />
                  </TableCell>
                  <TableCell>{rule.useCase}</TableCell>
                  <TableCell>
                    <Typography variant="body2" noWrap sx={{ maxWidth: 300 }}>
                      {rule.detectionRule}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={rule.severity}
                      size="small"
                      color={
                        rule.severity === 'Critical' ? 'error' :
                        rule.severity === 'High' ? 'warning' :
                        rule.severity === 'Medium' ? 'info' : 'default'
                      }
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="caption">{rule.mitreTechnique}</Typography>
                  </TableCell>
                  <TableCell>
                    <Switch
                      checked={rule.enabled}
                      onChange={() => handleToggleRule(rule.id)}
                      color="primary"
                    />
                  </TableCell>
                  <TableCell align="center">
                    <IconButton
                      color="primary"
                      onClick={() => handleViewRule(rule)}
                    >
                      <ViewIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Rule Details Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        {selectedRule && (
          <>
            <DialogTitle>
              Rule Details - {selectedRule.id}
            </DialogTitle>
            <DialogContent>
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" gutterBottom>Use Case</Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>{selectedRule.useCase}</Typography>

                <Typography variant="subtitle2" gutterBottom>Detection Rule</Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>{selectedRule.detectionRule}</Typography>

                <Typography variant="subtitle2" gutterBottom>Incident Rule</Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>{selectedRule.incidentRule}</Typography>

                <Typography variant="subtitle2" gutterBottom>MITRE ATT&CK</Typography>
                <Box sx={{ mb: 2 }}>
                  <Chip label={selectedRule.mitreTactic} size="small" sx={{ mr: 1 }} />
                  <Chip label={selectedRule.mitreTechnique} size="small" />
                </Box>

                <Typography variant="subtitle2" gutterBottom>CQL Query</Typography>
                <TextField
                  multiline
                  rows={10}
                  fullWidth
                  value={selectedRule.cqlQuery}
                  InputProps={{ readOnly: true }}
                  sx={{ fontFamily: 'monospace', fontSize: '0.875rem' }}
                />

                <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                  <Typography variant="caption">
                    Created: {format(new Date(selectedRule.createdAt), 'PPpp')}
                  </Typography>
                  <Typography variant="caption">
                    Modified: {format(new Date(selectedRule.lastModified), 'PPpp')}
                  </Typography>
                </Box>
              </Box>
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseDialog}>Close</Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Box>
  );
};

export default Rules;
