import React from 'react';
import './ReviewList.css';

const ReviewList = ({ reviews }) => {
  const getAvatarStyle = (sentiment) => {
    const colors = {
      Positive: 'var(--success-color)',
      Negative: 'var(--danger-color)',
      Neutral: 'var(--neutral-color)',
    };
    return { backgroundColor: colors[sentiment] };
  };

  const getAvatarIcon = (sentiment) => {
    const icons = {
      Positive: '👍',
      Negative: '👎',
      Neutral: '🤔',
    };
    return icons[sentiment];
  };

  return (
    <div className="review-list">
      {reviews.map((review, index) => (
        <div key={index} className="review-card">
          <div className="avatar" style={getAvatarStyle(review.sentiment)}>
            {getAvatarIcon(review.sentiment)}
          </div>
          <div className="review-content">
            <p className="review-text">{review.text}</p>
            <span className={`sentiment-badge sentiment-${review.sentiment.toLowerCase()}`}>
              {review.sentiment}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ReviewList;
