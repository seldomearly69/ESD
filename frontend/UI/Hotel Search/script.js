let checkin = "";
let checkout = "";

function createHotelCard(hotel) {
    const hotelElement = document.createElement('div');
    hotelElement.classList.add('hotel-card');
    let desc = hotel.description;
    if (desc === undefined){
        desc = "A " + hotel.type;
        if (hotel.nearby_places.length > 0){
            desc += " near " + hotel.nearby_places[0].name;
        }else{
            desc += "in the middle of nowhere"
        }
    }
    hotelElement.innerHTML = `
        
        <div class="result-item">
            <img src="${hotel.images[0].thumbnail}" alt="Hotel Thumbnail" class="hotel-image">
            <div class = "hotel-wrapper">
            <h3 class="hotel-name">${hotel.name}</h3>
            <p class="hotel-description">${desc}</p>
            </div>
            <div class="sub-total">
                <span>${hotel.rate_per_night.lowest}</span> per night
            </div>
        </div>
    `;
    
    // Add event listener to the "Add to Booking Basket" button
    hotelElement.addEventListener('click', () => {
        seeHotelDetails(hotel);
    });

    return hotelElement;
}

function seeHotelDetails(hotel) {
    hotel.stay = [checkin,checkout];
    sessionStorage.setItem("hInfo",JSON.stringify(hotel));
    console.log(hotel);
    window.location.href = "../Hotel Info/info.html";

}

document.addEventListener("DOMContentLoaded", function() {
    const hotelSearchForm = document.getElementById("hotel-search-form");

    hotelSearchForm.addEventListener("submit", async function(event) {
        event.preventDefault(); // Prevent the default form submission
        document.getElementById('loading-indicator').classList.remove('hidden');
        checkin = document.getElementById("check-in-date").value;
        checkout = document.getElementById("check-out-date").value
        // Call backend to search
        
        const response = await fetch('http://localhost:5003/hotels', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({q: document.getElementById("query").value,
                    gl: "SG",
                    hl: "en",
                    currency: "SGD",
                    check_in_date: checkin,
                    check_out_date: checkout,
                    adults : 2,
                    children: 0
                    })
        })
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log(data);

        // Display search results
        const resultsContainer = document.getElementById('hotel-results');
        resultsContainer.innerHTML = ''; // Clear previous results

        if (data && data.cachedData) {
            // Display cached results
            const cachedResult = data.cachedData;
            const hotels = cachedResult.cachedResult;
            hotels.forEach(hotel => {
                const hotelElement = createHotelCard(hotel);
                resultsContainer.appendChild(hotelElement);
            });
        } else if (data && data.data) {
            // Display fresh results
            const freshResult = data.data;
            const hotels = freshResult.cachedResult;
            hotels.forEach(hotel => {
                const hotelElement = createHotelCard(hotel);
                resultsContainer.appendChild(hotelElement);
            });
        } else {
            resultsContainer.innerHTML = 'No results found.';
        }

        document.getElementById('loading-indicator').classList.add('hidden');
        resultsContainer.classList.remove('hidden');
    });
    
});




