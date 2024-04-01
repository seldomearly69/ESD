// script.js

document.addEventListener("DOMContentLoaded", function() {
    const cancelBookingForm = document.getElementById("cancel-booking-form");

    cancelBookingForm.addEventListener("submit", async function(event) {
        event.preventDefault(); // Prevent the default form submission
        document.getElementById('loading-indicator').classList.remove('hidden');
        
        const hotel = document.getElementById("hotel").value;
        const sdate = document.getElementById("sdate").value;
        const edate = document.getElementById("edate").value;

        console.log(hotel)
        console.log(sdate)
        console.log(edate)
        
        // Send cancellation request to backend
        const response = await fetch('http://localhost:8000/api/v1/delete_booking', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                hotel: hotel,
                dates: [sdate,edate]
            })
        });

        

        // Display cancellation results
        const resultsContainer = document.getElementById('cancel-results');
        resultsContainer.innerHTML = ''; // Clear previous results

        if (response.ok) {
            const data = await response.json();
            console.log(data);
            const cancelledBookings = data.Cancelled_Bookings;
            cancelledBookings.forEach(booking => {
                resultsContainer.innerHTML += `<p>Booking ID ${booking._id} cancelled successfully.</p>`;
            });
        } else if (response.status == 404) {
            resultsContainer.innerHTML = 'No bookings found.';
        }else{
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        document.getElementById('loading-indicator').classList.add('hidden');
        resultsContainer.classList.remove('hidden');
    });
});
