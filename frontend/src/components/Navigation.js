import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navigation.css';

const Navigation = () => {
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);
  
  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/predictions', label: 'Predictions', icon: '🌊' },
    { path: '/alerts', label: 'Alerts', icon: '🚨' },
    { path: '/resources', label: 'Resources', icon: '🚛' },
  ];
  
  return (
    <>
      {/* Mobile menu button */}
      <button 
        className="mobile-menu-btn"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle menu"
      >
        ☰
      </button>
      
      <nav className={`navigation ${isOpen ? 'open' : ''}`}>
        <div className="nav-header">
          <h1 className="nav-title">
            <span className="nav-icon">🛡️</span>
            FloodGuardian AI
          </h1>
          <p className="nav-subtitle">Emergency Response System</p>
        </div>
      
      <ul className="nav-menu">
        {navItems.map((item) => (
          <li key={item.path}>
            <Link
              to={item.path}
              className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
              onClick={() => setIsOpen(false)}
            >
              <span className="nav-link-icon">{item.icon}</span>
              <span className="nav-link-text">{item.label}</span>
            </Link>
          </li>
        ))}
      </ul>
      
      <div className="nav-footer">
        <div className="system-status">
          <div className="status-indicator online"></div>
          <span>System Online</span>
        </div>
        <p className="nav-version">v1.0.0</p>
      </div>
    </nav>
    </>
  );
};

export default Navigation;

