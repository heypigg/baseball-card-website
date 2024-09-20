document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const resultsContainer = document.getElementById('results-container');
    const playerNameInput = document.getElementById('player-name');
    const cardNumberInput = document.getElementById('card-number');

    if (!searchForm || !resultsContainer || !playerNameInput || !cardNumberInput) {
        console.error('Error: One or more required elements not found');
        return;
    }
  
    searchForm.addEventListener('submit', async (event) => {
        event.preventDefault();
      
        const playerName = document.getElementById('player-name').value.trim();
        const cardNumber = document.getElementById('card-number').value.trim();
      
        let query = '';
        if (playerName) {
          query = `playerName=${encodeURIComponent(playerName)}`;
        } else if (cardNumber) {
          query = `cardNumber=${encodeURIComponent(cardNumber)}`;
        }
      
        if (query) {
          try {
            const response = await fetch(`http://localhost:5001/api/cards?${query}`);
            const data = await response.json();
            console.log('Search Results:', data); // Debugging
      
            resultsContainer.innerHTML = '';
            if (data.length > 0) {
              data.forEach(item => {
                const resultDiv = document.createElement('div');
                resultDiv.innerHTML = `
                  <h3>${item.PlayerName || 'Unknown Player'}</h3>
                  <p>Card Number: ${item.CardNumber || 'Unknown'}</p>
                  <p>Team Name: ${item.TeamName || 'Unknown'}</p>
                  <p>Quantity: ${item.Quantity || 'Unknown'}</p>
                  <p>Quality: ${item.Quality || 'Unknown'}</p>
                  <p>Base Card: ${item.BaseCard || 'Unknown'}</p>
                  <p>Parallel: ${item.Parallel || 'Unknown'}</p>
                `;
                resultsContainer.appendChild(resultDiv);
              });
            } else {
              resultsContainer.innerHTML = '<p>No results found.</p>';
            }
          } catch (error) {
            console.error('Error fetching data:', error);
            resultsContainer.innerHTML = '<p>Error fetching data.</p>';
          }
        } else {
          resultsContainer.innerHTML = '<p>Please enter a search term.</p>';
        }
      });
      
});
