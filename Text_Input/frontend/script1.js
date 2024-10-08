    // // run the code once the window has loaded
    // window.onload = function() {
    //         // Initialize Socket.IO connection to Flask-SocketIO server
    //         var socket = io.connect('http://localhost:5001');  // Ensure this matches your backend port

    //         // Add event listener to the textarea for real-time input
    //         // listens for if there's anything being inputted
    //         document.getElementById('inputText').addEventListener('input', function() {
    //             var inputText = this.value;  // Get the current text in the textarea

    //             // Only send text if the socket is connected
    //             if (socket.connected && inputText.trim()) {
    //                 socket.emit('message', { text: inputText });
    //             } else if (!socket.connected) {
    //                 document.getElementById('result').textContent = 'Server is disconnected.';
    //             }
    //         });

    //         // Listen for sentiment analysis responses from the server
    //         socket.on('response', function(data) {
    //             // Display the sentiment score in the result area
    //             document.getElementById('result').innerHTML = '<h3>Score: ' + data.compound + '</h3>';
    //         });

    //         // Handle WebSocket disconnection event
    //         socket.on('disconnect', function() {
    //             // Update the status to show the user the connection is lost
    //             document.getElementById('status').textContent = 'Disconnected from the server.';
    //             document.getElementById('result').textContent = 'Server connection lost. Cannot analyze sentiment.';
    //         });

    //         // Optionally, handle the reconnection event if the server comes back online
    //         socket.on('connect', function() {
    //             // Update the status to show the user the connection is re-established
    //             document.getElementById('status').textContent = 'Connected';
    //         });
    //     }