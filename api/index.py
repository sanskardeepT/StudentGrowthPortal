import sys
import os
from pathlib import Path

# Get the parent directory
PARENT_DIR = str(Path(__file__).parent.parent)
sys.path.insert(0, PARENT_DIR)

# Import the Flask app
from app import app as flask_app

# Export for Vercel serverless
app = flask_app
