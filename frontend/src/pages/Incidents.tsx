/**
 * Incidents page - View and manage security incidents
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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Tooltip,
  Stack,
} from '@mui/material';
import {
  Visibility,
  PlayArrow,
  CheckCircle,
  Error,
  Warning,
  Info,
  Person,
  Timeline,
  Refresh,
} from '@mui/icons-material';
import axios from 'axios';

interface Incident {
  incident_id: string;
  pattern_id: string;
  pattern_name: string;
  entity_key: string;
  phases_matched: string[];
  confidence_level: string;
  event_count: number;
  severity: string;
  status: string;
  assigned_to: string | null;
  created_at: string;
  updated_at: string;
  events?: any[];
}

interface IncidentStats {
  total_incidents: number;
  recent_incidents_24h: number;
  by_status: Record<string, number>;
  by_severity: Record<string, number>;
}

const Incidents: React.FC = () => {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [stats, setStats] = useState<IncidentStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Filters
  const [statusFilter, setStatusFilter] = useState('');
  const [severityFilter, setSeverityFilter] = useState('');
  const [daysFilter, setDaysFilter] = useState(7);
  
  // Detail dialog
  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null);
  const [detailDialogOpen, setDetailDialogOpen] = useState(false);
  
  // Assign dialog
  const [assignDialogOpen, setAssignDialogOpen] = useState(false);
  const [assignAnalyst, setAssignAnalyst] = useState('');
  const [assigningIncident, setAssigningIncident] = useState<Incident | null>(null);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, [statusFilter, severityFilter, daysFilter]);

  const loadData = async () => {
    try {
      setError('');
      const token = localStorage.getItem('token');
      
      // Build query parameters
      const params: any = { days: daysFilter, limit: 100 };
      if (statusFilter) params.status = statusFilter;
      if (severityFilter) params.severity = severityFilter;
      
      // Load incidents
      const incidentsResponse = await axios.get('/api/v1/incidents/', {
        headers: { Authorization: `Bearer ${token}` },
        params,
      });
      
      // Load stats
      const statsResponse = await axios.get('/api/v1/incidents/stats/summary', {
        headers: { Authorization: `Bearer ${token}` },
        params: { days: daysFilter },
      });
      
      setIncidents(incidentsResponse.data.incidents || []);
      setStats(statsResponse.data);
    } catch (err: any) {
      console.error('Error loading incidents:', err);
      setError(err.response?.data?.detail || 'Failed to load incidents');
    } finally {
      setIsLoading(false);
    }
  };

  const handleViewDetails = async (incident: Incident) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`/api/v1/incidents/${incident.incident_id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setSelectedIncident(response.data);
      setDetailDialogOpen(true);
    } catch (err: any) {
      setError('Failed to load incident details');
    }
  };

  const handleUpdateStatus = async (incidentId: string, newStatus: string) => {
    try {
      const token = localStorage.getItem('token');
      await axios.patch(
        `/api/v1/incidents/${incidentId}`,
        { status: newStatus },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      loadData();
      if (selectedIncident?.incident_id === incidentId) {
        setSelectedIncident({ ...selectedIncident, status: newStatus });
      }
    } catch (err: any) {
      setError('Failed to update incident status');
    }
  };

  const handleAssignIncident = async () => {
    if (!assigningIncident || !assignAnalyst) return;
    
    try {
      const token = localStorage.getItem('token');
      await axios.post(
        `/api/v1/incidents/${assigningIncident.incident_id}/assign`,
        { analyst: assignAnalyst },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setAssignDialogOpen(false);
      setAssignAnalyst('');
      loadData();
    } catch (err: any) {
      setError('Failed to assign incident');
    }
  };

  const handleExecutePlaybook = async (incidentId: string) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(
        `/api/v1/incidents/${incidentId}/execute-playbook`,
        { mode: 'manual' },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('Playbooks executed successfully');
      loadData();
    } catch (err: any) {
      setError('Failed to execute playbooks');
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity?.toLowerCase()) {
      case 'critical':
        return 'error';
      case 'high':
        return 'warning';
      case 'medium':
        return 'info';
      default:
        return 'default';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'open':
        return 'error';
      case 'investigating':
        return 'warning';
      case 'contained':
        return 'info';
      case 'resolved':
        return 'success';
      case 'false_positive':
        return 'default';
      default:
        return 'default';
    }
  };

  const getConfidenceColor = (confidence: string) => {
    switch (confidence?.toLowerCase()) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'info';
      default:
        return 'default';
    }
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1">
          Security Incidents
        </Typography>
        <IconButton onClick={loadData} color="primary">
          <Refresh />
        </IconButton>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {/* Stats Cards */}
      {stats && (
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Error color="error" sx={{ mr: 1 }} />
                  <Typography variant="h6">{stats.total_incidents}</Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Total Incidents ({daysFilter}d)
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Warning color="warning" sx={{ mr: 1 }} />
                  <Typography variant="h6">{stats.recent_incidents_24h}</Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Last 24 Hours
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Timeline color="info" sx={{ mr: 1 }} />
                  <Typography variant="h6">{stats.by_status.investigating || 0}</Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Under Investigation
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <CheckCircle color="success" sx={{ mr: 1 }} />
                  <Typography variant="h6">{stats.by_status.resolved || 0}</Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Resolved
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth size="small">
                <InputLabel>Status</InputLabel>
                <Select
                  value={statusFilter}
                  label="Status"
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <MenuItem value="">All</MenuItem>
                  <MenuItem value="open">Open</MenuItem>
                  <MenuItem value="investigating">Investigating</MenuItem>
                  <MenuItem value="contained">Contained</MenuItem>
                  <MenuItem value="resolved">Resolved</MenuItem>
                  <MenuItem value="false_positive">False Positive</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth size="small">
                <InputLabel>Severity</InputLabel>
                <Select
                  value={severityFilter}
                  label="Severity"
                  onChange={(e) => setSeverityFilter(e.target.value)}
                >
                  <MenuItem value="">All</MenuItem>
                  <MenuItem value="Critical">Critical</MenuItem>
                  <MenuItem value="High">High</MenuItem>
                  <MenuItem value="Medium">Medium</MenuItem>
                  <MenuItem value="Low">Low</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth size="small">
                <InputLabel>Time Range</InputLabel>
                <Select
                  value={daysFilter}
                  label="Time Range"
                  onChange={(e) => setDaysFilter(Number(e.target.value))}
                >
                  <MenuItem value={1}>Last 24 hours</MenuItem>
                  <MenuItem value={7}>Last 7 days</MenuItem>
                  <MenuItem value={30}>Last 30 days</MenuItem>
                  <MenuItem value={90}>Last 90 days</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Incidents Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Incident ID</TableCell>
              <TableCell>Pattern</TableCell>
              <TableCell>Entity</TableCell>
              <TableCell align="center">Severity</TableCell>
              <TableCell align="center">Confidence</TableCell>
              <TableCell align="center">Status</TableCell>
              <TableCell align="center">Phases</TableCell>
              <TableCell>Assigned To</TableCell>
              <TableCell>Created</TableCell>
              <TableCell align="center">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {incidents.length === 0 ? (
              <TableRow>
                <TableCell colSpan={10} align="center">
                  <Typography variant="body2" color="text.secondary">
                    No incidents found
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              incidents.map((incident) => (
                <TableRow key={incident.incident_id} hover>
                  <TableCell>
                    <Typography variant="body2" fontWeight="bold">
                      {incident.incident_id}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">{incident.pattern_name}</Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" sx={{ fontSize: '0.85rem' }}>
                      {incident.entity_key}
                    </Typography>
                  </TableCell>
                  <TableCell align="center">
                    <Chip
                      label={incident.severity}
                      color={getSeverityColor(incident.severity) as any}
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="center">
                    <Chip
                      label={incident.confidence_level}
                      color={getConfidenceColor(incident.confidence_level) as any}
                      size="small"
                      variant="outlined"
                    />
                  </TableCell>
                  <TableCell align="center">
                    <Chip
                      label={incident.status}
                      color={getStatusColor(incident.status) as any}
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="center">
                    <Typography variant="body2">
                      {incident.phases_matched?.length || 0} / {incident.event_count} events
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">
                      {incident.assigned_to || '-'}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">
                      {new Date(incident.created_at).toLocaleString()}
                    </Typography>
                  </TableCell>
                  <TableCell align="center">
                    <Stack direction="row" spacing={1}>
                      <Tooltip title="View Details">
                        <IconButton
                          size="small"
                          color="primary"
                          onClick={() => handleViewDetails(incident)}
                        >
                          <Visibility />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Assign">
                        <IconButton
                          size="small"
                          color="info"
                          onClick={() => {
                            setAssigningIncident(incident);
                            setAssignDialogOpen(true);
                          }}
                        >
                          <Person />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Execute Playbook">
                        <IconButton
                          size="small"
                          color="success"
                          onClick={() => handleExecutePlaybook(incident.incident_id)}
                        >
                          <PlayArrow />
                        </IconButton>
                      </Tooltip>
                    </Stack>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Detail Dialog */}
      <Dialog
        open={detailDialogOpen}
        onClose={() => setDetailDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Incident Details: {selectedIncident?.incident_id}
        </DialogTitle>
        <DialogContent>
          {selectedIncident && (
            <Box>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Pattern
                  </Typography>
                  <Typography variant="body1">{selectedIncident.pattern_name}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Entity Key
                  </Typography>
                  <Typography variant="body1">{selectedIncident.entity_key}</Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Matched Phases
                  </Typography>
                  <Box sx={{ mt: 1 }}>
                    {selectedIncident.phases_matched?.map((phase, idx) => (
                      <Chip key={idx} label={phase} size="small" sx={{ mr: 1, mb: 1 }} />
                    ))}
                  </Box>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
                    Status
                  </Typography>
                  <FormControl size="small" sx={{ minWidth: 200 }}>
                    <Select
                      value={selectedIncident.status}
                      onChange={(e) => handleUpdateStatus(selectedIncident.incident_id, e.target.value)}
                    >
                      <MenuItem value="open">Open</MenuItem>
                      <MenuItem value="investigating">Investigating</MenuItem>
                      <MenuItem value="contained">Contained</MenuItem>
                      <MenuItem value="resolved">Resolved</MenuItem>
                      <MenuItem value="false_positive">False Positive</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
                    Events Timeline ({selectedIncident.event_count})
                  </Typography>
                  <Paper variant="outlined" sx={{ p: 2, maxHeight: 300, overflow: 'auto' }}>
                    {selectedIncident.events?.map((event, idx) => (
                      <Box key={idx} sx={{ mb: 2, pb: 2, borderBottom: idx < selectedIncident.events!.length - 1 ? 1 : 0, borderColor: 'divider' }}>
                        <Typography variant="body2" fontWeight="bold">
                          Phase: {event.phase}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {new Date(event.timestamp).toLocaleString()}
                        </Typography>
                        <Typography variant="caption" component="pre" sx={{ fontSize: '0.75rem', mt: 1, display: 'block' }}>
                          {JSON.stringify(event.event_data, null, 2)}
                        </Typography>
                      </Box>
                    ))}
                  </Paper>
                </Grid>
              </Grid>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDetailDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Assign Dialog */}
      <Dialog open={assignDialogOpen} onClose={() => setAssignDialogOpen(false)}>
        <DialogTitle>Assign Incident</DialogTitle>
        <DialogContent>
          <Typography variant="body2" sx={{ mb: 2 }}>
            Assign incident {assigningIncident?.incident_id} to an analyst
          </Typography>
          <TextField
            fullWidth
            label="Analyst Name/Email"
            value={assignAnalyst}
            onChange={(e) => setAssignAnalyst(e.target.value)}
            size="small"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAssignDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleAssignIncident} variant="contained" color="primary">
            Assign
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Incidents;
