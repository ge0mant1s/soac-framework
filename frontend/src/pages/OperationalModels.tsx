/**
 * Operational Models page - View loaded operational models and their details
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
  Button,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  ExpandMore,
  Refresh,
  Security,
  Timeline,
  Code,
  PlayArrow,
  CheckCircle,
} from '@mui/icons-material';
import axios from 'axios';

interface OperationalModel {
  id: string;
  name: string;
  version: string;
  severity: string;
  phases_count: number;
  playbooks_count: number;
  created_at: string;
}

interface ModelDetails {
  id: string;
  name: string;
  version: string;
  objective: {
    goal: string;
    business_outcome: string;
  };
  correlation_pattern: {
    pattern_id: string;
    description: string;
    phases: any[];
    correlation_window: string;
    pivot_entities: string[];
  };
  detection_queries: any;
  alert_policy: {
    severity: string;
    trigger_condition: string;
    suppression_window: string;
    escalation_path: string;
    runbook_reference: string;
  };
  playbooks: any[];
  decision_matrix: any[];
  kpi_metrics: any[];
}

const OperationalModels: React.FC = () => {
  const [models, setModels] = useState<OperationalModel[]>([]);
  const [selectedModel, setSelectedModel] = useState<ModelDetails | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [reloading, setReloading] = useState(false);

  useEffect(() => {
    loadModels();
  }, []);

  const loadModels = async () => {
    try {
      setError('');
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/v1/operational-models/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setModels(response.data.models || []);
    } catch (err: any) {
      console.error('Error loading models:', err);
      setError(err.response?.data?.detail || 'Failed to load operational models');
    } finally {
      setIsLoading(false);
    }
  };

  const loadModelDetails = async (modelId: string) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`/api/v1/operational-models/${modelId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setSelectedModel(response.data);
    } catch (err: any) {
      setError('Failed to load model details');
    }
  };

  const handleReloadModels = async () => {
    try {
      setReloading(true);
      setError('');
      const token = localStorage.getItem('token');
      await axios.post(
        '/api/v1/operational-models/reload',
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      await loadModels();
      alert('Operational models reloaded successfully');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to reload models');
    } finally {
      setReloading(false);
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
          Operational Models
        </Typography>
        <Button
          variant="contained"
          startIcon={reloading ? <CircularProgress size={20} /> : <Refresh />}
          onClick={handleReloadModels}
          disabled={reloading}
        >
          Reload Models
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Security color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">{models.length}</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Total Models
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Timeline color="info" sx={{ mr: 1 }} />
                <Typography variant="h6">
                  {models.reduce((sum, m) => sum + m.phases_count, 0)}
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Total Phases
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <PlayArrow color="success" sx={{ mr: 1 }} />
                <Typography variant="h6">
                  {models.reduce((sum, m) => sum + m.playbooks_count, 0)}
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Total Playbooks
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <CheckCircle color="success" sx={{ mr: 1 }} />
                <Typography variant="h6">Active</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Detection Status
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Models List */}
      {models.length === 0 ? (
        <Alert severity="info">
          No operational models loaded. Upload operational model DOCX files and reload.
        </Alert>
      ) : (
        models.map((model) => (
          <Accordion
            key={model.id}
            onChange={(_, expanded) => {
              if (expanded) {
                loadModelDetails(model.id);
              }
            }}
          >
            <AccordionSummary expandIcon={<ExpandMore />}>
              <Box sx={{ display: 'flex', alignItems: 'center', width: '100%', pr: 2 }}>
                <Security sx={{ mr: 2, color: 'primary.main' }} />
                <Box sx={{ flex: 1 }}>
                  <Typography variant="h6">{model.name}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {model.id} • v{model.version}
                  </Typography>
                </Box>
                <Chip
                  label={model.severity}
                  color={getSeverityColor(model.severity) as any}
                  size="small"
                  sx={{ mr: 2 }}
                />
                <Typography variant="body2" color="text.secondary" sx={{ mr: 2 }}>
                  {model.phases_count} Phases
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {model.playbooks_count} Playbooks
                </Typography>
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              {selectedModel?.id === model.id ? (
                <Box>
                  {/* Objective */}
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      Objective
                    </Typography>
                    <Paper variant="outlined" sx={{ p: 2 }}>
                      <Typography variant="subtitle2" color="primary" gutterBottom>
                        Goal
                      </Typography>
                      <Typography variant="body2" paragraph>
                        {selectedModel.objective?.goal}
                      </Typography>
                      <Typography variant="subtitle2" color="primary" gutterBottom>
                        Business Outcome
                      </Typography>
                      <Typography variant="body2">
                        {selectedModel.objective?.business_outcome}
                      </Typography>
                    </Paper>
                  </Box>

                  {/* Correlation Pattern */}
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      Correlation Pattern
                    </Typography>
                    <Paper variant="outlined" sx={{ p: 2 }}>
                      <Grid container spacing={2}>
                        <Grid item xs={12} sm={6}>
                          <Typography variant="subtitle2" color="text.secondary">
                            Pattern ID
                          </Typography>
                          <Typography variant="body2">
                            {selectedModel.correlation_pattern?.pattern_id}
                          </Typography>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                          <Typography variant="subtitle2" color="text.secondary">
                            Correlation Window
                          </Typography>
                          <Typography variant="body2">
                            {selectedModel.correlation_pattern?.correlation_window}
                          </Typography>
                        </Grid>
                        <Grid item xs={12}>
                          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                            Pivot Entities
                          </Typography>
                          <Box>
                            {selectedModel.correlation_pattern?.pivot_entities?.map((entity, idx) => (
                              <Chip key={idx} label={entity} size="small" sx={{ mr: 1, mb: 1 }} />
                            ))}
                          </Box>
                        </Grid>
                      </Grid>
                    </Paper>
                  </Box>

                  {/* Attack Phases */}
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      Attack Phases ({selectedModel.correlation_pattern?.phases?.length || 0})
                    </Typography>
                    <TableContainer component={Paper} variant="outlined">
                      <Table size="small">
                        <TableHead>
                          <TableRow>
                            <TableCell>Phase</TableCell>
                            <TableCell>Source</TableCell>
                            <TableCell>Indicators</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {selectedModel.correlation_pattern?.phases?.map((phase, idx) => (
                            <TableRow key={idx}>
                              <TableCell>
                                <Typography variant="body2" fontWeight="bold">
                                  {phase.name}
                                </Typography>
                              </TableCell>
                              <TableCell>
                                <Typography variant="body2">{phase.source}</Typography>
                              </TableCell>
                              <TableCell>
                                <Typography variant="body2" sx={{ fontSize: '0.85rem' }}>
                                  {phase.indicators}
                                </Typography>
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </Box>

                  {/* Alert Policy */}
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      Alert Policy
                    </Typography>
                    <Paper variant="outlined" sx={{ p: 2 }}>
                      <Grid container spacing={2}>
                        <Grid item xs={12} sm={6}>
                          <Typography variant="subtitle2" color="text.secondary">
                            Severity
                          </Typography>
                          <Chip
                            label={selectedModel.alert_policy?.severity}
                            color={getSeverityColor(selectedModel.alert_policy?.severity) as any}
                            size="small"
                          />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                          <Typography variant="subtitle2" color="text.secondary">
                            Suppression Window
                          </Typography>
                          <Typography variant="body2">
                            {selectedModel.alert_policy?.suppression_window}
                          </Typography>
                        </Grid>
                        <Grid item xs={12}>
                          <Typography variant="subtitle2" color="text.secondary">
                            Trigger Condition
                          </Typography>
                          <Typography variant="body2">
                            {selectedModel.alert_policy?.trigger_condition}
                          </Typography>
                        </Grid>
                        <Grid item xs={12}>
                          <Typography variant="subtitle2" color="text.secondary">
                            Escalation Path
                          </Typography>
                          <Typography variant="body2">
                            {selectedModel.alert_policy?.escalation_path}
                          </Typography>
                        </Grid>
                        <Grid item xs={12}>
                          <Typography variant="subtitle2" color="text.secondary">
                            Runbook Reference
                          </Typography>
                          <Typography variant="body2">
                            {selectedModel.alert_policy?.runbook_reference}
                          </Typography>
                        </Grid>
                      </Grid>
                    </Paper>
                  </Box>

                  {/* Playbooks */}
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      Response Playbooks ({selectedModel.playbooks?.length || 0})
                    </Typography>
                    {selectedModel.playbooks?.map((playbook, idx) => (
                      <Accordion key={idx}>
                        <AccordionSummary expandIcon={<ExpandMore />}>
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <PlayArrow sx={{ mr: 1, color: 'success.main' }} />
                            <Typography variant="body1" fontWeight="bold">
                              {playbook.name}
                            </Typography>
                            <Chip
                              label={`${playbook.steps?.length || 0} steps`}
                              size="small"
                              sx={{ ml: 2 }}
                            />
                          </Box>
                        </AccordionSummary>
                        <AccordionDetails>
                          <TableContainer>
                            <Table size="small">
                              <TableHead>
                                <TableRow>
                                  <TableCell>Step</TableCell>
                                  <TableCell>Action</TableCell>
                                </TableRow>
                              </TableHead>
                              <TableBody>
                                {playbook.steps?.map((step: any, stepIdx: number) => (
                                  <TableRow key={stepIdx}>
                                    <TableCell>{step.step}</TableCell>
                                    <TableCell>
                                      <Typography variant="body2">{step.action}</Typography>
                                    </TableCell>
                                  </TableRow>
                                ))}
                              </TableBody>
                            </Table>
                          </TableContainer>
                        </AccordionDetails>
                      </Accordion>
                    ))}
                  </Box>

                  {/* Detection Queries */}
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      Detection Queries
                    </Typography>
                    {Object.entries(selectedModel.detection_queries || {}).map(([key, value]: any) => {
                      if (key === 'combined_rule' || key === 'trigger_condition') return null;
                      return (
                        <Accordion key={key}>
                          <AccordionSummary expandIcon={<ExpandMore />}>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <Code sx={{ mr: 1, color: 'info.main' }} />
                              <Typography variant="body1">
                                {value.name || key}
                              </Typography>
                            </Box>
                          </AccordionSummary>
                          <AccordionDetails>
                            <Paper
                              variant="outlined"
                              sx={{ p: 2, bgcolor: 'grey.900', color: 'grey.100' }}
                            >
                              <Typography
                                component="pre"
                                sx={{
                                  fontFamily: 'monospace',
                                  fontSize: '0.85rem',
                                  whiteSpace: 'pre-wrap',
                                  wordBreak: 'break-word',
                                }}
                              >
                                {value.query}
                              </Typography>
                            </Paper>
                          </AccordionDetails>
                        </Accordion>
                      );
                    })}
                  </Box>
                </Box>
              ) : (
                <Box display="flex" justifyContent="center" p={3}>
                  <CircularProgress />
                </Box>
              )}
            </AccordionDetails>
          </Accordion>
        ))
      )}
    </Box>
  );
};

export default OperationalModels;
