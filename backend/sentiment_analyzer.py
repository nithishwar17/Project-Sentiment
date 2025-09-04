# backend/sentiment_analyzer.py

from textblob import TextBlob

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: A dictionary containing the sentiment ('Positive', 'Negative', 'Neutral'),
              the polarity score, and the subjectivity score.
    """
    # Create a TextBlob object
    analysis = TextBlob(text)

    # Determine sentiment based on polarity
    if analysis.sentiment.polarity > 0:
        sentiment = "Positive"
    elif analysis.sentiment.polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        'sentiment': sentiment,
        # Polarity is a float within the range [-1.0, 1.0]
        'polarity': analysis.sentiment.polarity,
        # Subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.
        'subjectivity': analysis.sentiment.subjectivity
    }

# --- This is for testing the analyzer directly ---
if __name__ == '__main__':
    test_reviews = [
        "Satisfied with the product, worth the price consider it is so lightswight and also has an RTX gpu.",
        "Worst experience from Amazon. I purchased this laptop and I got a defective product.",
        "Nice...",
        "The performance is good. Battery life is decent."
    ]

    print("--- Testing Sentiment Analyzer ---")
    for i, review in enumerate(test_reviews, 1):
        result = analyze_sentiment(review)
        print(f"Review {i}: '{review[:50]}...'")
        print(f"  -> Sentiment: {result['sentiment']}, Polarity: {result['polarity']:.2f}\n")