
/**
 * Alerts Routes
 * Handles security alerts and incidents
 */

const express = require('express');
const router = express.Router();
const { authenticateToken } = require('../middleware/auth');
const fs = require('fs');
const path = require('path');

const alertsPath = path.join(__dirname, '../../../data/mock/alerts.json');

/**
 * GET /api/alerts
 * Get all alerts with optional filtering
 */
router.get('/', authenticateToken, (req, res) => {
  try {
    let alerts = JSON.parse(fs.readFileSync(alertsPath, 'utf8'));
    
    // Apply filters
    const { status, severity, limit } = req.query;
    
    if (status) {
      alerts = alerts.filter(a => a.status === status);
    }
    
    if (severity) {
      alerts = alerts.filter(a => a.severity === severity);
    }
    
    // Sort by detection time (newest first)
    alerts.sort((a, b) => new Date(b.detectedAt) - new Date(a.detectedAt));
    
    // Apply limit
    if (limit) {
      alerts = alerts.slice(0, parseInt(limit));
    }

    res.json({
      success: true,
      count: alerts.length,
      data: alerts
    });
  } catch (error) {
    console.error('Error reading alerts:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to retrieve alerts'
    });
  }
});

/**
 * GET /api/alerts/:id
 * Get alert by ID
 */
router.get('/:id', authenticateToken, (req, res) => {
  try {
    const alerts = JSON.parse(fs.readFileSync(alertsPath, 'utf8'));
    const alert = alerts.find(a => a.id === req.params.id);

    if (!alert) {
      return res.status(404).json({
        error: 'Not found',
        message: 'Alert not found'
      });
    }

    res.json({
      success: true,
      data: alert
    });
  } catch (error) {
    console.error('Error reading alert:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to retrieve alert'
    });
  }
});

/**
 * PUT /api/alerts/:id/status
 * Update alert status
 */
router.put('/:id/status', authenticateToken, (req, res) => {
  try {
    const { status, comment } = req.body;
    
    const validStatuses = ['open', 'investigating', 'resolved', 'false_positive'];
    if (!validStatuses.includes(status)) {
      return res.status(400).json({
        error: 'Invalid status',
        message: 'Status must be one of: ' + validStatuses.join(', ')
      });
    }

    const alerts = JSON.parse(fs.readFileSync(alertsPath, 'utf8'));
    const alert = alerts.find(a => a.id === req.params.id);

    if (!alert) {
      return res.status(404).json({
        error: 'Not found',
        message: 'Alert not found'
      });
    }

    alert.status = status;
    alert.updatedAt = new Date().toISOString();
    alert.updatedBy = req.user.username;
    
    if (comment) {
      alert.comment = comment;
    }

    fs.writeFileSync(alertsPath, JSON.stringify(alerts, null, 2));

    res.json({
      success: true,
      message: 'Alert status updated successfully',
      data: alert
    });
  } catch (error) {
    console.error('Error updating alert:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to update alert'
    });
  }
});

/**
 * GET /api/alerts/stats/summary
 * Get alert statistics
 */
router.get('/stats/summary', authenticateToken, (req, res) => {
  try {
    const alerts = JSON.parse(fs.readFileSync(alertsPath, 'utf8'));

    const stats = {
      total: alerts.length,
      byStatus: {
        open: alerts.filter(a => a.status === 'open').length,
        investigating: alerts.filter(a => a.status === 'investigating').length,
        resolved: alerts.filter(a => a.status === 'resolved').length,
        false_positive: alerts.filter(a => a.status === 'false_positive').length
      },
      bySeverity: {
        critical: alerts.filter(a => a.severity === 'Critical').length,
        high: alerts.filter(a => a.severity === 'High').length,
        medium: alerts.filter(a => a.severity === 'Medium').length,
        low: alerts.filter(a => a.severity === 'Low').length
      },
      recentAlerts: alerts
        .sort((a, b) => new Date(b.detectedAt) - new Date(a.detectedAt))
        .slice(0, 5)
    };

    res.json({
      success: true,
      data: stats
    });
  } catch (error) {
    console.error('Error calculating alert stats:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to calculate alert statistics'
    });
  }
});

module.exports = router;
