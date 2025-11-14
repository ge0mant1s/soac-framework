import { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip,
  IconButton,
  TextField,
  MenuItem,
  Grid,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  FilterList as FilterIcon,
  Visibility as ViewIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { eventAPI, deviceAPI } from '../services/api';
import type { Event, Device } from '../types';
import { format } from 'date-fns';

export default function Events() {
  const [events, setEvents] = useState<Event[]>([]);
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(50);
  const [total, setTotal] = useState(0);
  
  // Filters
  const [deviceFilter, setDeviceFilter] = useState('');
  const [eventTypeFilter, setEventTypeFilter] = useState('');
  const [severityFilter, setSeverityFilter] = useState('');
  const [processedFilter, setProcessedFilter] = useState('');
  
  // Event details dialog
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [detailsOpen, setDetailsOpen] = useState(false);
  
  // Auto-refresh
  const [autoRefresh, setAutoRefresh] = useState(true);

  const fetchEvents = async () => {
    try {
      setLoading(true);
      const params: any = {
        page: page + 1,
        page_size: rowsPerPage,
      };
      
      if (deviceFilter) params.device_id = deviceFilter;
      if (eventTypeFilter) params.event_type = eventTypeFilter;
      if (severityFilter) params.severity = severityFilter;
      if (processedFilter !== '') params.processed = processedFilter === 'true';
      
      const response = await eventAPI.list(params);
      setEvents(response.events);
      setTotal(response.total);
      setError(null);
    } catch (err: any) {
      console.error('Error fetching events:', err);
      setError(err.response?.data?.error?.message || 'Failed to fetch events');
    } finally {
      setLoading(false);
    }
  };

  const fetchDevices = async () => {
    try {
      const devicesData = await deviceAPI.list();
      setDevices(devicesData);
    } catch (err) {
      console.error('Error fetching devices:', err);
    }
  };

  useEffect(() => {
    fetchDevices();
  }, []);

  useEffect(() => {
    fetchEvents();
  }, [page, rowsPerPage, deviceFilter, eventTypeFilter, severityFilter, processedFilter]);

  // Auto-refresh every 30 seconds
  useEffect(() => {
    if (!autoRefresh) return;
    
    const interval = setInterval(() => {
      fetchEvents();
    }, 30000);
    
    return () => clearInterval(interval);
  }, [autoRefresh, page, rowsPerPage, deviceFilter, eventTypeFilter, severityFilter, processedFilter]);

  const handleChangePage = (_event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleViewDetails = (event: Event) => {
    setSelectedEvent(event);
    setDetailsOpen(true);
  };

  const handleDeleteEvent = async (eventId: string) => {
    if (!confirm('Are you sure you want to delete this event?')) return;
    
    try {
      await eventAPI.delete(eventId);
      fetchEvents();
    } catch (err) {
      console.error('Error deleting event:', err);
      alert('Failed to delete event');
    }
  };

  const handleClearFilters = () => {
    setDeviceFilter('');
    setEventTypeFilter('');
    setSeverityFilter('');
    setProcessedFilter('');
    setPage(0);
  };

  const getSeverityColor = (severity: string | null): 'error' | 'warning' | 'info' | 'success' | 'default' => {
    if (!severity) return 'default';
    
    switch (severity.toLowerCase()) {
      case 'critical':
        return 'error';
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

  const formatTimestamp = (timestamp: string) => {
    try {
      return format(new Date(timestamp), 'MMM dd, yyyy HH:mm:ss');
    } catch {
      return timestamp;
    }
  };

  return (
    <Container maxWidth="xl">
      <Box sx={{ py: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" component="h1">
            Security Events
          </Typography>
          <Box>
            <Button
              variant={autoRefresh ? 'contained' : 'outlined'}
              color="primary"
              onClick={() => setAutoRefresh(!autoRefresh)}
              sx={{ mr: 1 }}
            >
              Auto-Refresh: {autoRefresh ? 'ON' : 'OFF'}
            </Button>
            <IconButton onClick={fetchEvents} color="primary">
              <RefreshIcon />
            </IconButton>
          </Box>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        {/* Filters */}
        <Paper sx={{ p: 2, mb: 2 }}>
          <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
            <FilterIcon sx={{ mr: 1 }} />
            Filters
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                select
                fullWidth
                label="Device"
                value={deviceFilter}
                onChange={(e) => setDeviceFilter(e.target.value)}
                size="small"
              >
                <MenuItem value="">All Devices</MenuItem>
                {devices.map((device) => (
                  <MenuItem key={device.id} value={device.id}>
                    {device.name}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6} md={2}>
              <TextField
                fullWidth
                label="Event Type"
                value={eventTypeFilter}
                onChange={(e) => setEventTypeFilter(e.target.value)}
                size="small"
                placeholder="e.g. authentication"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={2}>
              <TextField
                select
                fullWidth
                label="Severity"
                value={severityFilter}
                onChange={(e) => setSeverityFilter(e.target.value)}
                size="small"
              >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="critical">Critical</MenuItem>
                <MenuItem value="high">High</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="low">Low</MenuItem>
                <MenuItem value="info">Info</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6} md={2}>
              <TextField
                select
                fullWidth
                label="Processed"
                value={processedFilter}
                onChange={(e) => setProcessedFilter(e.target.value)}
                size="small"
              >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="true">Processed</MenuItem>
                <MenuItem value="false">Unprocessed</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} sm={12} md={3}>
              <Button
                fullWidth
                variant="outlined"
                onClick={handleClearFilters}
                sx={{ height: '40px' }}
              >
                Clear Filters
              </Button>
            </Grid>
          </Grid>
        </Paper>

        {/* Events Table */}
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Timestamp</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Severity</TableCell>
                <TableCell>Device</TableCell>
                <TableCell>Processed</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading && events.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} align="center">
                    <CircularProgress />
                  </TableCell>
                </TableRow>
              ) : events.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} align="center">
                    No events found
                  </TableCell>
                </TableRow>
              ) : (
                events.map((event) => {
                  const device = devices.find(d => d.id === event.device_id);
                  
                  return (
                    <TableRow key={event.id} hover>
                      <TableCell>{formatTimestamp(event.timestamp)}</TableCell>
                      <TableCell>
                        <Chip label={event.event_type || 'unknown'} size="small" />
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={event.severity || 'info'}
                          color={getSeverityColor(event.severity)}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{device?.name || event.device_id}</TableCell>
                      <TableCell>
                        <Chip
                          label={event.processed ? 'Yes' : 'No'}
                          color={event.processed ? 'success' : 'warning'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell align="right">
                        <IconButton
                          size="small"
                          onClick={() => handleViewDetails(event)}
                          title="View Details"
                        >
                          <ViewIcon />
                        </IconButton>
                        <IconButton
                          size="small"
                          onClick={() => handleDeleteEvent(event.id)}
                          title="Delete"
                          color="error"
                        >
                          <DeleteIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  );
                })
              )}
            </TableBody>
          </Table>
          <TablePagination
            rowsPerPageOptions={[25, 50, 100]}
            component="div"
            count={total}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </TableContainer>
      </Box>

      {/* Event Details Dialog */}
      <Dialog
        open={detailsOpen}
        onClose={() => setDetailsOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Event Details</DialogTitle>
        <DialogContent>
          {selectedEvent && (
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                <strong>ID:</strong> {selectedEvent.id}
              </Typography>
              <Typography variant="subtitle2" gutterBottom>
                <strong>Timestamp:</strong> {formatTimestamp(selectedEvent.timestamp)}
              </Typography>
              <Typography variant="subtitle2" gutterBottom>
                <strong>Type:</strong> {selectedEvent.event_type || 'N/A'}
              </Typography>
              <Typography variant="subtitle2" gutterBottom>
                <strong>Severity:</strong>{' '}
                <Chip
                  label={selectedEvent.severity || 'info'}
                  color={getSeverityColor(selectedEvent.severity)}
                  size="small"
                />
              </Typography>
              <Typography variant="subtitle2" gutterBottom>
                <strong>Processed:</strong> {selectedEvent.processed ? 'Yes' : 'No'}
              </Typography>
              
              <Typography variant="h6" sx={{ mt: 2, mb: 1 }}>
                Normalized Data
              </Typography>
              <Paper sx={{ p: 2, bgcolor: 'grey.100', overflow: 'auto', maxHeight: 200 }}>
                <pre style={{ margin: 0, fontSize: '12px' }}>
                  {JSON.stringify(selectedEvent.normalized_data, null, 2)}
                </pre>
              </Paper>
              
              <Typography variant="h6" sx={{ mt: 2, mb: 1 }}>
                Raw Data
              </Typography>
              <Paper sx={{ p: 2, bgcolor: 'grey.100', overflow: 'auto', maxHeight: 200 }}>
                <pre style={{ margin: 0, fontSize: '12px' }}>
                  {JSON.stringify(selectedEvent.raw_data, null, 2)}
                </pre>
              </Paper>
              
              {selectedEvent.detection_results && (
                <>
                  <Typography variant="h6" sx={{ mt: 2, mb: 1 }}>
                    Detection Results
                  </Typography>
                  <Paper sx={{ p: 2, bgcolor: 'grey.100', overflow: 'auto', maxHeight: 200 }}>
                    <pre style={{ margin: 0, fontSize: '12px' }}>
                      {JSON.stringify(selectedEvent.detection_results, null, 2)}
                    </pre>
                  </Paper>
                </>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDetailsOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
