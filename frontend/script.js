// Function to analyze sentiment by sending a POST request to the Flask API
function analyzeSentiment() {
    // Get the input text from the textarea
    const text = document.getElementById('inputText').value;

    // dictionary for the input text
    const data = {
        text: text
    };

    // Send the text to the Flask backend using AJAX (Fetch API)
    // creating the json file to send to the server
    fetch('http://127.0.0.1:5001/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),  // Convert the data object to JSON
    })
    // to show errors
    .then(response => response.json())
    .then(data => {
        // Display the sentiment analysis result
        document.getElementById('result').textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
