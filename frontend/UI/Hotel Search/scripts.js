document.getElementById('search-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const checkinDate = document.getElementById('checkin-date').value;
    const checkoutDate = document.getElementById('checkout-date').value;
    const query = document.getElementById('query').value;
    const gl = document.getElementById('gl').value;

    try {
        const response = await fetch('/hotels', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                checkin_date: checkinDate,
                checkout_date: checkoutDate,
                q: query,
                gl: gl
            })
        });

        const data = await response.json();
        console.log(data);

        // Display search results
        const resultsContainer = document.getElementById('results');
        resultsContainer.innerHTML = ''; // Clear previous results

        if (data && data.cachedData) {
            // Display cached results
            const cachedResult = data.cachedData;
            const hotels = cachedResult.cachedResult;
            hotels.forEach(hotel => {
                const hotelElement = document.createElement('div');
                hotelElement.innerHTML = `
                    <h2>${hotel.name}</h2>
                    <p>${hotel.description}</p>
                    <!-- Add more hotel details here -->
                `;
                resultsContainer.appendChild(hotelElement);
            });
        } else if (data && data.data) {
            // Display fresh results
            const freshResult = data.data;
            const hotels = freshResult.cachedResult;
            hotels.forEach(hotel => {
                const hotelElement = document.createElement('div');
                hotelElement.innerHTML = `
                    <h2>${hotel.name}</h2>
                    <p>${hotel.description}</p>
                    <!-- Add more hotel details here -->
                `;
                resultsContainer.appendChild(hotelElement);
            });
        } else {
            resultsContainer.innerHTML = 'No results found.';
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
