console.log(sessionStorage);
let fInfo = null;
let hInfo = null;
let total = 0;
let hotel_amt = 0;
let flight_amt = 0;
if (sessionStorage.getItem("hInfo") !== null){
    hInfo = JSON.parse(sessionStorage.getItem("hInfo"));
    console.log(hInfo);
   
    let d1 = new Date(hInfo.stay[0]);
    let d2 = new Date(hInfo.stay[1]);
    let daydiff = (d2.getTime() - d1.getTime())/1000/3600/24;
    total += hInfo.rate_per_night.lowest.slice(1) * hInfo.num_rooms * daydiff;
    //store the amount user pays for hotel
    hotel_amt = hInfo.rate_per_night.lowest.slice(1) * hInfo.num_rooms * daydiff;
    document.getElementsByClassName("selection")[0].innerHTML += `<h3>Hotel Details:</h3><br>`;
    document.getElementsByClassName("selection")[0].innerHTML += `
        <div class="hotel-card">
        <div class="hotel-info">
            <div class="hotel-name">` + hInfo.name + `</div>
            <div class="check-in-out">
                <div>Check-in: ` + String(new Date(hInfo.stay[0])).slice(0,-44) + `</div>
                <div>Check-out: ` + String(new Date(hInfo.stay[1])).slice(0,-44) + `</div>
            </div>
            <div class="number-of-rooms">No. of rooms: ` + hInfo.num_rooms + `</div>
        </div>
        <div class="sub-total">$` + hInfo.rate_per_night.lowest.slice(1) * hInfo.num_rooms * daydiff + `</div>
    </div>`;
}


if (sessionStorage.getItem("fInfo") !== null){
    fInfo = JSON.parse(sessionStorage.getItem("fInfo"));
    console.log(fInfo);
    document.getElementsByClassName("selection")[0].innerHTML += `<h3>Flight Details:</h3>`;
    fInfo.forEach((f,index) => {
        total += f.data.price;
        //store the amount user pays for flight
        flight_amt += f.data.price
        f.html = f.html.replace("Total:", "");
        let icon = "";
        if (index == 0){
            icon = "<i class='fa-solid fa-plane-departure'></i>";
        }else{
            icon = "<i class='fa-solid fa-plane-arrival'></i>";
        }
        
        document.getElementsByClassName("selection")[0].innerHTML += icon + "</div>" + f.html;
    });
}

document.getElementById("total-price").innerHTML = "$"+total;
function acknowledgeBooking(){
    document.getElementById('booking-success').classList.add('hidden');
    window.location.href ="../../templates/Nav/home.html";
}

document.addEventListener('DOMContentLoaded', function() {
    var stripe = Stripe('pk_test_51Op0OtL12QL7JE0gJTw6uqWwOwO8Ik9EDEa6S39Ef2znnSslMAz31UAbnPaqKQ0BdMLP3Oxn16QiqmDsc19JMA2A00tRo1uDkN');
    var elements = stripe.elements();
    var card = elements.create('card');
    card.mount('#card-element');
    
    var form = document.getElementById('payment-form');
    var displayError = document.getElementById('payment-errors');

    card.on('change', function(event) {
        console.log(event);
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });

    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        form.querySelector('button[type="submit"]').disabled = true;

    // Use Stripe to create a payment method with the card information
    let valid = true;
    await stripe.createPaymentMethod({
        type: 'card',
        card: card,
    }).then(function(result) {
        if (result.error) {
            // Inform the user if there was an error creating the payment method
            displayError.textContent = result.error.message;
            // Reset the submit button state to allow resubmission
            console.log("hi");
            form.querySelector('button[type="submit"]').disabled = false;
            valid = false;
        } else {
            // The card details are valid at this point, and you have a payment method ID
            displayError.textContent = '';

            // Hide the previous booking confirmation modal if necessary
        }
    })
    console.log("hi");
        if (!valid){
            return;
        }

    document.getElementById('booking-success').classList.remove('hidden');
    document.getElementById('loading-symbol').classList.remove('hidden');
    document.getElementById('success-message').classList.add('hidden');
    // Assuming there's an input with an id of 'amount' to specify the payment amount
    var amountInCents = parseInt(total) * 100;
    var amountInCentsHotel = parseInt(hotel_amt);
    var amountInCentsFlight = parseInt(flight_amt);
    console.log(amountInCents, amountInCentsFlight, amountInCentsHotel)

    fetch('http://localhost:8000/api/v1/payment', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        mode: "cors",
        body: JSON.stringify({amount: amountInCents})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        const clientSecret = data.clientSecret;
        const paymentIntent_id = data.paymentIntent_id
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {card: card}
        })
        .then(result => {
            if (result.error) {
                console.log(result.error.message);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    console.log('Payment succeeded!');

                    // Prepare booking info
                    let body = {paymentIntent_id: paymentIntent_id};
                    if (fInfo != null) {
                        body.flight = {"departure": fInfo[0].data, "amount": amountInCentsFlight};
                        if (fInfo.length==2){
                            body.flight.arrival = fInfo[1].data;
                        }
                    }
                    if (hInfo != null) {
                        body.hotel = {"hotel": hInfo, "amount": amountInCentsHotel};
                    }
                    body.dayTime = new Date();
                    body.email = sessionStorage.getItem("email");
                    console.log(body)
                    // Confirm booking
                    fetch('http://localhost:8000/api/v1/confirm_booking', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        mode: "cors",
                        body: JSON.stringify(body)
                    })
                    .then(response => {
                        if (response.status == 201){
                            return response.json();
                        }
                    })
                    .then(data => {
                        console.log(data);
                        document.getElementById('loading-symbol').classList.add('hidden');
                        document.getElementById('success-message').classList.remove('hidden');

                    })
                    .catch(error => {
                        console.log(error);
                    });
                }
            }
        });
    })
    .catch(error => console.error(error));
});
});
