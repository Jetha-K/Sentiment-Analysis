from flask import Flask, request, jsonify, send_from_directory
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import praw
from googleapiclient.discovery import build
import traceback

# Download the VADER lexicon for sentiment analysis (only the first time)
nltk.download('vader_lexicon')

# Setup Flask app
app = Flask(__name__, static_folder='../frontend')
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500", 
                              "allow_headers": ["Content-Type"]}})  # Allow Content-Type header
socketio = SocketIO(app, cors_allowed_origins="*")

# Setup SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

### REDDIT SETUP ###
reddit = praw.Reddit(client_id='f6Gy0Ss0xme7YTJ9r9mKDg', 
                     client_secret='-nFNpm_ADNRvZoUqrcz9H5HmYSYOcg', 
                     user_agent='web:SentimentAnalyzer:1.0 (by /u/Similar_Mind_4536)')

# Historical sentiment analysis route
@app.route('/historical/<platform>', methods=['POST'])
def historical_sentiment(platform):
    try:
        # Fetch keywords from the request body
        keywords = request.get_json().get('keywords', ['feminism', 'gender equality'])
        results = []

        if platform == "reddit":
            for submission in reddit.subreddit('all').search(" OR ".join(keywords), limit=100):
                post_content = submission.title + " " + submission.selftext
                sentiment_scores = sia.polarity_scores(post_content)
                results.append({
                    'title': submission.title,
                    'content': submission.selftext,
                    'sentiment': sentiment_scores
                })
        # Return results containing titles, content, and sentiment analysis
        return jsonify(results)

    except Exception as e:
        print(f"Error occurred in historical sentiment analysis: {e}")
        print(traceback.format_exc())  # Log the full traceback for debugging
        return jsonify({"error": str(e)}), 500  # Return a JSON error message

@app.before_request
def before_request():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5500'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Allow Content-Type
        return response

# Serve the index.html file
@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

# WebSocket handler for real-time communication
@socketio.on('message')
def handle_message(data):
    try:
        text = data['text']
        sentiment_scores = sia.polarity_scores(text)
        emit('response', sentiment_scores)
    except Exception as e:
        print(f"Error occurred in WebSocket message handling: {e}")
        emit('response', {"error": str(e)})

# Start the Flask server
if __name__ == '__main__':
    socketio.run(app, debug=True, port=5500)
