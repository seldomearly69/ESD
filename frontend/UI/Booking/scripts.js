console.log(sessionStorage);
let fInfo = null;
let hInfo = null;
let total = 0;
if (sessionStorage.getItem("hInfo") !== null){
    hInfo = JSON.parse(sessionStorage.getItem("hInfo"));
    console.log(hInfo);
    total += hInfo.rate_per_night.lowest.slice(1) * hInfo.num_rooms;
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
        <div class="sub-total">$` + hInfo.rate_per_night.lowest.slice(1) * hInfo.num_rooms + `</div>
    </div>`;
}


if (sessionStorage.getItem("fInfo") !== null){
    fInfo = JSON.parse(sessionStorage.getItem("fInfo"));
    console.log(fInfo);
    document.getElementsByClassName("selection")[0].innerHTML += `<h3>Flight Details:</h3>`;
    fInfo.forEach((f,index) => {
        total += f.data.price;
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
    window.location.href ="../Nav/home.html";
}

document.addEventListener('DOMContentLoaded', function() {
    var stripe = Stripe('pk_test_51Op0OtL12QL7JE0gJTw6uqWwOwO8Ik9EDEa6S39Ef2znnSslMAz31UAbnPaqKQ0BdMLP3Oxn16QiqmDsc19JMA2A00tRo1uDkN');
    var elements = stripe.elements();
    var card = elements.create('card');
    card.mount('#card-element');
    
    var form = document.getElementById('payment-form');
    var displayError = document.getElementById('payment-errors');

    card.on('change', function(event) {
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Assuming there's an input with an id of 'amount' to specify the payment amount
        var amountInCents = parseInt(total) * 100;
        console.log(amountInCents)

        fetch('http://127.0.0.1:5008/payment', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            mode: "cors",
            body: JSON.stringify({amount: amountInCents})
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            const clientSecret = data.clientSecret;

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
                        let body = {};
                        if (fInfo != null) {
                            body.flight = {"departure": fInfo[0].data, "arrival": fInfo[1].data};
                        }
                        if (hInfo != null) {
                            body.hotel = {"hotel": hInfo};
                        }
                        body.dayTime = new Date();
                        body.email = sessionStorage.getItem("email");
                        console.log(body)
                        // Confirm booking
                        fetch('http://127.0.0.1:5008/confirm_booking', {
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
                            document.getElementById('booking-success').classList.remove('hidden');
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
