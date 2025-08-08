import React, { useState } from 'react';
import './App.css';

// API URL configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [activeTab, setActiveTab] = useState('text');
  const [message, setMessage] = useState('');
  const [context, setContext] = useState('');
  const [targetLanguage, setTargetLanguage] = useState('en');
  const [adaptedMessage, setAdaptedMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [pdfResults, setPdfResults] = useState(null);

  const culturalContexts = [
    { value: '', label: 'Select Cultural Context' },
    { value: 'tagalog-rural', label: 'Tagalog (Rural Philippines)' },
    { value: 'thai-low-literacy', label: 'Thai (Low Literacy)' },
    { value: 'khmer-indigenous', label: 'Khmer (Indigenous Communities)' },
    { value: 'vietnamese-elderly', label: 'Vietnamese (Elderly)' },
    { value: 'malay-traditional', label: 'Malay (Traditional Communities)' }
  ];

  const languages = [
    { value: 'en', label: 'English' },
    { value: 'th', label: 'Thai (ไทย)' },
    { value: 'vi', label: 'Vietnamese (Tiếng Việt)' },
    { value: 'ms', label: 'Malay (Bahasa Melayu)' },
    { value: 'km', label: 'Khmer (ខ្មែរ)' },
    { value: 'tl', label: 'Tagalog (Filipino)' }
  ];

  // Network connectivity test
  const testBackendConnection = async () => {
    try {
      console.log('Testing backend connection...');
      const response = await fetch(`${API_BASE_URL}/api/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('Backend connection successful:', data);
        const aiService = data.ai_services?.primary_service || 'Unknown';
        const sealionStatus = data.ai_services?.sealion_available ? 'Available' : 'Not Available';
        const geminiStatus = data.ai_services?.gemini_available ? 'Available' : 'Not Available';
        
        alert(`Backend Status: ${data.status}\n` +
              `Service: ${data.service}\n` +
              `Primary AI: ${aiService}\n` +
              `SEA-Lion: ${sealionStatus}\n` +
              `Gemini: ${geminiStatus}`);
      } else {
        throw new Error(`Backend returned ${response.status}`);
      }
    } catch (error) {
      console.error('Backend connection failed:', error);
      alert(`Backend Connection Failed: ${error.message}\n\nPlease ensure the Flask backend is running on port 5000.`);
    }
  };

  const handleGenerate = async () => {
    if (!message.trim() || !context) {
      alert('Please enter a medical message and select a cultural context.');
      return;
    }

    setIsLoading(true);
    
    try {
      // Call the Python backend API
      const response = await fetch(`${API_BASE_URL}/api/cultural-adaptation/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message.trim(),
          context: context
        })
      });

      console.log('API Response Status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('API Error Response:', errorText);
        throw new Error(`API Error: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log('API Response Data:', data);

      if (data.success) {
        const contextLabel = culturalContexts.find(c => c.value === context)?.label || context;
        setAdaptedMessage(`[Culturally adapted for ${contextLabel}]\n\n${data.data.adaptedMessage}`);
      } else {
        console.error('API returned error:', data.error);
        throw new Error(data.error?.message || 'Failed to generate adaptation');
      }
    } catch (error) {
      console.error('Full error details:', error);
      console.error('Error calling backend:', error.message);
      
      // Show detailed error for debugging
      alert(`Backend Error: ${error.message}\n\nUsing fallback mode instead.`);
      
      // Fallback to local simulation
      const contextLabel = culturalContexts.find(c => c.value === context)?.label || context;
      setAdaptedMessage(`[Culturally adapted for ${contextLabel}]\n\n${generateAdaptedMessage(message, context)}\n\n⚠️ Note: Using offline mode - backend connection failed.\nError: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePdfUpload = async () => {
    console.log('PDF Upload clicked!');
    console.log('Selected file:', selectedFile);
    console.log('Context:', context);
    console.log('Target language:', targetLanguage);
    
    if (!selectedFile || !context || !targetLanguage) {
      console.log('Validation failed!');
      alert('Please select a PDF file, cultural context, and target language.');
      return;
    }

    setIsLoading(true);
    console.log('Starting PDF upload...');
    
    try {
      const formData = new FormData();
      formData.append('pdf', selectedFile);
      formData.append('context', context);
      formData.append('target_language', targetLanguage);

      console.log('Uploading PDF:', {
        fileName: selectedFile.name,
        fileSize: selectedFile.size,
        context: context,
        targetLanguage: targetLanguage
      });

      const response = await fetch(`${API_BASE_URL}/api/extract-pdf`, {
        method: 'POST',
        body: formData
      });

      console.log('PDF API Response Status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('PDF API Error Response:', errorText);
        throw new Error(`PDF Processing Error: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log('PDF API Response Data:', data);

      if (data.success) {
        console.log('Setting PDF results:', data.data);
        setPdfResults(data.data);
      } else {
        console.error('PDF API returned error:', data.error);
        throw new Error(data.error?.message || 'Failed to analyze PDF');
      }
    } catch (error) {
      console.error('Full PDF error details:', error);
      console.error('Error analyzing PDF:', error.message);
      
      // Show detailed error for debugging
      alert(`PDF Analysis Error: ${error.message}\n\nUsing fallback mode instead.`);
      
      // Fallback simulation
      const contextLabel = culturalContexts.find(c => c.value === context)?.label || context;
      const languageLabel = languages.find(l => l.value === targetLanguage)?.label || targetLanguage;
      setPdfResults({
        originalText: '[Sample PDF content extracted...]',
        summary: `This is a sample summary of the medical document, culturally adapted for ${contextLabel} and translated to ${languageLabel}.`,
        keyTerms: ['Sample Term 1', 'Sample Term 2', 'Sample Term 3'],
        culturalContext: `Document adapted for ${contextLabel} cultural context`,
        detectedLanguage: 'English',
        outputLanguage: targetLanguage,
        fileName: selectedFile.name,
        errorMessage: `⚠️ Note: Using offline mode - backend connection failed.\nError: ${error.message}`
      });
    } finally {
      setIsLoading(false);
    }
  };

  const generateAdaptedMessage = (msg, ctx) => {
    const adaptations = {
      'tagalog-rural': `Sa madaling salita: ${msg}\n\nPaalala para sa pamilya: Makipag-ugnayan sa inyong doktor kung may mga katanungan kayo.`,
      'thai-low-literacy': `คำแนะนำง่ายๆ: ${msg}\n\nสำคัญ: ปรึกษาหมอหรือพยาบาลหากมีข้อสงสัย`,
      'khmer-indigenous': `ការណែនាំសំខាន់: ${msg}\n\nចំណាំ: សូមពិគ្រោះជាមួយគ្រូពេទ្យ`,
      'vietnamese-elderly': `Lời khuyên quan trọng: ${msg}\n\nXin lưu ý: Hãy tham khảo ý kiến bác sĩ`,
      'malay-traditional': `Nasihat penting: ${msg}\n\nIngatan: Sila berjumpa dengan doktor jika ada soalan`
    };
    
    return adaptations[ctx] || `Cultural adaptation for ${ctx}: ${msg}`;
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
    } else {
      alert('Please select a valid PDF file.');
      event.target.value = '';
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="container">
          <h1 className="title">MediTalks</h1>
          <p className="subtitle">Adaptive Cultural Contextualization Engine</p>
          <button 
            onClick={testBackendConnection}
            className="connection-test-button"
            style={{
              position: 'absolute',
              top: '20px',
              right: '20px',
              padding: '8px 16px',
              backgroundColor: '#8b7355',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '12px'
            }}
          >
            Test Backend Connection
          </button>
        </div>
      </header>

      {/* Tab Navigation */}
      <div className="tab-navigation">
        <button 
          className={`tab-button ${activeTab === 'text' ? 'active' : ''}`}
          onClick={() => setActiveTab('text')}
        >
          Text Analysis
        </button>
        <button 
          className={`tab-button ${activeTab === 'pdf' ? 'active' : ''}`}
          onClick={() => setActiveTab('pdf')}
        >
          PDF Upload
        </button>
      </div>

      {/* Main Content */}
      <main className="main">
        <div className="content-card">
          
          {activeTab === 'text' && (
            <div className="tab-content">
              {/* Input Section */}
              <div className="input-section">
                <label className="form-label">Medical Message</label>
                <textarea
                  className="form-textarea"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Enter your medical message here..."
                  rows="4"
                />
              </div>

              {/* Context Selection */}
              <div className="context-section">
                <label className="form-label">Cultural Context</label>
                <select
                  className="form-select"
                  value={context}
                  onChange={(e) => setContext(e.target.value)}
                >
                  {culturalContexts.map(ctx => (
                    <option key={ctx.value} value={ctx.value}>
                      {ctx.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Generate Button */}
              <div className="action-section">
                <button
                  onClick={handleGenerate}
                  disabled={isLoading || !message.trim() || !context}
                  className="generate-button"
                >
                  {isLoading ? 'Generating...' : 'Generate Cultural Adaptation'}
                </button>
              </div>

              {/* Output Section */}
              {adaptedMessage && (
                <div className="output-section">
                  <label className="form-label">Culturally Adapted Message</label>
                  <div className="output-box">
                    <div className="output-text">{adaptedMessage}</div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'pdf' && (
            <div className="tab-content">
              {/* PDF Upload Section */}
              <div className="upload-section">
                <label className="form-label">Upload PDF Document</label>
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileSelect}
                  className="file-input"
                />
                {selectedFile && (
                  <div className="file-info">
                    📄 Selected: {selectedFile.name} ({Math.round(selectedFile.size / 1024)} KB)
                  </div>
                )}
              </div>

              {/* Context Selection */}
              <div className="context-section">
                <label className="form-label">Cultural Context</label>
                <select
                  className="form-select"
                  value={context}
                  onChange={(e) => setContext(e.target.value)}
                >
                  {culturalContexts.map(ctx => (
                    <option key={ctx.value} value={ctx.value}>
                      {ctx.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Language Selection */}
              <div className="language-section">
                <label className="form-label">Target Language</label>
                <select
                  className="form-select"
                  value={targetLanguage}
                  onChange={(e) => setTargetLanguage(e.target.value)}
                >
                  {languages.map(lang => (
                    <option key={lang.value} value={lang.value}>
                      {lang.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Analyze Button */}
              <div className="action-section">
                <button
                  onClick={handlePdfUpload}
                  disabled={isLoading || !selectedFile || !context || !targetLanguage}
                  className="generate-button"
                >
                  {isLoading ? 'Analyzing...' : 'Analyze PDF Document'}
                </button>
              </div>

              {/* PDF Results */}
              {pdfResults && (
                <div className="pdf-results">
                  <div className="results-header">
                    <h3>📋 Document Summary</h3>
                    <p className="results-meta">
                      File: {pdfResults.fileName} | 
                      Words: {pdfResults.wordCount} |
                      Language: {languages.find(l => l.value === pdfResults.outputLanguage)?.label} |
                      Context: {culturalContexts.find(c => c.value === context)?.label}
                    </p>
                  </div>

                  {/* Document Summary Only */}
                  <div className="results-section">
                    <label className="form-label">📝 Summary</label>
                    <div className="output-box">
                      <div className="output-text summary-content">{pdfResults.summary}</div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
