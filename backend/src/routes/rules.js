
/**
 * Rules Management Routes
 * Handles detection rules for Palo Alto and EntraID
 */

const express = require('express');
const router = express.Router();
const { authenticateToken } = require('../middleware/auth');
const fs = require('fs');
const path = require('path');

/**
 * GET /api/rules
 * Get all rules (combined or by device type)
 */
router.get('/', authenticateToken, (req, res) => {
  try {
    const { type } = req.query;
    
    let rules = [];
    
    if (!type || type === 'paloalto') {
      const paloaltoPath = path.join(__dirname, '../../../data/mock/paloalto_rules.json');
      const paloaltoRules = JSON.parse(fs.readFileSync(paloaltoPath, 'utf8'));
      rules = [...rules, ...paloaltoRules];
    }
    
    if (!type || type === 'entraid') {
      const entraidPath = path.join(__dirname, '../../../data/mock/entraid_rules.json');
      const entraidRules = JSON.parse(fs.readFileSync(entraidPath, 'utf8'));
      rules = [...rules, ...entraidRules];
    }

    res.json({
      success: true,
      count: rules.length,
      data: rules
    });
  } catch (error) {
    console.error('Error reading rules:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to retrieve rules'
    });
  }
});

/**
 * GET /api/rules/:id
 * Get rule by ID
 */
router.get('/:id', authenticateToken, (req, res) => {
  try {
    const paloaltoPath = path.join(__dirname, '../../../data/mock/paloalto_rules.json');
    const entraidPath = path.join(__dirname, '../../../data/mock/entraid_rules.json');
    
    const paloaltoRules = JSON.parse(fs.readFileSync(paloaltoPath, 'utf8'));
    const entraidRules = JSON.parse(fs.readFileSync(entraidPath, 'utf8'));
    
    const allRules = [...paloaltoRules, ...entraidRules];
    const rule = allRules.find(r => r.id === req.params.id);

    if (!rule) {
      return res.status(404).json({
        error: 'Not found',
        message: 'Rule not found'
      });
    }

    res.json({
      success: true,
      data: rule
    });
  } catch (error) {
    console.error('Error reading rule:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to retrieve rule'
    });
  }
});

/**
 * PUT /api/rules/:id
 * Update rule
 */
router.put('/:id', authenticateToken, (req, res) => {
  try {
    const ruleId = req.params.id;
    const deviceType = ruleId.startsWith('PA-') ? 'paloalto' : 'entraid';
    const filePath = path.join(__dirname, `../../../data/mock/${deviceType}_rules.json`);
    
    const rules = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const index = rules.findIndex(r => r.id === ruleId);

    if (index === -1) {
      return res.status(404).json({
        error: 'Not found',
        message: 'Rule not found'
      });
    }

    rules[index] = {
      ...rules[index],
      ...req.body,
      lastModified: new Date().toISOString()
    };

    fs.writeFileSync(filePath, JSON.stringify(rules, null, 2));

    res.json({
      success: true,
      message: 'Rule updated successfully',
      data: rules[index]
    });
  } catch (error) {
    console.error('Error updating rule:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to update rule'
    });
  }
});

/**
 * POST /api/rules/:id/toggle
 * Toggle rule enabled/disabled
 */
router.post('/:id/toggle', authenticateToken, (req, res) => {
  try {
    const ruleId = req.params.id;
    const deviceType = ruleId.startsWith('PA-') ? 'paloalto' : 'entraid';
    const filePath = path.join(__dirname, `../../../data/mock/${deviceType}_rules.json`);
    
    const rules = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const rule = rules.find(r => r.id === ruleId);

    if (!rule) {
      return res.status(404).json({
        error: 'Not found',
        message: 'Rule not found'
      });
    }

    rule.enabled = !rule.enabled;
    rule.lastModified = new Date().toISOString();

    fs.writeFileSync(filePath, JSON.stringify(rules, null, 2));

    res.json({
      success: true,
      message: `Rule ${rule.enabled ? 'enabled' : 'disabled'} successfully`,
      data: rule
    });
  } catch (error) {
    console.error('Error toggling rule:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to toggle rule'
    });
  }
});

/**
 * GET /api/rules/stats/summary
 * Get rules statistics
 */
router.get('/stats/summary', authenticateToken, (req, res) => {
  try {
    const paloaltoPath = path.join(__dirname, '../../../data/mock/paloalto_rules.json');
    const entraidPath = path.join(__dirname, '../../../data/mock/entraid_rules.json');
    
    const paloaltoRules = JSON.parse(fs.readFileSync(paloaltoPath, 'utf8'));
    const entraidRules = JSON.parse(fs.readFileSync(entraidPath, 'utf8'));
    
    const allRules = [...paloaltoRules, ...entraidRules];

    const stats = {
      total: allRules.length,
      enabled: allRules.filter(r => r.enabled).length,
      disabled: allRules.filter(r => !r.enabled).length,
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
    };

    res.json({
      success: true,
      data: stats
    });
  } catch (error) {
    console.error('Error calculating stats:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to calculate statistics'
    });
  }
});

module.exports = router;
