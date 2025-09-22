import os
import sys
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add backend folder to path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Import backend modules
try:
    from backend.database import init_db, get_db, save_document_to_db, Document, Analysis
    from backend.auth_system import auth_manager
    from backend.integration_services import IntegrationManager
    from backend.enhanced_document_generator import EnhancedDocumentGenerator

    BACKEND_IMPORTS_SUCCESS = True
except ImportError as e:
    print(f"⚠️ Warning: Backend imports failed: {e}")
    BACKEND_IMPORTS_SUCCESS = False

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize components if imports succeeded
if BACKEND_IMPORTS_SUCCESS:
    try:
        init_db()
        integration_manager = IntegrationManager()
        enhanced_doc_generator = EnhancedDocumentGenerator(None)
    except Exception as e:
        print(f"⚠️ Warning: Component initialization failed: {e}")

# Health endpoint
@app.route('/api/health')
def health_check():
    return {
        'status': 'healthy',
        'backend_imports': BACKEND_IMPORTS_SUCCESS,
        'timestamp': str(datetime.now())
    }

# Example analyze endpoint
@app.route('/api/analyze', methods=['POST'])
def analyze_document():
    if not BACKEND_IMPORTS_SUCCESS:
        return {'error': 'Backend components not loaded'}, 500
    data = request.json
    text = data.get('text')
    if not text:
        return {'error': 'Text is required'}, 400
    return {
        'status': 'success',
        'length': len(text),
        'timestamp': str(datetime.now())
    }

# CORS for all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == "__main__":
    app.run(debug=True)
