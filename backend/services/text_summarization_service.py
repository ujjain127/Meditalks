"""
Text Summarization Service for MediTalks
Handles text analysis and summarization using various methods
"""

import os
import logging
import google.generativeai as genai
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class TextSummarizationService:
    """Service for text analysis and summarization"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model = None
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize Google Gemini AI"""
        try:
            logger.info(f"Initializing Gemini AI...")
            logger.info(f"API key present: {bool(self.api_key)}")
            logger.info(f"API key length: {len(self.api_key) if self.api_key else 0}")
            
            if not self.api_key:
                logger.error("GEMINI_API_KEY not found in environment variables")
                return False
            
            genai.configure(api_key=self.api_key)
            
            # Try to list available models
            try:
                models = genai.list_models()
                logger.info(f"Available models: {[model.name for model in models]}")
            except Exception as e:
                logger.warning(f"Could not list models: {e}")
            
            # Try different model names
            model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
            
            for model_name in model_names:
                try:
                    logger.info(f"Trying model: {model_name}")
                    self.model = genai.GenerativeModel(model_name)
                    
                    # Test the connection
                    test_response = self.model.generate_content("Test connection")
                    logger.info(f"Test connection successful with {model_name}: {bool(test_response.text)}")
                    logger.info("Gemini AI initialized for text summarization")
                    return True
                    
                except Exception as e:
                    logger.warning(f"Failed to initialize with {model_name}: {str(e)}")
                    continue
            
            logger.error("Failed to initialize with any available model")
            return False
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI: {str(e)}")
            return False
    
    def analyze_and_summarize(self, text: str, target_language: str = 'en', summary_length: str = 'medium') -> Dict[str, Any]:
        """
        Analyze and summarize text content
        
        Args:
            text (str): Text to analyze and summarize
            target_language (str): Target language for summary
            summary_length (str): Length of summary ('short', 'medium', 'long')
            
        Returns:
            Dict containing analysis results
        """
        try:
            if not text or len(text.strip()) < 10:
                return {
                    'success': False,
                    'error': 'Text too short for analysis',
                    'summary': '',
                    'key_points': [],
                    'word_count': 0
                }
            
            # Basic analysis
            word_count = len(text.split())
            char_count = len(text)
            
            # Generate summary
            summary = self._generate_summary(text, target_language, summary_length)
            
            # Extract key points
            key_points = self._extract_key_points(text, target_language)
            
            return {
                'success': True,
                'summary': summary,
                'key_points': key_points,
                'word_count': word_count,
                'char_count': char_count,
                'summary_length': summary_length,
                'target_language': target_language
            }
            
        except Exception as e:
            logger.error(f"Error in analyze_and_summarize: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'summary': self._fallback_summary(text),
                'key_points': [],
                'word_count': len(text.split()) if text else 0
            }
    
    def _generate_summary(self, text: str, target_language: str, summary_length: str) -> str:
        """Generate summary using Gemini AI or fallback method"""
        try:
            logger.info(f"_generate_summary called with language: {target_language}, length: {summary_length}")
            logger.info(f"Text length to summarize: {len(text)}")
            logger.info(f"Model available: {self.model is not None}")
            
            if not self.model:
                logger.warning("No Gemini model available, using fallback")
                return self._fallback_summary(text)
            
            # Determine summary parameters
            length_instructions = {
                'short': '1-2 sentences',
                'medium': '3-4 sentences', 
                'long': '5-6 sentences'
            }
            
            length_instruction = length_instructions.get(summary_length, '3-4 sentences')
            
            # Language names for better prompting
            language_names = {
                'en': 'English',
                'th': 'Thai',
                'vi': 'Vietnamese',
                'ms': 'Malay',
                'km': 'Khmer',
                'tl': 'Tagalog',
                'hi': 'Hindi',
                'te': 'Telugu',
                'ta': 'Tamil',
                'kn': 'Kannada',
                'bn': 'Bengali'
            }
            
            language_name = language_names.get(target_language, 'English')
            
            prompt = f"""
Summarize the following text in {language_name} ONLY. Do not use English in your response.
The summary should be {length_instruction} long and focus on the most important medical information.
If this is medical content, prioritize key medical information, instructions, and important health details.

Write everything in {language_name} only.

Text to summarize:
{text[:2000]}  # Limit for API efficiency
"""
            
            logger.info(f"Sending prompt to Gemini AI...")
            response = self.model.generate_content(prompt)
            logger.info(f"Gemini AI response received: {response.text[:100] if response.text else 'No response text'}")
            
            if response.text:
                return response.text.strip()
            else:
                logger.warning("Gemini AI returned empty response, using fallback")
                return self._fallback_summary(text)
                
        except Exception as e:
            logger.error(f"Error generating summary with Gemini: {str(e)}")
            return self._fallback_summary(text)
    
    def _extract_key_points(self, text: str, target_language: str) -> list:
        """Extract key points from text"""
        try:
            if not self.model:
                return self._fallback_key_points(text)
            
            language_names = {
                'en': 'English',
                'th': 'Thai', 
                'vi': 'Vietnamese',
                'ms': 'Malay',
                'km': 'Khmer',
                'tl': 'Tagalog'
            }
            
            language_name = language_names.get(target_language, 'English')
            
            prompt = f"""
Extract 3-5 key points from the following text in {language_name} ONLY. Do not use English.
Format as a bullet-point list. Focus on the most important information.
If this is medical content, prioritize medical instructions, warnings, and key health information.

Write everything in {language_name} only.

Text:
{text[:2000]}
"""
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                # Parse bullet points
                points = []
                lines = response.text.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line and (line.startswith('•') or line.startswith('-') or line.startswith('*')):
                        # Remove bullet point markers
                        clean_point = line.lstrip('•-*').strip()
                        if clean_point:
                            points.append(clean_point)
                
                return points[:5]  # Limit to 5 points
            else:
                return self._fallback_key_points(text)
                
        except Exception as e:
            logger.error(f"Error extracting key points with Gemini: {str(e)}")
            return self._fallback_key_points(text)
    
    def _fallback_summary(self, text: str) -> str:
        """Simple fallback summary method"""
        if not text:
            return "No content to summarize."
        
        # Simple approach: take first few sentences
        sentences = []
        current_sentence = ""
        
        for char in text:
            current_sentence += char
            if char in '.!?':
                sentences.append(current_sentence.strip())
                current_sentence = ""
                if len(sentences) >= 3:
                    break
        
        summary = ' '.join(sentences).strip()
        
        if len(summary) > 300:
            summary = summary[:300] + "..."
        
        return summary or "Content processed successfully."
    
    def _fallback_key_points(self, text: str) -> list:
        """Simple fallback key points extraction"""
        if not text:
            return []
        
        # Simple approach: extract sentences with medical keywords
        medical_keywords = [
            'medication', 'dose', 'treatment', 'doctor', 'hospital', 
            'symptoms', 'diagnosis', 'prescription', 'important', 'warning'
        ]
        
        sentences = text.split('.')
        key_points = []
        
        for sentence in sentences[:10]:  # Check first 10 sentences
            sentence = sentence.strip()
            if any(keyword.lower() in sentence.lower() for keyword in medical_keywords):
                if len(sentence) > 10 and len(sentence) < 200:
                    key_points.append(sentence)
                    if len(key_points) >= 3:
                        break
        
        # If no medical keywords found, take first 3 meaningful sentences
        if not key_points:
            for sentence in sentences[:5]:
                sentence = sentence.strip()
                if len(sentence) > 20:
                    key_points.append(sentence)
                    if len(key_points) >= 3:
                        break
        
        return key_points
