# MediTalks with SEA-Lion API Integration

## Overview
MediTalks now supports **SEA-Lion API** for enhanced cultural adaptation specifically designed for Southeast Asian languages and cultures. SEA-Lion will be used as the primary AI service when available, with Gemini as a fallback.

## SEA-Lion API Setup

### 1. Get SEA-Lion API Access
SEA-Lion is developed by AI Singapore. To get access:

1. **Visit the official SEA-Lion website**: https://www.aisingapore.org/sea-lion/
2. **Request API access** through their official channels
3. **Alternative**: Check if SEA-Lion is available through:
   - Hugging Face Model Hub
   - AI Singapore's research platforms
   - Academic collaboration programs

### 2. Configure API Key
Once you have your SEA-Lion API key:

1. Open `backend/.env`
2. Replace `your_sealion_api_key_here` with your actual API key:
   ```
   SEALION_API_KEY="your_actual_api_key_here"
   ```

### 3. API Endpoint Configuration
Update the API URL in `.env` if different:
```
SEALION_API_URL="https://api.sealion.ai/v1"
```

## Features with SEA-Lion

### Cultural Adaptation
- **Optimized for Southeast Asian cultures**: Filipino, Thai, Vietnamese, Malay, Khmer
- **Cultural context understanding**: Traditional values, family structures, religious considerations
- **Language-specific communication styles**: Respectful hierarchies, traditional terminology

### PDF Summarization
- **Culturally adapted summaries** in target languages
- **Medical content** optimized for specific communities
- **Traditional medicine integration** awareness

### Supported Cultural Contexts
1. **Tagalog (Rural Philippines)** - Family-oriented, Catholic influences
2. **Thai (Low Literacy)** - Buddhist culture, simple language
3. **Khmer (Indigenous Communities)** - Traditional practices, oral tradition
4. **Vietnamese (Elderly)** - Confucian values, formal communication
5. **Malay (Traditional Communities)** - Islamic considerations, family involvement

## Fallback System

If SEA-Lion API is not available, the system automatically falls back to:
1. **Gemini AI** for general adaptations
2. **Local fallback** with pre-configured cultural templates

## Testing SEA-Lion Integration

1. **Start the backend**:
   ```bash
   cd backend
   python app.py
   ```

2. **Test backend connection** using the "Test Backend Connection" button in the frontend

3. **Check AI service status** - the test will show:
   - Primary AI service being used
   - SEA-Lion availability status
   - Gemini availability status

## API Usage Notes

### SEA-Lion API Structure
The integration assumes this API structure (adjust based on actual SEA-Lion API):
```json
{
  "model": "sealion-7b-instruct",
  "messages": [{"role": "user", "content": "prompt"}],
  "max_tokens": 500,
  "temperature": 0.7,
  "language": "tl"
}
```

### Language Codes
- `tl` - Filipino/Tagalog
- `th` - Thai
- `vi` - Vietnamese
- `ms` - Malay
- `km` - Khmer
- `en` - English

## Development vs Production

### Development
- Uses localhost endpoints
- Detailed logging for debugging
- Fallback systems active

### Production Deployment
1. **Environment Variables**:
   ```
   SEALION_API_KEY=your_production_key
   SEALION_API_URL=https://production.sealion.api/v1
   ```

2. **Error Handling**: Production-ready error handling for API failures

3. **Rate Limiting**: Consider implementing rate limiting for API calls

## Benefits of SEA-Lion Integration

1. **Cultural Accuracy**: Built specifically for Southeast Asian contexts
2. **Language Quality**: Better understanding of regional languages and dialects
3. **Medical Terminology**: Optimized for healthcare communication in Southeast Asia
4. **Cultural Sensitivity**: Respects traditional values and communication styles

## Troubleshooting

### SEA-Lion API Not Working
1. Check API key in `.env` file
2. Verify API endpoint URL
3. Check network connectivity
4. Review API documentation for changes
5. System will automatically use Gemini fallback

### Getting API Access
If you cannot get SEA-Lion API access:
1. The system works perfectly with Gemini AI alone
2. Cultural templates provide good fallback adaptations
3. Consider academic collaboration with AI Singapore for research access

## Future Enhancements

1. **Model Selection**: Allow choosing between different SEA-Lion models
2. **Fine-tuning**: Custom model training for specific medical contexts
3. **Caching**: Implement response caching for better performance
4. **Analytics**: Track usage and effectiveness of cultural adaptations
