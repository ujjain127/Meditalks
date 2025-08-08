"""
Cultural Adaptation Service for MediTalks
Handles culturally sensitive medical message adaptation using Google Gemini AI
"""

import os
import logging
import google.generativeai as genai
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class CulturalAdaptationService:
    """Service for generating culturally adapted medical messages"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model = None
        self._initialize_gemini()
        
        # Cultural context templates
        self.context_templates = {
            'tagalog-rural': {
                'language': 'Tagalog/Filipino',
                'cultural_notes': 'Rural Philippines, traditional family values, respect for elders, community-oriented healthcare',
                'communication_style': 'Respectful, family-inclusive, uses local terms and metaphors'
            },
            'thai-low-literacy': {
                'language': 'Thai',
                'cultural_notes': 'Low literacy population, Buddhist influences, traditional medicine awareness',
                'communication_style': 'Simple language, visual metaphors, respectful tone'
            },
            'khmer-indigenous': {
                'language': 'Khmer/Cambodian', 
                'cultural_notes': 'Indigenous communities, traditional healing practices, Buddhist beliefs',
                'communication_style': 'Community-centered, respectful of traditional practices'
            },
            'vietnamese-elderly': {
                'language': 'Vietnamese',
                'cultural_notes': 'Elderly population, Confucian values, family hierarchy, traditional medicine',
                'communication_style': 'Highly respectful, family-oriented, acknowledges traditional practices'
            },
            'malay-traditional': {
                'language': 'Malay/Bahasa Melayu',
                'cultural_notes': 'Traditional Malay communities, Islamic influences, family-centered care',
                'communication_style': 'Respectful, Islamic-appropriate, family-inclusive'
            }
        }
    
    def _initialize_gemini(self):
        """Initialize Google Gemini AI"""
        try:
            if not self.api_key:
                logger.error("GEMINI_API_KEY not found in environment variables")
                return False
            
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Gemini AI initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI: {str(e)}")
            return False
    
    def generate_adaptation(self, message: str, cultural_context: str) -> str:
        """
        Generate culturally adapted medical message
        
        Args:
            message (str): Original medical message
            cultural_context (str): Target cultural context
            
        Returns:
            str: Culturally adapted message
        """
        try:
            if not self.model:
                logger.warning("Gemini AI not available, using fallback adaptation")
                return self._fallback_adaptation(message, cultural_context)
            
            context_info = self.context_templates.get(cultural_context, {})
            
            if not context_info:
                logger.warning(f"Unknown cultural context: {cultural_context}")
                return self._fallback_adaptation(message, cultural_context)
            
            # Construct prompt for Gemini
            prompt = self._build_adaptation_prompt(message, context_info)
            
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            
            if response.text:
                adapted_message = response.text.strip()
                logger.info(f"Successfully adapted message for {cultural_context}")
                return adapted_message
            else:
                logger.warning("Gemini returned empty response")
                return self._fallback_adaptation(message, cultural_context)
                
        except Exception as e:
            logger.error(f"Error generating adaptation with Gemini: {str(e)}")
            return self._fallback_adaptation(message, cultural_context)
    
    def _build_adaptation_prompt(self, message: str, context_info: Dict[str, str]) -> str:
        """Build prompt for Gemini AI"""
        language = context_info.get('language', 'English')
        cultural_notes = context_info.get('cultural_notes', '')
        communication_style = context_info.get('communication_style', '')
        
        prompt = f"""
You are a medical communication expert specializing in culturally sensitive healthcare messaging.

Task: Adapt the following medical message for a specific cultural context. Respond ONLY in {language}.

Original Message: "{message}"

Target Culture Information:
- Language: {language}
- Cultural Context: {cultural_notes}
- Communication Style: {communication_style}

Instructions:
1. Translate and adapt the message to be culturally appropriate
2. Use respectful, clear language appropriate for the target audience
3. Consider cultural beliefs and healthcare practices
4. Maintain the essential medical information while making it culturally sensitive
5. If applicable, acknowledge traditional practices respectfully
6. Use appropriate honorifics and respectful tone

Provide ONLY the adapted message in {language}. Do not use English or provide explanations.
"""
        return prompt
    
    def _fallback_adaptation(self, message: str, cultural_context: str) -> str:
        """Fallback adaptation when Gemini AI is not available"""
        context_info = self.context_templates.get(cultural_context, {})
        language = context_info.get('language', 'English')
        
        # Simple template-based adaptation
        adaptations = {
            'tagalog-rural': f"Mahalagang paalala tungkol sa inyong kalusugan: {message}\n\nPakisuyo, kumonsulta sa inyong doktor.",
            'thai-low-literacy': f"คำแนะนำสำคัญเกี่ยวกับสุขภาพ: {message}\n\nโปรดปรึกษาแพทย์",
            'khmer-indigenous': f"ការណែនាំសំខាន់អំពីសុខភាព: {message}\n\nសូមពិគ្រោះជាមួយវេជ្ជបណ្ឌិត",
            'vietnamese-elderly': f"Lời khuyên quan trọng về sức khỏe: {message}\n\nXin hãy tham khảo ý kiến bác sĩ",
            'malay-traditional': f"Nasihat penting mengenai kesihatan: {message}\n\nSila rujuk doktor"
        }
        
        adapted = adaptations.get(cultural_context, f"Important health advice: {message}\n\nPlease consult with your doctor.")
        
        logger.info(f"Used fallback adaptation for {cultural_context}")
        return adapted
    
    def get_supported_contexts(self) -> Dict[str, Any]:
        """Get list of supported cultural contexts"""
        return {
            context: {
                'language': info['language'],
                'description': info['cultural_notes']
            }
            for context, info in self.context_templates.items()
        }
