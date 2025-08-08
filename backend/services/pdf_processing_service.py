"""
PDF Processing Service for MediTalks
Handles PDF text extraction and processing using Google Gemini AI
"""

import os
import logging
import PyPDF2
import pdfplumber
import google.generativeai as genai
from typing import Dict, Any, Optional
from io import BytesIO
from langdetect import detect, DetectorFactory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set seed for consistent language detection
DetectorFactory.seed = 0

logger = logging.getLogger(__name__)

class PDFProcessingService:
    """Service for processing PDF documents and extracting text"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model = None
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize Google Gemini AI for PDF processing"""
        try:
            if not self.api_key:
                logger.error("GEMINI_API_KEY not found in environment variables")
                return False
            
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Gemini AI initialized for PDF processing")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI: {str(e)}")
            return False
    
    def extract_text_from_pdf(self, file, target_language: str = 'en') -> Dict[str, Any]:
        """
        Extract text from PDF file
        
        Args:
            file: PDF file object
            target_language (str): Target language code
            
        Returns:
            Dict containing extraction result
        """
        try:
            # Reset file pointer
            file.seek(0)
            
            # Try pdfplumber first (better for complex layouts)
            extracted_text = self._extract_with_pdfplumber(file)
            
            if not extracted_text or len(extracted_text.strip()) < 10:
                # Fallback to PyPDF2
                file.seek(0)
                extracted_text = self._extract_with_pypdf2(file)
            
            if not extracted_text or len(extracted_text.strip()) < 10:
                return {
                    'success': False,
                    'error': 'Could not extract text from PDF',
                    'text': ''
                }
            
            # Detect language
            detected_language = self._detect_language(extracted_text)
            
            # Clean and process text
            cleaned_text = self._clean_text(extracted_text)
            
            return {
                'success': True,
                'text': cleaned_text,
                'detected_language': detected_language,
                'word_count': len(cleaned_text.split()),
                'char_count': len(cleaned_text)
            }
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'text': ''
            }
    
    def _extract_with_pdfplumber(self, file) -> str:
        """Extract text using pdfplumber"""
        try:
            text_content = []
            
            with pdfplumber.open(file) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text_content.append(page_text)
                        
                        # Limit to first 10 pages for performance
                        if page_num >= 9:
                            break
                            
                    except Exception as e:
                        logger.warning(f"Error extracting page {page_num + 1}: {str(e)}")
                        continue
            
            return '\n'.join(text_content)
            
        except Exception as e:
            logger.error(f"pdfplumber extraction failed: {str(e)}")
            return ""
    
    def _extract_with_pypdf2(self, file) -> str:
        """Extract text using PyPDF2 as fallback"""
        try:
            text_content = []
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Limit to first 10 pages
            max_pages = min(len(pdf_reader.pages), 10)
            
            for page_num in range(max_pages):
                try:
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
                        
                except Exception as e:
                    logger.warning(f"Error extracting page {page_num + 1}: {str(e)}")
                    continue
            
            return '\n'.join(text_content)
            
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {str(e)}")
            return ""
    
    def _detect_language(self, text: str) -> str:
        """Detect the language of extracted text"""
        try:
            if len(text.strip()) < 10:
                return "unknown"
            
            # Use first 1000 characters for detection
            sample_text = text[:1000]
            detected = detect(sample_text)
            
            # Map common language codes to full names
            language_map = {
                'en': 'English',
                'th': 'Thai',
                'vi': 'Vietnamese',
                'ms': 'Malay',
                'km': 'Khmer',
                'tl': 'Tagalog',
                'fil': 'Filipino'
            }
            
            return language_map.get(detected, detected)
            
        except Exception as e:
            logger.warning(f"Language detection failed: {str(e)}")
            return "unknown"
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        import re
        
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove excessive line breaks
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        
        # Clean up common PDF artifacts
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}\"\'\/\\\n]', ' ', text)
        
        return text.strip()
    
    def summarize_pdf_content(self, text: str, target_language: str = 'en') -> str:
        """
        Summarize PDF content using Gemini AI
        
        Args:
            text (str): Extracted text to summarize
            target_language (str): Target language for summary
            
        Returns:
            str: Summarized content
        """
        try:
            if not self.model:
                return self._simple_summary(text)
            
            prompt = f"""
Summarize the following medical document text in {target_language}. 
Focus on key medical information, instructions, and important details.
Keep the summary concise but comprehensive.

Text to summarize:
{text[:3000]}  # Limit text length for API
"""
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
            else:
                return self._simple_summary(text)
                
        except Exception as e:
            logger.error(f"Error summarizing with Gemini: {str(e)}")
            return self._simple_summary(text)
    
    def generate_detailed_explanation(self, text: str, cultural_context: str, target_language: str = 'en') -> str:
        """
        Generate detailed explanation of PDF content with cultural considerations
        
        Args:
            text (str): Extracted PDF text
            cultural_context (str): Cultural context for adaptation
            target_language (str): Target language for explanation
            
        Returns:
            str: Detailed explanation
        """
        try:
            if not self.model:
                return self._fallback_detailed_explanation(text, cultural_context)
            
            # Cultural context mapping for better prompting
            context_mapping = {
                'tagalog-rural': 'rural Filipino communities with traditional family values and respect for elders',
                'thai-low-literacy': 'Thai communities with limited literacy, Buddhist influences, and traditional medicine awareness',
                'khmer-indigenous': 'indigenous Khmer communities with strong Buddhist beliefs and traditional healing practices',
                'vietnamese-elderly': 'elderly Vietnamese population with Confucian values and family-centered healthcare',
                'malay-traditional': 'traditional Malay communities with Islamic influences and family-centered care'
            }
            
            context_description = context_mapping.get(cultural_context, 'general healthcare context')
            
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
You are a medical communication expert. Analyze the following medical document and provide a comprehensive summary ONLY in {language_name}. Do not use English in your response.

The target audience is: {context_description}

Medical Document Text:
{text[:3000]}

Provide a complete summary in {language_name} that includes:
1. What this medical document is about
2. Key medical information in simple terms
3. Important instructions for the patient/family
4. Any warnings or precautions
5. Cultural considerations for this community

Write everything in {language_name} only. Make it culturally appropriate and easy to understand.
"""
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
            else:
                return self._fallback_detailed_explanation(text, cultural_context)
                
        except Exception as e:
            logger.error(f"Error generating detailed explanation: {str(e)}")
            return self._fallback_detailed_explanation(text, cultural_context)
    
    def generate_cultural_solutions(self, text: str, cultural_context: str, target_language: str = 'en') -> list:
        """
        Generate actionable, culturally appropriate solutions based on PDF content
        
        Args:
            text (str): Extracted PDF text
            cultural_context (str): Cultural context for adaptation
            target_language (str): Target language for solutions
            
        Returns:
            list: List of actionable solutions
        """
        try:
            if not self.model:
                return self._fallback_solutions(text, cultural_context)
            
            context_mapping = {
                'tagalog-rural': 'rural Filipino families who value community input and respect traditional practices',
                'thai-low-literacy': 'Thai communities with limited literacy who prefer simple, visual explanations',
                'khmer-indigenous': 'indigenous Khmer communities who respect traditional healing alongside modern medicine',
                'vietnamese-elderly': 'elderly Vietnamese patients who prefer family involvement in healthcare decisions',
                'malay-traditional': 'traditional Malay families who consider Islamic principles in healthcare'
            }
            
            context_description = context_mapping.get(cultural_context, 'general healthcare context')
            
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
Based on this medical document, provide ONLY actionable solutions in {language_name} for: {context_description}

Medical Document:
{text[:2500]}

Provide 5-7 specific solutions in {language_name} that are:
1. Culturally appropriate and respectful
2. Practical and actionable
3. Consider family/community involvement
4. Respect traditional practices while emphasizing medical compliance
5. Include specific steps to take

Write ONLY in {language_name}. Format as a numbered list of clear action items.
"""
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                # Parse the solutions into a list
                solutions = []
                lines = response.text.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    # Look for numbered or bulleted items
                    if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                        # Clean up the solution text
                        clean_solution = line.lstrip('0123456789.-•').strip()
                        if clean_solution:
                            solutions.append(clean_solution)
                
                return solutions[:7]  # Limit to 7 solutions
            else:
                return self._fallback_solutions(text, cultural_context)
                
        except Exception as e:
            logger.error(f"Error generating cultural solutions: {str(e)}")
            return self._fallback_solutions(text, cultural_context)
    
    def extract_medical_concepts(self, text: str, target_language: str = 'en') -> Dict[str, list]:
        """
        Extract medical concepts, key terms, and instructions from PDF text
        
        Args:
            text (str): Extracted PDF text
            target_language (str): Target language for concepts
            
        Returns:
            Dict: Dictionary containing key_terms, medical_concepts, and instructions
        """
        try:
            if not self.model:
                return self._fallback_medical_concepts(text, target_language)
            
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
Analyze this medical document and extract key information in {language_name} ONLY. Do not use English.

Medical Document:
{text[:2500]}

Provide in {language_name}:
1. Key Medical Terms (5-8 important medical words/phrases)
2. Medical Concepts (3-5 main medical ideas or conditions)
3. Important Instructions (3-5 specific things the patient must do)

Format your response as:
KEY TERMS:
- term 1 in {language_name}
- term 2 in {language_name}

MEDICAL CONCEPTS:
- concept 1 in {language_name}
- concept 2 in {language_name}

INSTRUCTIONS:
- instruction 1 in {language_name}
- instruction 2 in {language_name}

Write everything in {language_name} only.
"""
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                return self._parse_medical_analysis(response.text)
            else:
                return self._fallback_medical_concepts(text)
                
        except Exception as e:
            logger.error(f"Error extracting medical concepts: {str(e)}")
            return self._fallback_medical_concepts(text, target_language)
    
    def _parse_medical_analysis(self, analysis_text: str) -> Dict[str, list]:
        """Parse the medical analysis response into structured data"""
        result = {
            'key_terms': [],
            'medical_concepts': [],
            'instructions': []
        }
        
        current_section = None
        lines = analysis_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if 'KEY TERMS' in line.upper():
                current_section = 'key_terms'
            elif 'MEDICAL CONCEPTS' in line.upper():
                current_section = 'medical_concepts'
            elif 'INSTRUCTIONS' in line.upper():
                current_section = 'instructions'
            elif line.startswith('-') or line.startswith('•') and current_section:
                clean_item = line.lstrip('-•').strip()
                if clean_item and current_section in result:
                    result[current_section].append(clean_item)
        
        return result
    
    def _fallback_detailed_explanation(self, text: str, cultural_context: str) -> str:
        """Fallback explanation when Gemini is not available"""
        explanations = {
            'tagalog-rural': f"Ang dokumentong ito ay naglalaman ng mahalagang impormasyon tungkol sa inyong kalusugan. Makipag-ugnayan sa inyong doktor para sa karagdagang paliwanag.",
            'thai-low-literacy': f"เอกสารนี้มีข้อมูลสำคัญเกี่ยวกับสุขภาพของคุณ กรุณาปรึกษาแพทย์เพื่อข้อมูลเพิ่มเติม",
            'khmer-indigenous': f"ឯកសារនេះមានព័ត៌មានសំខាន់អំពីសុខភាពរបស់អ្នក សូមពិគ្រោះជាមួយវេជ្ជបណ្ឌិតសម្រាប់ព័ត៌មានបន្ថែម",
            'vietnamese-elderly': f"Tài liệu này chứa thông tin quan trọng về sức khỏe của quý vị. Xin hãy tham khảo ý kiến bác sĩ để biết thêm chi tiết.",
            'malay-traditional': f"Dokumen ini mengandungi maklumat penting mengenai kesihatan anda. Sila rujuk doktor untuk maklumat lanjut."
        }
        
        return explanations.get(cultural_context, "Dokumen ini mengandungi maklumat penting mengenai kesihatan anda.")
    
    def _fallback_solutions(self, text: str, cultural_context: str) -> list:
        """Fallback solutions when Gemini is not available"""
        solutions_by_context = {
            'tagalog-rural': [
                "Makipag-ugnayan sa inyong doktor para sa personal na payo",
                "Sundin ang mga tagubilin sa paginom ng gamot",
                "Magtakda ng regular na appointment para sa follow-up",
                "Bantayan ang mga sintomas at iulat ang mga pagbabago",
                "Makipag-ugnayan sa inyong pamilya tungkol sa treatment plan"
            ],
            'thai-low-literacy': [
                "ปรึกษาแพทย์เพื่อรับคำแนะนำส่วนบุคคล",
                "ทานยาตามที่แพทย์สั่ง",
                "นัดหมายแพทย์เป็นประจำ",
                "สังเกตอาการและรายงานการเปลี่ยนแปลง",
                "ขอให้ครอบครัวช่วยจำรายละเอียดการรักษา"
            ],
            'khmer-indigenous': [
                "ពិគ្រោះជាមួយវេជ្ជបណ្ឌិតសម្រាប់ការណែនាំផ្ទាល់ខ្លួន",
                "ញ៉ាំថ្នាំតាមការណែនាំ",
                "កត់ត្រានៅវេជ្ជបណ្ឌិតជាទៀងទាត់",
                "សង្កេតមើលរោគសញ្ញានិងរាយការណ៍ការផ្លាស់ប្តូរ",
                "ពិភាក្សាជាមួយគ្រួសារអំពីផែនការព្យាបាល"
            ],
            'vietnamese-elderly': [
                "Tham khảo ý kiến bác sĩ để nhận tư vấn cá nhân",
                "Uống thuốc theo đúng chỉ định",
                "Đặt lịch tái khám định kỳ",
                "Theo dõi các triệu chứng và báo cáo thay đổi",
                "Thảo luận với gia đình về kế hoạch điều trị"
            ],
            'malay-traditional': [
                "Rujuk doktor untuk nasihat peribadi",
                "Ikut arahan pengambilan ubat",
                "Buat temujanji susulan berkala",
                "Pantau simptom dan laporkan perubahan",
                "Berbincang dengan keluarga mengenai rancangan rawatan"
            ]
        }
        
        return solutions_by_context.get(cultural_context, [
            "Rujuk doktor untuk maklumat lanjut",
            "Ikut semua arahan perubatan",
            "Pantau kesihatan dengan kerap"
        ])
    
    def _fallback_medical_concepts(self, text: str, target_language: str = 'en') -> Dict[str, list]:
        """Fallback medical concept extraction in appropriate language"""
        # Map language codes to cultural contexts for fallback
        language_to_context = {
            'tl': 'tagalog-rural',
            'th': 'thai-low-literacy', 
            'km': 'khmer-indigenous',
            'vi': 'vietnamese-elderly',
            'ms': 'malay-traditional',
            'en': 'malay-traditional'  # Default to Malay as fallback
        }
        
        context_key = language_to_context.get(target_language, 'malay-traditional')
        
        concepts_by_context = {
            'tagalog-rural': {
                'key_terms': ['gamot', 'doktor', 'ospital', 'sakit', 'lunas'],
                'medical_concepts': ['Pangangalaga ng kalusugan', 'Pagsunod sa gamot', 'Regular na checkup'],
                'instructions': ['Uminom ng gamot ayon sa tagubilin', 'Makipag-ugnayan sa doktor kung may tanong']
            },
            'thai-low-literacy': {
                'key_terms': ['ยา', 'หมอ', 'โรงพยาบาล', 'อาการ', 'การรักษา'],
                'medical_concepts': ['การดูแลสุขภาพ', 'การทานยา', 'การตรวจสุขภาพ'],
                'instructions': ['ทานยาตามแพทย์สั่ง', 'ติดต่อแพทย์หากมีข้อสงสัย']
            },
            'khmer-indigenous': {
                'key_terms': ['ថ្នាំ', 'វេជ្ជបណ្ឌិត', 'មន្ទីរពេទ្យ', 'រោគសញ្ញា', 'ការព្យាបាល'],
                'medical_concepts': ['ការថែទាំសុខភាព', 'ការញ៉ាំថ្នាំ', 'ការពិនិត្យសុខភាព'],
                'instructions': ['ញ៉ាំថ្នាំតាមការណែនាំ', 'ទាក់ទងវេជ្ជបណ្ឌិតប្រសិនបើមានសំណួរ']
            },
            'vietnamese-elderly': {
                'key_terms': ['thuốc', 'bác sĩ', 'bệnh viện', 'triệu chứng', 'điều trị'],
                'medical_concepts': ['Chăm sóc sức khỏe', 'Uống thuốc đúng cách', 'Khám sức khỏe định kỳ'],
                'instructions': ['Uống thuốc theo chỉ định', 'Liên hệ bác sĩ nếu có thắc mắc']
            },
            'malay-traditional': {
                'key_terms': ['ubat', 'doktor', 'hospital', 'simptom', 'rawatan'],
                'medical_concepts': ['Penjagaan kesihatan', 'Pengambilan ubat', 'Pemeriksaan kesihatan'],
                'instructions': ['Ambil ubat mengikut arahan', 'Hubungi doktor jika ada pertanyaan']
            }
        }
        
        return concepts_by_context.get(context_key, concepts_by_context['malay-traditional'])

    def _simple_summary(self, text: str) -> str:
        """Simple fallback summary"""
        if not text:
            return "No content to summarize."
        
        # Simple approach: take first few sentences
        sentences = text.split('.')[:3]
        summary = '. '.join(sentences).strip()
        
        if len(summary) > 200:
            summary = summary[:200] + "..."
        
        return summary or "Document content extracted successfully."
