import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import pymongo
from datetime import datetime, timezone

# --- NEW: Explicitly define the path to the .env file ---
# This finds the directory where app.py is located
basedir = os.path.abspath(os.path.dirname(__file__))
# This creates the full path to the .env file
dotenv_path = os.path.join(basedir, '.env')
# Load the .env file from that specific path
load_dotenv(dotenv_path=dotenv_path)

# Add a print statement for debugging
print(f"Attempting to load .env file from: {dotenv_path}")

# Import our custom modules
from scraper import scrape_amazon_reviews
from sentiment_analyzer import analyze_sentiment

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# --- MongoDB Connection Setup ---
MONGO_URI = os.getenv("MONGO_URI")

# Add another print statement for debugging
print(f"Loaded MONGO_URI from environment: {MONGO_URI is not None}")

if not MONGO_URI:
    print("ERROR: MONGO_URI variable not found after loading .env.")
    client = None
else:
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client.get_database("sentiment_db")
        results_collection = db.get_collection("analysis_results")
        print("Successfully connected to MongoDB Atlas!")
    except pymongo.errors.ConfigurationError as e:
        print(f"ERROR connecting to MongoDB Atlas: {e}")
        client = None
# -----------------------------

# ... (The rest of your code remains exactly the same) ...

@app.route('/api/analyze', methods=['POST'])
def analyze_url():
    if not client:
        return jsonify({"error": "Database connection is not configured."}), 500

    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "URL not provided"}), 400

    url = data['url']

    try:
        reviews_text = scrape_amazon_reviews(url)
        if not reviews_text:
            return jsonify({"error": "Could not scrape reviews. Check the URL or website structure."}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred during scraping: {e}"}), 500

    analyzed_reviews = []
    positive_count, negative_count, neutral_count = 0, 0, 0

    for review in reviews_text:
        analysis = analyze_sentiment(review)
        analyzed_reviews.append({
            "text": review,
            "sentiment": analysis['sentiment'],
            "polarity": analysis['polarity']
        })
        if analysis['sentiment'] == 'Positive': positive_count += 1
        elif analysis['sentiment'] == 'Negative': negative_count += 1
        else: neutral_count += 1
    
    summary = {
        "positive": positive_count, "negative": negative_count, 
        "neutral": neutral_count, "total": len(analyzed_reviews)
    }
    
    document_to_save = {
        "url": url,
        "summary": summary,
        "reviews": analyzed_reviews,
        "analyzedAt": datetime.now(timezone.utc)
    }
    results_collection.insert_one(document_to_save)
    print(f"Successfully saved analysis for {url} to the database.")
    
    response_data = { "summary": summary, "reviews": analyzed_reviews }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

