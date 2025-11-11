"""
SOaC Framework REST API
Main Flask application
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.incident_manager import IncidentManager
from core.engines.cql_engine import CQLEngine

app = Flask(__name__)
CORS(app)

# Initialize managers
incident_mgr = IncidentManager()
cql_engine = CQLEngine()

# In-memory storage for detection rules (replace with DB later)
detection_rules = []


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


@app.route('/api/detection-rules', methods=['GET', 'POST'])
def detection_rules_list():
    """List or create detection rules"""
    if request.method == 'GET':
        # Filter by platform if specified
        platform = request.args.get('platform')
        if platform:
            filtered = [r for r in detection_rules if r.get('platform') == platform]
            return jsonify(filtered)
        return jsonify(detection_rules)

    elif request.method == 'POST':
        data = request.json
        rule = {
            'id': len(detection_rules) + 1,
            'name': data['name'],
            'platform': data['platform'],
            'query': data.get('query', ''),
            'cql_query': data.get('cql_query', ''),
            'severity': data.get('severity', 'medium'),
            'use_case': data.get('use_case', ''),
            'mitre_tactic': data.get('mitre_tactic', ''),
            'mitre_technique': data.get('mitre_technique', ''),
            'enabled': data.get('enabled', True),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        detection_rules.append(rule)
        return jsonify(rule), 201


@app.route('/api/detection-rules/<int:rule_id>', methods=['GET', 'PUT', 'DELETE'])
def detection_rule_detail(rule_id):
    """Get, update, or delete a detection rule"""
    rule = next((r for r in detection_rules if r['id'] == rule_id), None)
    
    if not rule:
        return jsonify({'error': 'Rule not found'}), 404

    if request.method == 'GET':
        return jsonify(rule)

    elif request.method == 'PUT':
        data = request.json
        rule.update(data)
        rule['updated_at'] = datetime.utcnow().isoformat()
        return jsonify(rule)

    elif request.method == 'DELETE':
        detection_rules.remove(rule)
        return jsonify({'message': 'Rule deleted'}), 200


@app.route('/api/detection-rules/import', methods=['POST'])
def import_detection_rules():
    """Import detection rules from Excel/CSV"""
    data = request.json
    rules = data.get('rules', [])
    
    imported_count = 0
    for rule_data in rules:
        rule = {
            'id': len(detection_rules) + 1,
            'name': rule_data.get('name', 'Imported Rule'),
            'platform': rule_data.get('platform', 'unknown'),
            'query': rule_data.get('query', ''),
            'cql_query': rule_data.get('cql_query', ''),
            'severity': rule_data.get('severity', 'medium'),
            'use_case': rule_data.get('use_case', ''),
            'mitre_tactic': rule_data.get('mitre_tactic', ''),
            'mitre_technique': rule_data.get('mitre_technique', ''),
            'enabled': True,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        detection_rules.append(rule)
        imported_count += 1
    
    return jsonify({
        'message': f'Imported {imported_count} rules',
        'count': imported_count
    }), 201


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


@app.route('/api/use-cases', methods=['GET'])
def list_use_cases():
    """List available use cases"""
    use_cases = [
        {'id': 'intrusion', 'name': 'Intrusion Detection', 'category': 'Security'},
        {'id': 'malware', 'name': 'Malware Detection', 'category': 'Security'},
        {'id': 'data_theft', 'name': 'Data Theft/Exfiltration', 'category': 'Data Protection'},
        {'id': 'fraud', 'name': 'Fraud Detection', 'category': 'Fraud'},
        {'id': 'dos', 'name': 'Denial of Service', 'category': 'Availability'}
    ]
    return jsonify(use_cases)


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get framework statistics"""
    incidents_list = incident_mgr.list_incidents({})
    
    stats = {
        'incidents': {
            'total': len(incidents_list),
            'open': len([i for i in incidents_list if i.status == 'open']),
            'in_progress': len([i for i in incidents_list if i.status == 'investigating']),
            'closed': len([i for i in incidents_list if i.status == 'closed'])
        },
        'detection_rules': {
            'total': len(detection_rules),
            'enabled': len([r for r in detection_rules if r.get('enabled', True)]),
            'by_platform': {}
        },
        'platforms': {
            'supported': len(cql_engine.supported_platforms)
        }
    }
    
    # Count rules by platform
    for rule in detection_rules:
        platform = rule.get('platform', 'unknown')
        stats['detection_rules']['by_platform'][platform] = \
            stats['detection_rules']['by_platform'].get(platform, 0) + 1
    
    return jsonify(stats)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)