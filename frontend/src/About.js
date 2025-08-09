import React from 'react';
import './About.css';

function About() {
  return (
    <div className="about-page">
      {/* Hero Section */}
      <div className="hero-section">
        <div className="hero-content">
          <h1>About MediTalks</h1>
          <p className="hero-subtitle">
            Making Medical Information Accessible Across Southeast Asia
          </p>
          <div className="hero-description">
            <p>
              A practical tool that helps translate and adapt medical documents for 
              Filipino, Thai, Vietnamese, Malay, and Khmer communities.
            </p>
          </div>
          <div className="hero-stats">
            <div className="stat">
              <span className="stat-number">6</span>
              <span className="stat-label">Languages</span>
            </div>
            <div className="stat">
              <span className="stat-number">5</span>
              <span className="stat-label">Cultural Contexts</span>
            </div>
            <div className="stat">
              <span className="stat-number">1</span>
              <span className="stat-label">AI Model</span>
            </div>
          </div>
        </div>
      </div>

      {/* About This PoC Section */}
      <div className="section about-section">
        <div className="container">
          <h2>What This Tool Does</h2>
          <div className="about-grid">
            <div className="about-card">
              <h3>Medical Translation</h3>
              <p>Takes your medical text or PDF documents and translates them into clear, understandable language for different Southeast Asian communities.</p>
            </div>
            <div className="about-card">
              <h3>Cultural Adaptation</h3>
              <p>Goes beyond word-for-word translation to consider cultural practices, family dynamics, and local healthcare customs.</p>
            </div>
            <div className="about-card">
              <h3>Simple Document Processing</h3>
              <p>Upload medical PDFs and get back easy-to-understand summaries with clear instructions in the language you need.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Use Cases Section */}
      <div className="section use-cases-section">
        <div className="container">
          <h2>When This Helps</h2>
          <div className="use-cases">
            <div className="use-case">
              <h3>Hospital Paperwork</h3>
              <p>Turn complicated discharge instructions into clear guidance that patients and families can actually understand and follow.</p>
            </div>
            <div className="use-case">
              <h3>Medication Instructions</h3>
              <p>Explain prescriptions, dosages, and side effects in simple terms and the patient's preferred language.</p>
            </div>
            <div className="use-case">
              <h3>Test Results</h3>
              <p>Make lab reports and medical test results understandable for patients who speak different languages.</p>
            </div>
            <div className="use-case">
              <h3>Health Education</h3>
              <p>Adapt health information for communities with different literacy levels and cultural backgrounds.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Technology Stack Section */}
      <div className="section tech-section">
        <div className="container">
          <h2>How It Works</h2>
          <div className="tech-stack">
            <div className="tech-category">
              <h3>AI Technology</h3>
              <ul>
                <li>SEA-Lion AI specialized for Southeast Asian languages and cultures</li>
                <li>Automatic language detection</li>
                <li>Cultural context understanding</li>
                <li>Medical terminology adaptation</li>
              </ul>
            </div>
            <div className="tech-category">
              <h3>Document Processing</h3>
              <ul>
                <li>PDF text extraction and analysis</li>
                <li>Multi-format document support</li>
                <li>Content structure recognition</li>
                <li>Text cleaning and preparation</li>
              </ul>
            </div>
            <div className="tech-category">
              <h3>Platform</h3>
              <ul>
                <li>Web-based interface (React)</li>
                <li>Python backend (Flask)</li>
                <li>Cloud deployment (Render)</li>
                <li>Cross-platform accessibility</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Supported Languages Section */}
      <div className="section languages-section">
        <div className="container">
          <h2>Languages & Cultural Contexts</h2>
          <div className="languages-grid">
            <div className="language-card">
              <h3>Filipino (Tagalog)</h3>
              <p>Takes into account family involvement in healthcare decisions and respect for medical authority.</p>
            </div>
            <div className="language-card">
              <h3>Thai</h3>
              <p>Considers Buddhist perspectives on health and the role of traditional medicine alongside modern treatment.</p>
            </div>
            <div className="language-card">
              <h3>Vietnamese</h3>
              <p>Respects traditional medicine practices and the importance of family in healthcare decisions.</p>
            </div>
            <div className="language-card">
              <h3>Malay</h3>
              <p>Incorporates Islamic perspectives on health and considers halal requirements in medical advice.</p>
            </div>
            <div className="language-card">
              <h3>Khmer</h3>
              <p>Acknowledges traditional healing practices and Buddhist beliefs about health and wellness.</p>
            </div>
            <div className="language-card">
              <h3>English</h3>
              <p>Standard medical communication adapted for different cultural backgrounds and literacy levels.</p>
            </div>
          </div>
        </div>
      </div>

      {/* How to Use Section */}
      <div className="section demo-section">
        <div className="container">
          <h2>How to Use</h2>
          <div className="demo-steps">
            <div className="demo-step">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3>Pick Your Input</h3>
                <p>Type in medical text directly or upload a PDF document you need translated.</p>
              </div>
            </div>
            <div className="demo-step">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3>Choose Your Context</h3>
                <p>Select which community you're translating for - each has different cultural considerations.</p>
              </div>
            </div>
            <div className="demo-step">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3>Get Your Translation</h3>
                <p>Receive adapted text that's not just translated, but culturally appropriate.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Impact Section */}
      <div className="section impact-section">
        <div className="container">
          <h2>Why This Matters</h2>
          <div className="impact-grid">
            <div className="impact-item">
              <h3>Better Understanding</h3>
              <p>Patients understand their medical instructions better when they're explained in familiar terms and their own language.</p>
            </div>
            <div className="impact-item">
              <h3>Cultural Respect</h3>
              <p>Medical advice that acknowledges traditional practices and cultural values is more likely to be followed.</p>
            </div>
            <div className="impact-item">
              <h3>Saves Time</h3>
              <p>Healthcare providers spend less time explaining when information is already clear and culturally appropriate.</p>
            </div>
            <div className="impact-item">
              <h3>Reaches More People</h3>
              <p>Breaking down language barriers means more people can access and understand healthcare information.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="poc-footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-section">
              <h3>MediTalks</h3>
              <p>A tool for making medical information accessible across Southeast Asian cultures.</p>
              <p className="version">Current Version - Prototype</p>
            </div>
            <div className="footer-section">
              <h3>Languages Supported</h3>
              <p>English • Filipino • Thai • Vietnamese • Malay • Khmer</p>
            </div>
            <div className="footer-section">
              <h3>Built With</h3>
              <p>SEA-Lion AI • React • Python • Deployed on Render</p>
            </div>
          </div>
          <div className="footer-bottom">
            <p>© 2025 MediTalks - Making Healthcare Communication Clearer</p>
            <p>Designed for Southeast Asian communities</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default About;
