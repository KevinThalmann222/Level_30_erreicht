# WSGI configuration file for PythonAnywhere
# This file tells PythonAnywhere how to run the Flask application

import sys
import os

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Import the Flask app
from app import app

# The application object that PythonAnywhere will use
application = app

# Ensure uploads directory exists
upload_dir = os.path.join(project_dir, 'static', 'uploads')
os.makedirs(upload_dir, exist_ok=True)
