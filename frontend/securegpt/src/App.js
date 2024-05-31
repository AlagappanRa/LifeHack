import './App.css';
import React from 'react';
import userImage from './images/user.png'
import logoImage from './images/Logo.png'

function App() {
  return (
    <div className="container">
      <div className="sidebar">
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <img src={userImage} alt="ChatGPT" />
          </div>
          <h1>SecureGPT - Stay Secure</h1>
        </div>
        <nav className="sidebar-nav">
          <ul>
            <li><a href="new">SecureGPT 1.0</a></li>
            <li><a href="new">Machine Learning Model</a></li>
            <li><a href="new">Literature Review</a></li>
            <li><a href="new">Explore other secure GPTs</a></li>
          </ul>
        </nav>
        <div className="recent-activities">
          <h2>Today</h2>
          <ul>
            <li>Preprocess Text for NLP</li>
            <li>Launch Jupyter in Kubeflow</li>
            <li>Masks Postprocessing: Differences</li>
            <li>Summarize User Request</li>
            <li>Integrating Negative Prior: SAM</li>
          </ul>
          <h2>Yesterday</h2>
          <ul>
            <li>Visualize Singapore Police Boundaries</li>
          </ul>
        </div>
        <button className="add-team">Add Team Workspace</button>
      </div>
      <div className="main-content">
        <div className="content">
          <div className="logo-center">
            <img src={logoImage} alt="ChatGPT Logo" />
          </div>
          <div className="buttons">
            <div className="btn">
              <span>Input article text in pdf or word format</span>
            </div>
            <div className="btn">
              <span>Select how many times to analyse a text and receive sentiment information</span>
            </div>
            <div className="btn">
              <span>Output more information on the input</span>
            </div>
            <div className="btn">
              <span>Obtain more information about the person or organisation in this article</span>
            </div>
          </div>
        </div>
        <div className="footer">
          <div className="message-box">
            <input type="text" placeholder="Message SecureGPT" />
            <button className="send-btn">Send</button>
          </div>
          <div className="info">SecureGPT can make mistakes. Check important info.</div>
        </div>
      </div>
    </div>
  );
}

export default App;
