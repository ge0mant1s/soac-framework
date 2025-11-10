"""
SOaC Framework REST API
Main Flask application
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.incident_manager import IncidentManager
from core.engines.cql_engine import CQLEngine

app = Flask(__name__)
CORS(app)

# Initialize managers
incident_mgr = IncidentManager()
cql_engine = CQLEngine()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '0.1.0',
        'service': 'soac-api'
    })


@app.route('/api/incidents', methods=['GET', 'POST'])
def incidents():
    """List or create incidents"""
    if request.method == 'GET':
        filters = request.args.to_dict()
        incidents_list = incident_mgr.list_incidents(filters)
        return jsonify([inc.to_dict() for inc in incidents_list])

    elif request.method == 'POST':
        data = request.json
        incident = incident_mgr.create_incident(
            title=data['title'],
            severity=data['severity'],
            use_case=data['use_case'],
            description=data.get('description', '')
        )
        return jsonify(incident.to_dict()), 201


@app.route('/api/incidents/<incident_id>', methods=['GET', 'PUT'])
def incident_detail(incident_id):
    """Get or update incident"""
    incident = incident_mgr.get_incident(incident_id)
    if not incident:
        return jsonify({'error': 'Incident not found'}), 404

    if request.method == 'GET':
        return jsonify(incident.to_dict())

    elif request.method == 'PUT':
        data = request.json
        if 'status' in data:
            incident_mgr.update_status(incident_id, data['status'], data.get('notes', ''))
        if 'assigned_to' in data:
            incident_mgr.assign_incident(incident_id, data['assigned_to'])
        return jsonify(incident.to_dict())


@app.route('/api/cql/translate', methods=['POST'])
def translate_cql():
    """Translate CQL to platform-specific query"""
    data = request.json
    cql_query = data.get('query', '')
    platform = data.get('platform', 'splunk')

    try:
        translated = cql_engine.translate(cql_query, platform)
        return jsonify({
            'cql': cql_query,
            'platform': platform,
            'translated': translated
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/platforms', methods=['GET'])
def list_platforms():
    """List supported platforms"""
    return jsonify({
        'platforms': cql_engine.supported_platforms,
        'count': len(cql_engine.supported_platforms)
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
