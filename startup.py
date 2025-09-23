#!/usr/bin/env python3
"""
Azure Web App Startup Script for BA Agent Backend
This file is the entry point for Azure Web App deployment
"""

import os
import sys
from main import app

if __name__ == "__main__":
    # Get port from environment variable (Azure sets this)
    port = int(os.environ.get('PORT', 8000))
    
    print(f"🚀 Starting BA Agent Backend on Azure Web App")
    print(f"🌐 Port: {port}")
    print(f"🔧 Environment: {os.environ.get('FLASK_ENV', 'production')}")
    
    # Run the Flask application
    app.run(host='0.0.0.0', port=port, debug=False)