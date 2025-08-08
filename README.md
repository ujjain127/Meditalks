# MediTalks
## Adaptive Cultural Contextualization Engine for Medical Communications

### Overview

MediTalks is a sophisticated web application designed to bridge cultural and linguistic gaps in medical communication across Southeast Asian communities. The platform leverages advanced AI technology to provide culturally sensitive medical message adaptation, ensuring effective healthcare communication for diverse populations.

### Key Features

**Cultural Adaptation Engine**
- Contextual adaptation for five Southeast Asian cultural groups
- Support for Tagalog (Rural Philippines), Thai (Low Literacy), Khmer (Indigenous Communities), Vietnamese (Elderly), and Malay (Traditional Communities)
- AI-powered cultural sensitivity analysis

**Multi-Language Support**
- Translation and adaptation for six languages: English, Thai, Vietnamese, Malay, Khmer, and Tagalog
- Native language output with cultural context preservation
- Literacy-level appropriate messaging

**Document Processing**
- PDF document analysis and extraction
- Medical terminology identification
- Cultural adaptation of complex medical documents
- Structured output with key terms and summaries

**AI Integration**
- Google Gemini AI integration for enhanced cultural adaptation
- Fallback system ensuring continuous operation
- Real-time API health monitoring

### Technical Architecture

**Frontend**
- React.js application with modern ES6+ features
- Responsive design optimized for healthcare environments
- Clean, minimalist interface inspired by professional design standards
- Real-time error handling and user feedback

**Backend**
- Flask-based Python backend with RESTful API
- Modular service architecture for scalability
- Google Gemini AI integration for natural language processing
- Comprehensive error handling and logging

**Core Services**
- Cultural Adaptation Service: AI-powered message contextualization
- PDF Processing Service: Document extraction and analysis
- Text Summarization Service: Medical content summarization
- Validation Service: Input validation and quality assurance

### Installation and Setup

**Prerequisites**
- Node.js 16+ and npm
- Python 3.8+
- Google Gemini API key (free tier available)

**Frontend Setup**
```bash
cd meditalks
npm install
npm start
```

**Backend Setup**
```bash
cd backend
pip install -r requirements.txt
# Configure environment variables in .env file
python app.py
```

**Environment Configuration**
Create a `.env` file in the backend directory:
```
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
GEMINI_API_KEY=your_gemini_api_key_here
```

### API Documentation

**Cultural Adaptation Endpoint**
```
POST /api/cultural-adaptation/generate
Content-Type: application/json

{
  "message": "Take your medication twice daily",
  "context": "thai-low-literacy"
}
```

**PDF Processing Endpoint**
```
POST /api/extract-pdf
Content-Type: multipart/form-data

pdf: [PDF file]
context: "tagalog-rural"
target_language: "tl"
```

**Health Check Endpoint**
```
GET /api/health
```

### Supported Cultural Contexts

**Tagalog (Rural Philippines)**
- Simple, family-oriented language
- Emphasis on elder respect and community support
- Integration with traditional Filipino healthcare practices

**Thai (Low Literacy)**
- Visual aids and simple terminology
- Respectful hierarchy awareness
- Step-by-step instruction format

**Khmer (Indigenous Communities)**
- Traditional medicine integration
- Cultural practice acknowledgment
- Respectful approach to indigenous beliefs

**Vietnamese (Elderly)**
- Formal honorific language
- Life experience references
- Traditional value integration

**Malay (Traditional Communities)**
- Islamic cultural considerations
- Traditional-modern healthcare balance
- Community-centered approach

### Development Guidelines

**Code Quality**
- Follow PEP 8 standards for Python code
- Use ESLint and Prettier for JavaScript formatting
- Comprehensive error handling and logging
- Unit tests for critical functions

**Security Considerations**
- API key management through environment variables
- Input validation and sanitization
- CORS configuration for cross-origin requests
- Rate limiting for API endpoints

**Performance Optimization**
- Efficient PDF processing with streaming
- Caching for frequent cultural adaptations
- Minimal bundle size for frontend assets
- Database query optimization

### Contributing

We welcome contributions to improve MediTalks. Please follow these guidelines:

1. Fork the repository and create a feature branch
2. Ensure all tests pass and code follows style guidelines
3. Add comprehensive documentation for new features
4. Submit a pull request with detailed description of changes

### License

This project is licensed under the MIT License. See LICENSE file for details.

### Support and Contact

For technical support, feature requests, or general inquiries:
- Documentation: See GEMINI_SETUP.md for detailed AI integration setup
- Issues: Use GitHub Issues for bug reports and feature requests
- Development: Follow semantic versioning for releases

### Acknowledgments

Built with modern web technologies and powered by Google Gemini AI for enhanced cultural adaptation capabilities. Special consideration given to Southeast Asian cultural diversity and healthcare communication needs.