import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_engine.factory import get_ai_assistant

app = Flask(__name__)
CORS(app)

@app.route('/api/ai/nl-to-cql', methods=['POST'])
def nl_to_cql():
    data = request.json
    query = data.get('query')
    provider = data.get('provider', 'abacus')  # default to abacus
    if not query:
        return jsonify({"error": "Query is required"}), 400
    try:
        ai_engine = get_ai_assistant(provider)
        result = ai_engine.natural_language_to_cql(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/summarize-incident', methods=['POST'])
def summarize_incident():
    data = request.json
    text = data.get('text')
    provider = data.get('provider', 'abacus')
    if not text:
        return jsonify({"error": "Incident text is required"}), 400
    try:
        ai_engine = get_ai_assistant(provider)
        summary = ai_engine.summarize_incident(text)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)