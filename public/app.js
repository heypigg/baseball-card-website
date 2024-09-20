document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const resultsContainer = document.getElementById('card-info');
    const updateForm = document.getElementById('update-form');

    if (!searchForm || !resultsContainer || !updateForm) {
        console.error('Error: One or more required elements not found');
        return;
    }

    // Handle search submission
    searchForm.addEventListener('submit', async (event) => {
        event.preventDefault();
      
        const playerName = document.getElementById('player-name').value.trim();
        const cardNumber = document.getElementById('card-number').value.trim();
      
        if (!playerName && !cardNumber) {
            resultsContainer.innerHTML = '<p>Please enter either a player name or card number.</p>';
            return;
        }

        let query = '';
        if (playerName) {
            query = `playerName=${encodeURIComponent(playerName)}`;
        } else if (cardNumber) {
            query = `cardNumber=${encodeURIComponent(cardNumber)}`;
        }

        // Search for the card in the database
        try {
            const response = await fetch(`http://localhost:5001/api/search-card?${query}`);
            const data = await response.json();
            console.log('Search Results:', data); // Debugging

            if (data.length > 0) {
                const card = data[0]; // Assume first result for simplicity

                // Display card details and prefill the update form
                resultsContainer.innerHTML = `
                    <h3>${card.PlayerName}</h3>
                    <p>Card Number: ${card.CardNumber}</p>
                    <p>Team Name: ${card.TeamName || 'Unknown'}</p>
                `;

                document.getElementById('quantity').value = card.Quantity || '';
                document.getElementById('quality').value = card.Quality || '';
                document.getElementById('base-card').value = card.BaseCard || '';
                document.getElementById('parallel').value = card.Parallel || '';

                // Show the update form
                updateForm.style.display = 'block';

                // Handle form submission for updating the card
                updateForm.addEventListener('submit', async (event) => {
                    event.preventDefault();

                    const updatedData = {
                        Quantity: document.getElementById('quantity').value,
                        Quality: document.getElementById('quality').value,
                        BaseCard: document.getElementById('base-card').value,
                        Parallel: document.getElementById('parallel').value
                    };

                    // Send the updated data to the backend
                    try {
                        const updateResponse = await fetch(`http://localhost:5001/api/cards/${card.CardNumber}`, {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(updatedData)
                        });

                        if (updateResponse.ok) {
                            resultsContainer.innerHTML += '<p>Card updated successfully!</p>';
                        } else {
                            throw new Error('Error updating the card');
                        }
                    } catch (error) {
                        console.error('Error updating card:', error);
                        resultsContainer.innerHTML += '<p>Error updating card.</p>';
                    }
                });
            } else {
                resultsContainer.innerHTML = '<p>No results found.</p>';
            }
        } catch (error) {
            console.error('Error fetching data:', error);
            resultsContainer.innerHTML = '<p>Error fetching data.</p>';
        }
    });
});