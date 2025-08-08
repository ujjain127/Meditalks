"""
Validation Service for MediTalks
Handles input validation and content filtering
"""

import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ValidationService:
    """Service for validating user inputs and content"""
    
    def __init__(self):
        self.max_message_length = 5000
        self.min_message_length = 10
        self.forbidden_patterns = [
            r'<script.*?>.*?</script>',  # Script tags
            r'javascript:',              # JavaScript URLs
            r'on\w+\s*=',               # Event handlers
        ]
        logger.info("Validation service initialized")
    
    def validate_message(self, message: str) -> Dict[str, Any]:
        """
        Validate medical message input
        
        Args:
            message (str): The message to validate
            
        Returns:
            Dict containing validation result
        """
        try:
            if not message or not isinstance(message, str):
                return {
                    'valid': False,
                    'message': 'Message must be a non-empty string'
                }
            
            message = message.strip()
            
            # Check length constraints
            if len(message) < self.min_message_length:
                return {
                    'valid': False,
                    'message': f'Message must be at least {self.min_message_length} characters long'
                }
            
            if len(message) > self.max_message_length:
                return {
                    'valid': False,
                    'message': f'Message must not exceed {self.max_message_length} characters'
                }
            
            # Check for forbidden patterns (XSS prevention)
            for pattern in self.forbidden_patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    return {
                        'valid': False,
                        'message': 'Message contains potentially harmful content'
                    }
            
            # Basic medical content check
            if not self._contains_medical_content(message):
                logger.warning(f"Message may not be medical-related: {message[:100]}...")
            
            return {
                'valid': True,
                'message': 'Message is valid',
                'cleaned_message': message
            }
            
        except Exception as e:
            logger.error(f"Error validating message: {str(e)}")
            return {
                'valid': False,
                'message': f'Validation error: {str(e)}'
            }
    
    def validate_cultural_context(self, context: str) -> Dict[str, Any]:
        """
        Validate cultural context selection
        
        Args:
            context (str): The cultural context to validate
            
        Returns:
            Dict containing validation result
        """
        try:
            valid_contexts = [
                'tagalog-rural',
                'thai-low-literacy', 
                'khmer-indigenous',
                'vietnamese-elderly',
                'malay-traditional',
                'general'
            ]
            
            if not context or context not in valid_contexts:
                return {
                    'valid': False,
                    'message': f'Invalid cultural context. Must be one of: {", ".join(valid_contexts)}'
                }
            
            return {
                'valid': True,
                'message': 'Cultural context is valid'
            }
            
        except Exception as e:
            logger.error(f"Error validating cultural context: {str(e)}")
            return {
                'valid': False,
                'message': f'Context validation error: {str(e)}'
            }
    
    def validate_file_upload(self, file, max_size_mb: int = 10) -> Dict[str, Any]:
        """
        Validate uploaded file
        
        Args:
            file: The uploaded file object
            max_size_mb (int): Maximum file size in MB
            
        Returns:
            Dict containing validation result
        """
        try:
            if not file:
                return {
                    'valid': False,
                    'message': 'No file provided'
                }
            
            # Check file extension
            allowed_extensions = ['.pdf']
            filename = file.filename.lower() if file.filename else ''
            
            if not any(filename.endswith(ext) for ext in allowed_extensions):
                return {
                    'valid': False,
                    'message': f'Invalid file type. Allowed extensions: {", ".join(allowed_extensions)}'
                }
            
            # Check file size (if available)
            if hasattr(file, 'content_length') and file.content_length:
                max_size_bytes = max_size_mb * 1024 * 1024
                if file.content_length > max_size_bytes:
                    return {
                        'valid': False,
                        'message': f'File size exceeds {max_size_mb}MB limit'
                    }
            
            return {
                'valid': True,
                'message': 'File is valid'
            }
            
        except Exception as e:
            logger.error(f"Error validating file: {str(e)}")
            return {
                'valid': False,
                'message': f'File validation error: {str(e)}'
            }
    
    def _contains_medical_content(self, message: str) -> bool:
        """
        Check if message contains medical-related content
        
        Args:
            message (str): The message to check
            
        Returns:
            bool: True if message appears to be medical-related
        """
        medical_keywords = [
            'medicine', 'medication', 'doctor', 'hospital', 'clinic', 'treatment',
            'diagnosis', 'symptoms', 'patient', 'health', 'medical', 'prescription',
            'dose', 'dosage', 'therapy', 'surgery', 'examination', 'consultation',
            'healthcare', 'illness', 'disease', 'condition', 'recovery', 'healing',
            'pain', 'fever', 'infection', 'vaccine', 'immunization', 'checkup'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in medical_keywords)
    
    def sanitize_input(self, text: str) -> str:
        """
        Sanitize user input by removing potentially harmful content
        
        Args:
            text (str): The text to sanitize
            
        Returns:
            str: Sanitized text
        """
        if not text:
            return ""
        
        # Remove script tags and JavaScript
        for pattern in self.forbidden_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
