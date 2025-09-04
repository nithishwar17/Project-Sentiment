import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import SearchBar from './components/SearchBar';
import Dashboard from './components/Dashboard';

function App() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalysis = async (url) => {
    setIsLoading(true);
    setAnalysisResult(null);
    setError('');
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/analyze', { url });
      setAnalysisResult(response.data);
    } catch (err) {
      setError('Failed to analyze URL. Please check the URL and ensure the backend is running.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Product Sentiment Analyzer</h1>
        <p>Gain instant insights from customer feedback</p>
      </header>
      <main>
        <SearchBar onAnalyze={handleAnalysis} />

        {isLoading && (
          <div>
            <div className="loader"></div>
            {/* This is the updated loading message */}
            <p className="status-message">Fetching and analyzing reviews...</p>
          </div>
        )}
        {error && <p className="status-message error">{error}</p>}
        {analysisResult && <Dashboard data={analysisResult} />}
      </main>
    </div>
  );
}

export default App;

