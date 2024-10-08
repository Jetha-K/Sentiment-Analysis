window.onload = function() {
  console.log("Script loaded and running!");

  // Function to fetch historical sentiment
  function fetchHistorical() {
      console.log("Button clicked, starting fetch...");

      const platform = 'twitter';
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
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(data => {
          console.log("Data received:", data);  // Log the data received
          document.getElementById('result').textContent = JSON.stringify(data, null, 2);
      })
      .catch(error => {
          console.error('Error:', error);
          document.getElementById('result').textContent = 'Error: ' + error.message;
      });
  }

  document.getElementById('analyzeButton').addEventListener('click', fetchHistorical);
}
