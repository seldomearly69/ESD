import countries from "../resources/countries.js";
const select = document.getElementById("country-code");
for (let key in countries){
    let option = document.createElement("option");
    option.value = countries[key];
    option.textContent = key;
    select.appendChild(option);
}
document.addEventListener("DOMContentLoaded", function() {
    const flightOption = document.getElementById("flight-option");
    const hotelOption = document.getElementById("hotel-option");
    const toggleButton = document.getElementById("toggle-button");
    const hotelSearchForm = document.getElementById("hotel-search-form");

    toggleButton.addEventListener("click", function() {
        flightOption.classList.toggle("hidden");
        hotelOption.classList.toggle("hidden");

        // Toggle button text based on the active interface
        if (flightOption.classList.contains("hidden")) {
            toggleButton.textContent = "Search for Hotels";
        } else {
            toggleButton.textContent = "Search for Flights";
        }
    });



    hotelSearchForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Get the form values
        const params = {};
        const values = ["query","check-in-date","check-out-date","hotel-adults","hotel-children","country-code"]
        for (let v of values){
            params[v] = document.getElementById(v).value;
        }

        // Store the form values in session storage
        sessionStorage.setItem("hParams", JSON.stringify(params))

        // // Redirect to another page
        window.location.href = "../Hotel Search/hotel.html"; // Change this to the desired page
    });
    
});


