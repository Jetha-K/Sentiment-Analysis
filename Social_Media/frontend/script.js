window.onload = function() {
  console.log("Script loaded and running!");

  // Function to fetch historical sentiment
  function fetchHistorical() {
      console.log("Button clicked, starting fetch...");

      const platform = document.querySelector('input[name="platform"]:checked').value; // Get selected platform
      const keywords = { keywords: ['feminism', 'feminist', 'gender equality'] };

      fetch(`http://localhost:5500/historical/${platform}`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(keywords),
      })
      .then(response => {
          console.log("Fetch response:", response);
          if (!response.ok) {
              return response.json().then(err => { throw new Error(err.error); }); // Get error message from response
          }
          return response.json();
      })
      .then(data => {
          console.log("Data received:", data);  // Log the data received

          // Clear previous results
          const resultContainer = document.getElementById('result');
          resultContainer.innerHTML = ''; 

          // Display each post's title, content, and sentiment
          data.forEach(post => {
              const postElement = document.createElement('div');
              postElement.classList.add('post');

              postElement.innerHTML = `
                  <h4>${post.title}</h4>
                  <p>${post.content ? post.content : 'No content available'}</p>
                  <pre>Sentiment: ${JSON.stringify(post.sentiment, null, 2)}</pre>
                  <hr>
              `;

              resultContainer.appendChild(postElement);
          });
      })
      .catch(error => {
          console.error('Error:', error);
          document.getElementById('result').textContent = 'Error: ' + error.message;
      });
  }

  // Attach event listener to the button
  document.getElementById('analyzeButton').addEventListener('click', fetchHistorical);
}
