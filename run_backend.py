#!/usr/bin/env python3
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, '/app')

# Import the FastAPI app
from backend.server import app

# Print success message
print("Backend app imported successfully!")