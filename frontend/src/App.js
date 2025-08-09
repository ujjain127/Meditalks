import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import './App.css';
import Home from './Home';
import About from './About';

function Navigation() {
  const location = useLocation();
  
  return (
    <nav className="professional-nav">
      <div className="nav-container">
        <div className="nav-brand">
          <Link to="/" className="brand-link">
            <div className="brand-info">
              <span className="brand-name">MediTalks</span>
              <span className="brand-tagline">Medical AI Platform</span>
            </div>
          </Link>
        </div>
        <div className="nav-actions">
          <Link 
            to="/" 
            className={`nav-button ${location.pathname === '/' ? 'active' : ''}`}
          >
            <span className="nav-button-text">Platform</span>
          </Link>
          <Link 
            to="/about" 
            className={`nav-button ${location.pathname === '/about' ? 'active' : ''}`}
          >
            <span className="nav-button-text">About</span>
          </Link>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        
        <main className="main-content">
          <Routes>
            <Route path="/" element={
              <div className="professional-container">
                <Home />
              </div>
            } />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
