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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Visibility as ViewIcon,
  Edit as EditIcon,
} from '@mui/icons-material';
import api from '../services/api';
import { format } from 'date-fns';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [newStatus, setNewStatus] = useState('');
  const [comment, setComment] = useState('');

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      const response = await api.get('/alerts');
      setAlerts(response.data.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load alerts');
    } finally {
      setLoading(false);
    }
  };

  const handleViewAlert = (alert) => {
    setSelectedAlert(alert);
    setNewStatus(alert.status);
    setComment('');
    setDialogOpen(true);
  };

  const handleUpdateStatus = async () => {
    try {
      await api.put(`/alerts/${selectedAlert.id}/status`, {
        status: newStatus,
        comment: comment
      });
      await fetchAlerts();
      handleCloseDialog();
    } catch (err) {
      console.error('Update failed:', err);
    }
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setSelectedAlert(null);
    setNewStatus('');
    setComment('');
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'open': return 'error';
      case 'investigating': return 'warning';
      case 'resolved': return 'success';
      case 'false_positive': return 'default';
      default: return 'default';
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'Critical': return 'error';
      case 'High': return 'warning';
      case 'Medium': return 'info';
      case 'Low': return 'default';
      default: return 'default';
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
            Security Alerts
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Monitor and manage security alerts from all detection rules
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<RefreshIcon />}
          onClick={fetchAlerts}
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
                <TableCell>Alert ID</TableCell>
                <TableCell>Rule Name</TableCell>
                <TableCell>Severity</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Source IP</TableCell>
                <TableCell>Destination IP</TableCell>
                <TableCell>User</TableCell>
                <TableCell>Detected At</TableCell>
                <TableCell align="center">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {alerts.map((alert) => (
                <TableRow key={alert.id} hover>
                  <TableCell>
                    <Chip label={alert.id} size="small" />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" noWrap sx={{ maxWidth: 200 }}>
                      {alert.ruleName}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={alert.severity}
                      size="small"
                      color={getSeverityColor(alert.severity)}
                    />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={alert.status}
                      size="small"
                      color={getStatusColor(alert.status)}
                      variant="outlined"
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="caption">{alert.sourceIp}</Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="caption">{alert.destIp}</Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="caption" noWrap sx={{ maxWidth: 150 }}>
                      {alert.userName}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="caption">
                      {format(new Date(alert.detectedAt), 'PPp')}
                    </Typography>
                  </TableCell>
                  <TableCell align="center">
                    <IconButton
                      color="primary"
                      onClick={() => handleViewAlert(alert)}
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

      {/* Alert Details Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        {selectedAlert && (
          <>
            <DialogTitle>
              Alert Details - {selectedAlert.id}
            </DialogTitle>
            <DialogContent>
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" gutterBottom>Rule</Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>{selectedAlert.ruleName}</Typography>

                <Typography variant="subtitle2" gutterBottom>Severity</Typography>
                <Chip
                  label={selectedAlert.severity}
                  size="small"
                  color={getSeverityColor(selectedAlert.severity)}
                  sx={{ mb: 2 }}
                />

                <Typography variant="subtitle2" gutterBottom>Network Information</Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>
                  Source IP: {selectedAlert.sourceIp}<br />
                  Destination IP: {selectedAlert.destIp}<br />
                  User: {selectedAlert.userName}<br />
                  Device: {selectedAlert.deviceName}
                </Typography>

                <Typography variant="subtitle2" gutterBottom>MITRE ATT&CK</Typography>
                <Box sx={{ mb: 2 }}>
                  <Chip label={selectedAlert.mitreTactic} size="small" sx={{ mr: 1 }} />
                  <Chip label={selectedAlert.mitreTechnique} size="small" />
                </Box>

                <Typography variant="subtitle2" gutterBottom>Detection Time</Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>
                  {format(new Date(selectedAlert.detectedAt), 'PPpp')}
                </Typography>

                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel>Status</InputLabel>
                  <Select
                    value={newStatus}
                    onChange={(e) => setNewStatus(e.target.value)}
                    label="Status"
                  >
                    <MenuItem value="open">Open</MenuItem>
                    <MenuItem value="investigating">Investigating</MenuItem>
                    <MenuItem value="resolved">Resolved</MenuItem>
                    <MenuItem value="false_positive">False Positive</MenuItem>
                  </Select>
                </FormControl>

                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  label="Comment"
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  placeholder="Add a comment about this alert..."
                />
              </Box>
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseDialog}>Cancel</Button>
              <Button
                onClick={handleUpdateStatus}
                variant="contained"
                disabled={!newStatus}
              >
                Update Status
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Box>
  );
};

export default Alerts;
