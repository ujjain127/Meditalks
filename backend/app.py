from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
from werkzeug.utils import secure_filename

# Import our services
from services.cultural_adaptation_service import CulturalAdaptationService
from services.validation_service import ValidationService
from services.pdf_processing_service import PDFProcessingService
from services.text_summarization_service import TextSummarizationService
from services.sealion_service import SEALionService
from utils.error_handler import handle_error
from config.cultural_contexts import CULTURAL_CONTEXTS

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS - Allow multiple frontend URLs
allowed_origins = [
    'http://localhost:3000',
    'http://localhost:3001', 
    'http://localhost:3002',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:3001',
    'http://127.0.0.1:3002',
    # Add production frontend URLs (update these with your actual Render URLs)
    'https://meditalks-frontend.onrender.com',
    'https://your-frontend-name.onrender.com'
]
CORS(app, origins=allowed_origins)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
cultural_service = CulturalAdaptationService()
validation_service = ValidationService()
pdf_service = PDFProcessingService()
summarization_service = TextSummarizationService()
sealion_service = SEALionService()

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'MediTalks Backend API',
        'status': 'running',
        'version': '1.0.0',
        'endpoints': [
            '/api/health',
            '/api/cultural-adaptation/generate',
            '/api/cultural-adaptation/contexts',
            '/api/extract-pdf',
            '/api/document/upload',
            '/api/document/analyze',
            '/api/document/process'
        ]
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.now().isoformat(),
        'service': 'MediTalks Backend',
        'version': '1.0.0',
        'ai_services': {
            'sealion_available': sealion_service.is_available(),
            'gemini_available': cultural_service.ai_available if hasattr(cultural_service, 'ai_available') else False,
            'primary_service': 'SEA-Lion' if sealion_service.is_available() else 'Gemini'
        }
    }), 200

@app.route('/api/cultural-adaptation/generate', methods=['POST'])
def generate_adaptation():
    """Generate culturally adapted medical message"""
    try:
        # Get request data
        data = request.get_json()
        logger.info(f"Received adaptation request: {data}")
        
        if not data:
            return jsonify({
                'success': False,
                'error': {'message': 'No JSON data provided'}
            }), 400
        
        message = data.get('message', '').strip()
        context = data.get('context', '').strip()
        
        # Validate input
        if not message:
            return jsonify({
                'success': False,
                'error': {'message': 'Message is required'}
            }), 400
            
        if not context:
            return jsonify({
                'success': False,
                'error': {'message': 'Cultural context is required'}
            }), 400
        
        # Validate message length
        validation_result = validation_service.validate_message(message)
        if not validation_result['valid']:
            return jsonify({
                'success': False,
                'error': {'message': validation_result['message']}
            }), 400
        
        # Generate adaptation - use SEA-Lion if available, fallback to Gemini
        if sealion_service.is_available():
            logger.info("Using SEA-Lion for cultural adaptation")
            adapted_message = sealion_service.generate_cultural_adaptation(message, context)
        else:
            logger.info("Using Gemini for cultural adaptation")
            adapted_message = cultural_service.generate_adaptation(message, context)
        
        return jsonify({
            'success': True,
            'data': {
                'adaptedMessage': adapted_message,
                'originalMessage': message,
                'culturalContext': context,
                'timestamp': datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in generate_adaptation: {str(e)}")
        return handle_error(e)

@app.route('/api/cultural-adaptation/contexts', methods=['GET'])
def get_cultural_contexts():
    """Get available cultural contexts"""
    try:
        return jsonify({
            'success': True,
            'data': {
                'contexts': CULTURAL_CONTEXTS
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_cultural_contexts: {str(e)}")
        return handle_error(e)

@app.route('/api/extract-pdf', methods=['POST'])
def extract_pdf():
    """Extract and culturally adapt PDF content"""
    try:
        # Check if file is present
        if 'pdf' not in request.files:
            return jsonify({
                'success': False,
                'error': {'message': 'No PDF file uploaded'}
            }), 400
        
        file = request.files['pdf']
        context = request.form.get('context', 'general')
        target_language = request.form.get('target_language', 'en')
        
        logger.info(f"Processing PDF: {file.filename}, context: {context}, language: {target_language}")
        
        # Extract text from PDF
        extraction_result = pdf_service.extract_text_from_pdf(file, target_language)
        
        if not extraction_result['success']:
            return jsonify({
                'success': False,
                'error': {'message': f"PDF extraction failed: {extraction_result['error']}"}
            }), 400
        
        extracted_text = extraction_result['text']
        
        # Generate detailed summary with explanations - use SEA-Lion if available
        logger.info(f"Calling summarization service for text length: {len(extracted_text)}")
        logger.info(f"Target language: {target_language}")
        
        if sealion_service.is_available():
            logger.info("Using SEA-Lion for PDF summarization")
            summary = sealion_service.generate_pdf_summary(
                text=extracted_text,
                cultural_context=context,
                target_language=target_language
            )
            summary_result = {'summary': summary}
        else:
            logger.info("Using Gemini for PDF summarization")
            summary_result = summarization_service.analyze_and_summarize(
                text=extracted_text,
                target_language=target_language,
                summary_length='long'
            )
        
        logger.info(f"Summary result: {summary_result}")
        
        # Build simplified response with only summary
        response_data = {
            'summary': summary_result.get('summary', 'Content extracted successfully'),
            'fileName': file.filename,
            'detectedLanguage': extraction_result.get('detected_language', 'English'),
            'outputLanguage': target_language,
            'wordCount': len(extracted_text.split()),
            'culturalContext': context
        }
        
        return jsonify({
            'success': True,
            'data': response_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error in extract_pdf: {str(e)}")
        return handle_error(e)

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': {
            'message': 'Endpoint not found',
            'code': 404
        }
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': {
            'message': 'Internal server error',
            'code': 500
        }
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    logger.info(f"MediTalks Backend starting on port {port}")
    logger.info(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    logger.info(f"CORS enabled for: {allowed_origins}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
