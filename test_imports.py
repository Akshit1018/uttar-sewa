#!/usr/bin/env python3
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, '/app')

try:
    # Try to import the models
    from backend.models import VideoModel
    print("Successfully imported VideoModel from backend.models")
except Exception as e:
    print(f"Error importing VideoModel: {str(e)}")

try:
    # Try to import the services
    from backend.services.processing_service import ProcessingService
    print("Successfully imported ProcessingService from backend.services.processing_service")
except Exception as e:
    print(f"Error importing ProcessingService: {str(e)}")