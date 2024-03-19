document.addEventListener("DOMContentLoaded", function() {
    const flightOption = document.getElementById("flight-option");
    const hotelOption = document.getElementById("hotel-option");
    const toggleButton = document.getElementById("toggle-button");

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
});


