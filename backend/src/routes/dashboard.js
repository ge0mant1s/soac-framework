
/**
 * Dashboard Routes
 * Provides aggregated data for dashboard visualization
 */

const express = require('express');
const router = express.Router();
const { authenticateToken } = require('../middleware/auth');
const fs = require('fs');
const path = require('path');

/**
 * GET /api/dashboard/overview
 * Get complete dashboard overview
 */
router.get('/overview', authenticateToken, (req, res) => {
  try {
    // Load all data
    const devicesPath = path.join(__dirname, '../../../data/mock/devices.json');
    const alertsPath = path.join(__dirname, '../../../data/mock/alerts.json');
    const paloaltoPath = path.join(__dirname, '../../../data/mock/paloalto_rules.json');
    const entraidPath = path.join(__dirname, '../../../data/mock/entraid_rules.json');
    const statsPath = path.join(__dirname, '../../../data/mock/statistics.json');

    const devices = JSON.parse(fs.readFileSync(devicesPath, 'utf8'));
    const alerts = JSON.parse(fs.readFileSync(alertsPath, 'utf8'));
    const paloaltoRules = JSON.parse(fs.readFileSync(paloaltoPath, 'utf8'));
    const entraidRules = JSON.parse(fs.readFileSync(entraidPath, 'utf8'));
    const statistics = JSON.parse(fs.readFileSync(statsPath, 'utf8'));

    const allRules = [...paloaltoRules, ...entraidRules];

    const overview = {
      summary: {
        totalDevices: devices.length,
        activeDevices: devices.filter(d => d.status === 'active').length,
        totalRules: allRules.length,
        enabledRules: allRules.filter(r => r.enabled).length,
        totalAlerts: alerts.length,
        openAlerts: alerts.filter(a => a.status === 'open').length,
        criticalAlerts: alerts.filter(a => a.severity === 'Critical').length
      },
      alerts: {
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
        recent: alerts
          .sort((a, b) => new Date(b.detectedAt) - new Date(a.detectedAt))
          .slice(0, 10)
      },
      rules: {
        byDevice: {
          paloalto: paloaltoRules.length,
          entraid: entraidRules.length
        },
        bySeverity: {
          critical: allRules.filter(r => r.severity === 'Critical').length,
          high: allRules.filter(r => r.severity === 'High').length,
          medium: allRules.filter(r => r.severity === 'Medium').length,
          low: allRules.filter(r => r.severity === 'Low').length
        }
      },
      devices: devices.map(d => ({
        id: d.id,
        name: d.name,
        type: d.type,
        status: d.status,
        lastSync: d.lastSync
      })),
      timestamp: new Date().toISOString()
    };

    res.json({
      success: true,
      data: overview
    });
  } catch (error) {
    console.error('Error generating dashboard:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to generate dashboard'
    });
  }
});

/**
 * GET /api/dashboard/threat-landscape
 * Get threat landscape data
 */
router.get('/threat-landscape', authenticateToken, (req, res) => {
  try {
    const alertsPath = path.join(__dirname, '../../../data/mock/alerts.json');
    const alerts = JSON.parse(fs.readFileSync(alertsPath, 'utf8'));

    // Group by MITRE tactics
    const tacticCounts = alerts.reduce((acc, alert) => {
      const tactic = alert.mitreTactic;
      acc[tactic] = (acc[tactic] || 0) + 1;
      return acc;
    }, {});

    // Group by technique
    const techniqueCounts = alerts.reduce((acc, alert) => {
      const technique = alert.mitreTechnique;
      acc[technique] = (acc[technique] || 0) + 1;
      return acc;
    }, {});

    const threatLandscape = {
      byTactic: Object.entries(tacticCounts)
        .map(([tactic, count]) => ({ tactic, count }))
        .sort((a, b) => b.count - a.count),
      byTechnique: Object.entries(techniqueCounts)
        .map(([technique, count]) => ({ technique, count }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 10),
      totalThreats: alerts.length,
      uniqueTactics: Object.keys(tacticCounts).length,
      uniqueTechniques: Object.keys(techniqueCounts).length
    };

    res.json({
      success: true,
      data: threatLandscape
    });
  } catch (error) {
    console.error('Error generating threat landscape:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to generate threat landscape'
    });
  }
});

module.exports = router;
