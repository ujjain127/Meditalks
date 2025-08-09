import React, { useState } from 'react';

// API URL configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function Home() {
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

  const handleGenerate = async () => {
    if (!message.trim() || !context) {
      alert('Please enter a medical message and select a cultural context.');
      return;
    }

    setIsLoading(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/cultural-adaptation/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message.trim(),
          context: context,
          target_language: targetLanguage
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        setAdaptedMessage(data.data.adapted_message);
      } else {
        alert('Error: ' + (data.error?.message || 'Failed to generate adaptation'));
      }
    } catch (error) {
      console.error('Error calling API:', error);
      alert('Error connecting to the server. Please check your connection and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
    } else {
      alert('Please select a valid PDF file.');
    }
  };

  const handlePdfSubmit = async () => {
    if (!selectedFile || !context) {
      alert('Please select a PDF file and cultural context.');
      return;
    }

    setIsLoading(true);
    const formData = new FormData();
    formData.append('pdf', selectedFile);
    formData.append('context', context);
    formData.append('target_language', targetLanguage);

    try {
      const response = await fetch(`${API_BASE_URL}/api/extract-pdf`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        setPdfResults(data.data);
      } else {
        alert('Error: ' + (data.error?.message || 'Failed to process PDF'));
      }
    } catch (error) {
      console.error('Error uploading PDF:', error);
      alert('Error processing PDF. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="adaptive-engine">
      <h2>ADAPTIVE CULTURAL CONTEXTUALIZATION ENGINE</h2>
      
      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'text' ? 'active' : ''}`}
          onClick={() => setActiveTab('text')}
        >
          TEXT ANALYSIS
        </button>
        <button 
          className={`tab ${activeTab === 'pdf' ? 'active' : ''}`}
          onClick={() => setActiveTab('pdf')}
        >
          PDF UPLOAD
        </button>
      </div>

      {activeTab === 'text' && (
        <div className="tab-content">
          <div className="form-group">
            <label htmlFor="message">Medical Message</label>
            <textarea
              id="message"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Enter your medical message here..."
              rows="4"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="context">Cultural Context</label>
              <select
                id="context"
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

            <div className="form-group">
              <label htmlFor="language">Target Language</label>
              <select
                id="language"
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
          </div>

          <button 
            onClick={handleGenerate} 
            disabled={isLoading}
            className="generate-btn"
          >
            {isLoading ? 'PROCESSING...' : 'GENERATE CULTURAL ADAPTATION'}
          </button>

          {adaptedMessage && (
            <div className="result">
              <h4>Culturally Adapted Message:</h4>
              <div className="adapted-message">
                {adaptedMessage}
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'pdf' && (
        <div className="tab-content">
          <div className="form-group">
            <label htmlFor="pdf-upload">Select PDF File</label>
            <input
              id="pdf-upload"
              type="file"
              accept=".pdf"
              onChange={handleFileUpload}
              className="file-input"
            />
            {selectedFile && (
              <div className="file-info">
                Selected: {selectedFile.name}
              </div>
            )}
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="pdf-context">Cultural Context</label>
              <select
                id="pdf-context"
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

            <div className="form-group">
              <label htmlFor="pdf-language">Target Language</label>
              <select
                id="pdf-language"
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
          </div>

          <button 
            onClick={handlePdfSubmit} 
            disabled={isLoading || !selectedFile}
            className="generate-btn"
          >
            {isLoading ? 'PROCESSING PDF...' : 'ANALYZE PDF'}
          </button>

          {pdfResults && (
            <div className="result">
              <h4>PDF Analysis Results:</h4>
              <div className="pdf-info">
                <div className="info-item">
                  <strong>File:</strong> {pdfResults.fileName}
                </div>
                <div className="info-item">
                  <strong>Detected Language:</strong> {pdfResults.detectedLanguage}
                </div>
                <div className="info-item">
                  <strong>Output Language:</strong> {pdfResults.outputLanguage}
                </div>
                <div className="info-item">
                  <strong>Word Count:</strong> {pdfResults.wordCount}
                </div>
                <div className="info-item">
                  <strong>Cultural Context:</strong> {pdfResults.culturalContext}
                </div>
                {pdfResults.analysisSource && (
                  <div className="info-item">
                    <strong>AI Service:</strong> {pdfResults.analysisSource}
                  </div>
                )}
              </div>
              <div className="adapted-message">
                <strong>Summary & Adaptation:</strong>
                <div className="summary-content">
                  {pdfResults.summary}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Home;
