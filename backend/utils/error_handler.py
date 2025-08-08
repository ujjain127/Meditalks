"""
Error Handler Utility for MediTalks Backend
Provides centralized error handling and logging
"""

import logging
from flask import jsonify
from typing import Any, Dict

logger = logging.getLogger(__name__)

def handle_error(error: Exception, status_code: int = 500) -> tuple:
    """
    Handle errors and return appropriate JSON response
    
    Args:
        error (Exception): The error that occurred
        status_code (int): HTTP status code to return
        
    Returns:
        tuple: (JSON response, status code)
    """
    error_message = str(error)
    error_type = type(error).__name__
    
    # Log the error
    logger.error(f"Error occurred: {error_type} - {error_message}")
    
    # Create error response
    response = {
        'success': False,
        'error': {
            'message': 'Internal server error',
            'details': error_message
        }
    }
    
    # Customize response based on error type
    if isinstance(error, ValueError):
        response['error']['message'] = 'Invalid input provided'
        status_code = 400
    elif isinstance(error, FileNotFoundError):
        response['error']['message'] = 'Requested file not found'
        status_code = 404
    elif isinstance(error, PermissionError):
        response['error']['message'] = 'Permission denied'
        status_code = 403
    elif isinstance(error, ConnectionError):
        response['error']['message'] = 'External service connection failed'
        status_code = 503
    
    return jsonify(response), status_code

def log_api_call(endpoint: str, method: str, data: Dict[str, Any] = None):
    """
    Log API call for debugging and monitoring
    
    Args:
        endpoint (str): API endpoint called
        method (str): HTTP method
        data (Dict): Request data (optional)
    """
    logger.info(f"API Call: {method} {endpoint}")
    if data:
        logger.debug(f"Request data: {data}")

def validate_required_fields(data: Dict[str, Any], required_fields: list) -> Dict[str, Any]:
    """
    Validate that required fields are present in request data
    
    Args:
        data (Dict): Request data to validate
        required_fields (list): List of required field names
        
    Returns:
        Dict: Validation result
    """
    if not data:
        return {
            'valid': False,
            'message': 'No data provided'
        }
    
    missing_fields = []
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
    
    if missing_fields:
        return {
            'valid': False,
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }
    
    return {
        'valid': True,
        'message': 'All required fields present'
    }
