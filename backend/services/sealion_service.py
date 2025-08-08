"""
SEA-Lion API Service for MediTalks
Handles cultural adaptation using SEA-Lion LLM specifically designed for Southeast Asian contexts
"""

import os
import logging
import requests
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SEALionService:
    def __init__(self):
        self.api_key = os.getenv('SEALION_API_KEY')
        self.api_url = os.getenv('SEALION_API_URL', 'https://api.sealion.ai/v1')
        self.available = self._initialize_sealion()
        
        # SEA-Lion specific cultural context templates optimized for Southeast Asian cultures
        self.sea_context_templates = {
            'tagalog-rural': {
                'language': 'Filipino/Tagalog',
                'cultural_notes': 'Rural Filipino community with strong family values, Catholic influences, and traditional healing practices',
                'communication_style': 'Respectful, family-oriented, uses "po" and "opo" for respect',
                'medical_considerations': 'Family involvement in decisions, traditional and modern medicine integration'
            },
            'thai-low-literacy': {
                'language': 'Thai',
                'cultural_notes': 'Buddhist Thai community with low literacy, prefers simple language and visual communication',
                'communication_style': 'Simple, respectful, uses appropriate Buddhist terminology',
                'medical_considerations': 'Simple explanations, traditional medicine awareness, hierarchical respect'
            },
            'khmer-indigenous': {
                'language': 'Khmer/Cambodian',
                'cultural_notes': 'Indigenous Khmer community with strong Buddhist beliefs and traditional practices',
                'communication_style': 'Community-oriented, oral tradition, respectful of traditional healers',
                'medical_considerations': 'Traditional healing integration, community consensus in decisions'
            },
            'vietnamese-elderly': {
                'language': 'Vietnamese',
                'cultural_notes': 'Elderly Vietnamese with Confucian values and family-centered healthcare',
                'communication_style': 'Formal, hierarchical respect, family involvement',
                'medical_considerations': 'Intergenerational healthcare decisions, traditional medicine integration'
            },
            'malay-traditional': {
                'language': 'Malay/Bahasa Melayu',
                'cultural_notes': 'Traditional Malay community with Islamic influences and family involvement',
                'communication_style': 'Islamic considerations, gender-appropriate, family-oriented',
                'medical_considerations': 'Halal considerations, Islamic medical ethics, family involvement'
            }
        }

    def _initialize_sealion(self) -> bool:
        """Initialize SEA-Lion API connection"""
        try:
            logger.info("Initializing SEA-Lion API...")
            logger.info(f"API key present: {bool(self.api_key)}")
            
            if not self.api_key or self.api_key == "your_sealion_api_key_here":
                logger.warning("SEA-Lion API key not configured, will use fallback")
                return False
            
            # Test connection
            test_response = self._make_api_request("Test connection", "en", max_tokens=10)
            logger.info(f"SEA-Lion API connection successful: {bool(test_response)}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize SEA-Lion API: {str(e)}")
            return False

    def _make_api_request(self, prompt: str, language: str = "en", max_tokens: int = 500) -> Optional[str]:
        """Make request to SEA-Lion API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # SEA-Lion API payload structure (adjust based on actual API documentation)
            payload = {
                "model": "sealion-7b-instruct",  # or appropriate model name
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "language": language
            }
            
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                logger.error(f"SEA-Lion API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error making SEA-Lion API request: {str(e)}")
            return None

    def generate_cultural_adaptation(self, message: str, cultural_context: str) -> str:
        """
        Generate culturally adapted medical message using SEA-Lion
        
        Args:
            message (str): Original medical message
            cultural_context (str): Target cultural context
            
        Returns:
            str: Culturally adapted message
        """
        try:
            if not self.available:
                return self._fallback_adaptation(message, cultural_context)
            
            context_info = self.sea_context_templates.get(cultural_context, {})
            if not context_info:
                logger.warning(f"Unknown cultural context for SEA-Lion: {cultural_context}")
                return self._fallback_adaptation(message, cultural_context)
            
            # Build SEA-Lion specific prompt optimized for Southeast Asian cultural adaptation
            prompt = self._build_sealion_prompt(message, context_info)
            
            # Get language code for API
            language_code = self._get_language_code(context_info.get('language', 'English'))
            
            logger.info(f"Generating cultural adaptation with SEA-Lion for {cultural_context}")
            response = self._make_api_request(prompt, language_code, max_tokens=800)
            
            if response and response.strip():
                logger.info(f"Successfully adapted message with SEA-Lion for {cultural_context}")
                return response.strip()
            else:
                logger.warning("SEA-Lion returned empty response, using fallback")
                return self._fallback_adaptation(message, cultural_context)
                
        except Exception as e:
            logger.error(f"Error generating adaptation with SEA-Lion: {str(e)}")
            return self._fallback_adaptation(message, cultural_context)

    def _build_sealion_prompt(self, message: str, context_info: Dict[str, str]) -> str:
        """Build SEA-Lion specific prompt for cultural adaptation"""
        language = context_info.get('language', 'English')
        cultural_notes = context_info.get('cultural_notes', '')
        communication_style = context_info.get('communication_style', '')
        medical_considerations = context_info.get('medical_considerations', '')
        
        return f"""As a medical communication expert specializing in Southeast Asian cultures, please adapt the following medical message for the specified cultural context.

Target Language: {language}
Cultural Context: {cultural_notes}
Communication Style: {communication_style}
Medical Considerations: {medical_considerations}

Original Medical Message:
"{message}"

Instructions:
1. Translate and adapt the message to {language} if not already in that language
2. Use culturally appropriate communication style and terminology
3. Consider the specific cultural and medical considerations mentioned
4. Ensure the medical information remains accurate while being culturally sensitive
5. Include any necessary cultural context or explanations
6. Use respectful and appropriate language for the target community

Please provide the culturally adapted message in {language}:"""

    def _get_language_code(self, language: str) -> str:
        """Map language names to API language codes"""
        language_mapping = {
            'Filipino/Tagalog': 'tl',
            'Thai': 'th',
            'Khmer/Cambodian': 'km',
            'Vietnamese': 'vi',
            'Malay/Bahasa Melayu': 'ms',
            'English': 'en'
        }
        return language_mapping.get(language, 'en')

    def _fallback_adaptation(self, message: str, cultural_context: str) -> str:
        """Fallback adaptation when SEA-Lion is not available"""
        context_info = self.sea_context_templates.get(cultural_context, {})
        language = context_info.get('language', 'English')
        
        # Simple fallback adaptations
        fallback_adaptations = {
            'tagalog-rural': f"Mahalagang payo sa kalusugan: {message}\n\nPakipag-usap sa inyong doktor para sa karagdagang impormasyon.",
            'thai-low-literacy': f"คำแนะนำสำคัญเกี่ยวกับสุขภาพ: {message}\n\nกรุณาปรึกษาแพทย์สำหรับข้อมูลเพิ่มเติม",
            'khmer-indigenous': f"ដំបូន្មានសុខភាពសំខាន់: {message}\n\nសូមពិគ្រោះជាមួយគ្រូពេទ្យសម្រាប់ព័ត៌មានបន្ថែម",
            'vietnamese-elderly': f"Lời khuyên sức khỏe quan trọng: {message}\n\nVui lòng tham khảo ý kiến bác sĩ để biết thêm thông tin",
            'malay-traditional': f"Nasihat kesihatan penting: {message}\n\nSila rujuk doktor untuk maklumat lanjut"
        }
        
        adapted = fallback_adaptations.get(cultural_context, f"Important health advice: {message}\n\nPlease consult with your doctor for more information.")
        logger.info(f"Used fallback adaptation for {cultural_context}")
        return adapted

    def generate_pdf_summary(self, text: str, cultural_context: str, target_language: str = 'en') -> str:
        """
        Generate culturally adapted PDF summary using SEA-Lion
        
        Args:
            text (str): PDF text content
            cultural_context (str): Cultural context
            target_language (str): Target language code
            
        Returns:
            str: Culturally adapted summary
        """
        try:
            if not self.available:
                return self._fallback_summary(text, cultural_context, target_language)
            
            context_info = self.sea_context_templates.get(cultural_context, {})
            
            # Build prompt for PDF summarization
            prompt = f"""As a medical communication expert for Southeast Asian communities, please summarize the following medical document and adapt it for the specified cultural context.

Target Language: {target_language}
Cultural Context: {context_info.get('cultural_notes', 'General healthcare context')}
Communication Style: {context_info.get('communication_style', 'Clear and respectful')}

Document Content:
{text[:2000]}  # Limit content for API

Please provide:
1. A clear summary of the key medical information
2. Culturally appropriate explanations
3. Any important warnings or instructions
4. Language adapted for the target community

Summary in {target_language}:"""

            response = self._make_api_request(prompt, target_language, max_tokens=1000)
            
            if response and response.strip():
                return response.strip()
            else:
                return self._fallback_summary(text, cultural_context, target_language)
                
        except Exception as e:
            logger.error(f"Error generating PDF summary with SEA-Lion: {str(e)}")
            return self._fallback_summary(text, cultural_context, target_language)

    def _fallback_summary(self, text: str, cultural_context: str, target_language: str) -> str:
        """Fallback summary when SEA-Lion is not available"""
        # Extract first few sentences
        sentences = text.split('.')[:3]
        summary = '. '.join(sentences).strip()
        
        if len(summary) > 300:
            summary = summary[:300] + "..."
        
        return summary or "Medical document processed successfully."

    def is_available(self) -> bool:
        """Check if SEA-Lion service is available"""
        return self.available

    def get_supported_contexts(self) -> list:
        """Get list of supported cultural contexts"""
        return list(self.sea_context_templates.keys())
