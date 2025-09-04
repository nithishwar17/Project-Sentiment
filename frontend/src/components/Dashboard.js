// frontend/src/components/Dashboard.js
import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import ReviewList from './ReviewList'; // Import ReviewList
import './Dashboard.css';

ChartJS.register(ArcElement, Tooltip, Legend);

const Dashboard = ({ data }) => {
  const chartData = {
    labels: ['Positive', 'Negative', 'Neutral'],
    datasets: [
      {
        label: 'Sentiment',
        data: [data.summary.positive, data.summary.negative, data.summary.neutral],
        backgroundColor: [
          'rgba(75, 192, 192, 0.6)',
          'rgba(255, 99, 132, 0.6)',
          'rgba(201, 203, 207, 0.6)',
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(201, 203, 207, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className="dashboard-container">
      <h2>Analysis Results</h2>
      <div className="summary-grid">
        <div className="chart-container">
          <h3>Sentiment Distribution</h3>
          <Pie data={chartData} />
        </div>
        <div className="reviews-container">
          <h3>Customer Reviews ({data.summary.total})</h3>
          {/* Use the ReviewList component here */}
          <ReviewList reviews={data.reviews} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;