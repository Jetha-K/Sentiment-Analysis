# Libraries
# request for web to server requests and jsonify for converting into json for web use
from flask import Flask, request, jsonify
# VADER lexicon
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from flask_cors import CORS

# Download the VADER lexicon for sentiment analysis (only the first time)
nltk.download('vader_lexicon')

# It shows Flask where it's located 
app = Flask(__name__)
CORS(app)
# Initialises SentimentIntensity analysis 
sia = SentimentIntensityAnalyzer()

# root url that triggers home() when a user visits they should see Sentiment Analysis API is running on the web page
@app.route('/')
def home():
    return "Sentiment Analysis API is running."

# Sentiment analysis route
# Post requests are for sending text data to the server for analysis
@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()  # Get the JSON data sent by the frontend
    text = data.get('text', '')  # Extract the 'text' field from the JSON

    # Perform sentiment analysis using VADER
    # returns a dictionary containing these scores neg, neu, pos, compound from -1 to +1
    sentiment_scores = sia.polarity_scores(text)

    return jsonify(sentiment_scores)  # Return the scores as JSON

# checks if it's being directly run if it is 
if __name__ == '__main__':
    # runs the flask server
    app.run(debug=True)