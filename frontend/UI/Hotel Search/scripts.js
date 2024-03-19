
import countries from "../resources/countries.js";
    const select = document.getElementById("country-code");
    for (let key in countries){
        let option = document.createElement("option");
        option.value = countries[key];
        option.textContent = key;
        select.appendChild(option);
    }
var params = JSON.parse(sessionStorage.getItem("hParams"));
const paramNames = ["query","check-in-date","check-out-date","hotel-adults","hotel-children","country-code"]
async function search(){
    for (let p of paramNames){
        params[p] = document.getElementById(p).value
    }
    let b = JSON.stringify({
                
        q: params["query"],
        gl: params["country-code"],
        hl: "en",
        currency: "SGD",
        check_in_date: params["check-in-date"],
        check_out_date: params["check-out-date"],
        adults: Number(params["hotel-adults"]),
        children: Number(params["hotel-children"]),
    });

    try {
        const response = await fetch('http://localhost:5003/hotels', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: b
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
    } catch (error) {
        console.error('Error:', error);
    }
    return;
}



if (params === null){

    window.location.href = "../User Home/home.html";
}else{
    console.log(params);
    
    for (let p of paramNames){

        document.getElementById(p).value = params[p];
    }
    search();
}

document.getElementById('search-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    search();
});

// Scroll to top button functionality
const scrollToTopBtn = document.getElementById('scrollToTopBtn');

window.addEventListener('scroll', () => {
    // Show button when user scrolls down 200px from the top of the page
    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        scrollToTopBtn.style.display = 'block';
    } else {
        scrollToTopBtn.style.display = 'none';
    }
});

scrollToTopBtn.addEventListener('click', () => {
    // Scroll to the top of the page smoothly
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});


function createHotelCard(hotel) {
    const hotelElement = document.createElement('div');
    hotelElement.classList.add('hotel-card');
    let desc = hotel.description;
    if (desc === undefined){
        desc = "A " + hotel.type;
        if (hotel.nearby_places.length > 0){
            desc += " near " + hotel.nearby_places[0].name;
        }
    }
    hotelElement.innerHTML = `
        <h2>${hotel.name}</h2>
        <p>${desc}</p>
        <!-- Add more hotel details here -->
    `;
    
    // Add event listener to the "Add to Booking Basket" button
    hotelElement.addEventListener('click', () => {
        seeHotelDetails(hotel);
    });

    return hotelElement;
}

function seeHotelDetails(hotel) {
    sessionStorage.setItem("hInfo",JSON.stringify(hotel));
    console.log(hotel);
    window.location.href = "../Hotel Info/info.html";

}



