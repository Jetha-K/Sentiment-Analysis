from flask import Flask, request, jsonify, send_from_directory
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from flask_cors import CORS
import requests

# Download the VADER lexicon for sentiment analysis (only the first time)
nltk.download('vader_lexicon')

# Setup Flask app
app = Flask(__name__)
CORS(app)  # Allow all origins for testing

# Setup SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

### TWITTER API V2 SETUP ###
bearer_token = 'YOUR_BEARER_TOKEN'  # Replace with your Bearer Token for v2

def create_headers(bearer_token):
    return {"Authorization": f"Bearer {bearer_token}"}

def search_tweets(keywords):
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    query = " OR ".join(keywords)
    params = {
        'query': query,
        'max_results': 100,
        'tweet.fields': 'text',  # Specify fields to return
    }
    headers = create_headers(bearer_token)

    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.text}")  # Log response error
        return []

    return [tweet['text'] for tweet in response.json().get('data', [])]

# Historical sentiment analysis route
@app.route('/historical/<platform>', methods=['POST'])
def historical_sentiment(platform):
    print(f"Received request for platform: {platform}")  # Log request

    try:
        keywords = request.get_json().get('keywords', ["#feminism", "#genderEquality", "feminism", "gender equality"])
        print(f"Keywords received: {keywords}")  # Log keywords

        posts = []

        if platform == "twitter":
            posts = search_tweets(keywords)

        # Perform sentiment analysis on posts
        results = [sia.polarity_scores(post) for post in posts]
        
        print(f"Results: {results}")  # Log results
        return jsonify(results)

    except Exception as e:
        print(f"General error: {str(e)}")  # Log the error
        return jsonify({"error": str(e)}), 500

# Serve static files from the frontend directory
@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('../frontend', filename)

# Serve the index.html file
@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True, port=5500)
