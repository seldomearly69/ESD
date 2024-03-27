// script.js

document.addEventListener("DOMContentLoaded", function() {
    const cancelBookingForm = document.getElementById("cancel-booking-form");

    cancelBookingForm.addEventListener("submit", async function(event) {
        event.preventDefault(); // Prevent the default form submission
        document.getElementById('loading-indicator').classList.remove('hidden');
        
        const bookingId = document.getElementById("booking-id").value;
        const email = document.getElementById("email").value;
        
        // Send cancellation request to backend
        const response = await fetch('http://localhost:5010/delete_bookings', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                booking_id: bookingId,
                email: email
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);

        // Display cancellation results
        const resultsContainer = document.getElementById('cancel-results');
        resultsContainer.innerHTML = ''; // Clear previous results

        if (data && data.Cancelled_Bookings) {
            const cancelledBookings = data.Cancelled_Bookings;
            cancelledBookings.forEach(booking => {
                resultsContainer.innerHTML += `<p>Booking ID ${booking.booking_id} cancelled successfully.</p>`;
            });
        } else {
            resultsContainer.innerHTML = 'No bookings cancelled.';
        }

        document.getElementById('loading-indicator').classList.add('hidden');
        resultsContainer.classList.remove('hidden');
    });
});
