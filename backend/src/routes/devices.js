
/**
 * Device Management Routes
 * Handles device CRUD operations and integrations
 */

const express = require('express');
const router = express.Router();
const { authenticateToken } = require('../middleware/auth');
const fs = require('fs');
const path = require('path');

// Load mock data
const dataPath = path.join(__dirname, '../../../data/mock/devices.json');

/**
 * GET /api/devices
 * Get all devices
 */
router.get('/', authenticateToken, (req, res) => {
  try {
    const devices = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
    res.json({
      success: true,
      count: devices.length,
      data: devices
    });
  } catch (error) {
    console.error('Error reading devices:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to retrieve devices'
    });
  }
});

/**
 * GET /api/devices/:id
 * Get device by ID
 */
router.get('/:id', authenticateToken, (req, res) => {
  try {
    const devices = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
    const device = devices.find(d => d.id === req.params.id);

    if (!device) {
      return res.status(404).json({
        error: 'Not found',
        message: 'Device not found'
      });
    }

    res.json({
      success: true,
      data: device
    });
  } catch (error) {
    console.error('Error reading device:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to retrieve device'
    });
  }
});

/**
 * POST /api/devices
 * Create new device
 */
router.post('/', authenticateToken, (req, res) => {
  try {
    const devices = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
    const newDevice = {
      id: `device-${String(devices.length + 1).padStart(3, '0')}`,
      ...req.body,
      status: 'active',
      lastSync: new Date().toISOString()
    };

    devices.push(newDevice);
    fs.writeFileSync(dataPath, JSON.stringify(devices, null, 2));

    res.status(201).json({
      success: true,
      message: 'Device created successfully',
      data: newDevice
    });
  } catch (error) {
    console.error('Error creating device:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to create device'
    });
  }
});

/**
 * PUT /api/devices/:id
 * Update device
 */
router.put('/:id', authenticateToken, (req, res) => {
  try {
    const devices = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
    const index = devices.findIndex(d => d.id === req.params.id);

    if (index === -1) {
      return res.status(404).json({
        error: 'Not found',
        message: 'Device not found'
      });
    }

    devices[index] = {
      ...devices[index],
      ...req.body,
      lastSync: new Date().toISOString()
    };

    fs.writeFileSync(dataPath, JSON.stringify(devices, null, 2));

    res.json({
      success: true,
      message: 'Device updated successfully',
      data: devices[index]
    });
  } catch (error) {
    console.error('Error updating device:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to update device'
    });
  }
});

/**
 * DELETE /api/devices/:id
 * Delete device
 */
router.delete('/:id', authenticateToken, (req, res) => {
  try {
    const devices = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
    const index = devices.findIndex(d => d.id === req.params.id);

    if (index === -1) {
      return res.status(404).json({
        error: 'Not found',
        message: 'Device not found'
      });
    }

    devices.splice(index, 1);
    fs.writeFileSync(dataPath, JSON.stringify(devices, null, 2));

    res.json({
      success: true,
      message: 'Device deleted successfully'
    });
  } catch (error) {
    console.error('Error deleting device:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to delete device'
    });
  }
});

/**
 * POST /api/devices/:id/sync
 * Sync device rules
 */
router.post('/:id/sync', authenticateToken, (req, res) => {
  try {
    const devices = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
    const device = devices.find(d => d.id === req.params.id);

    if (!device) {
      return res.status(404).json({
        error: 'Not found',
        message: 'Device not found'
      });
    }

    // Simulate sync operation
    device.lastSync = new Date().toISOString();
    fs.writeFileSync(dataPath, JSON.stringify(devices, null, 2));

    res.json({
      success: true,
      message: `Device ${device.name} synced successfully`,
      data: {
        deviceId: device.id,
        syncedAt: device.lastSync,
        status: 'completed'
      }
    });
  } catch (error) {
    console.error('Error syncing device:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to sync device'
    });
  }
});

module.exports = router;
