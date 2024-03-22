var airports = [];

function convertTime(mins){
  mins = parseInt(mins);
  let hrs = Math.floor(mins/60);
  if (hrs>0){
    return String(hrs) + "H " + String(mins%60) + "m";
  }
  return String(mins%60) + "m";
  
}

fetch("../resources/airports.txt")
  .then(response => {
    if (!response.ok) {
      throw new Error('Failed to fetch file');
    }
    return response.text();
  })
  .then(text => {
    text.split('\n').forEach(function(line) {
        var parts = line.split(',');
        if (parts.length >= 14) {
          airports.push({
            label: parts[1] + ' (' + parts[2] + ')',
            value: parts[4]
          });
        }
      });
    
      ["departure-airport", "arrival-airport"].forEach(function(field) {
        $("#" + field).autocomplete({
          source: airports.map(function(airport) {
            return airport.label;
          }),
          select: function(event, ui) {
            var selectedAirport = airports.find(function(airport) {
              return airport.label === ui.item.value;
            });
            if (selectedAirport) {
              $("#error").text("");
              // Do something with the selected airport
              $("#" + field).attr("airport_code",selectedAirport.value);
              console.log($("#" + field));
              console.log("Selected " + field + ":", selectedAirport);
            } else {
              $("#error").text("Please select a valid " + field + ".");
            }
          }
        });
      });
  
  })
  .catch(error => {
    console.error('Error fetching file:', error);
  });


$(document).ready(function() {
  // Initially hide the to-date field
  $("#to-date-group").hide();

  // Show or hide to-date field based on flight type selection
  $("input[name='flight-type']").change(function() {
      if ($(this).val() === "1") {
          $("#to-date-group").show();
      } else {
          $("#to-date-group").hide();
      }
  });

  // Other JavaScript code
});

function createFlightCard(flight) {
  const flightElement = document.createElement('div');
  flightElement.classList.add('flight-card');
  flight.flights.forEach((f, i)=>{
    
    flightElement.innerHTML += `<div class="flight-segment">
        <span class="flight-airports">${f.departure_airport.id} → ${f.arrival_airport.id}</span>
        <span class="flight-timings">${f.departure_airport.time.slice(-4)} - ${f.arrival_airport.time.slice(-4)}</span>
    </div>`
    if (i<flight.layovers.length){
      console.log(flight.layovers[i].duration);
      let layover = convertTime(flight.layovers[i].duration);
      flightElement.innerHTML += `<div class="layover-info">Layover: ${layover} at ${flight.layovers[i].id}</div>`;
    }
    
  })
  flightElement.innerHTML += `<span class="flight-duration">${convertTime(flight.total_duration)}</span>`;
  flightElement.innerHTML += `<div class="total-cost">Total: $${flight.price}</div>`;
  
  // Add event listener to the "Add to Booking Basket" button
  flightElement.addEventListener('click', () => {
      seeHotelDetails(flight);
  });

  return flightElement;
}

function seeHotelDetails(flight) {
  sessionStorage.setItem("hInfo",JSON.stringify(flight));
  console.log(flight);
  // window.location.href = "../Hotel Info/info.html";

}

document.addEventListener("DOMContentLoaded", function() {
  const flightSearchForm = document.getElementById("flight-search-form");
  
  flightSearchForm.addEventListener("submit", async function(event) {
      event.preventDefault(); // Prevent the default form submission
      const params = {
        engine:"google_flights",
        currency: "SGD",
        hl: "en",
        api_key: "f3f6e4266e8a55e158eccff91716b1033839ff2368200bf47edd94ef78e8484b",
      }

      console.log(document.getElementById("departure-airport"));
      let did = $("#departure-airport").attr("airport_code");
      did = did.replace(/["\\]/g,"");
      params.departure_id = did;
      let aid = $("#arrival-airport").attr("airport_code");
      aid = aid.replace(/["\\]/g,"");
      params.arrival_id = aid;
      params.outbound_date = document.getElementById("from-date").value;

      document.getElementsByName('flight-type').forEach(radioButton => {

          if (radioButton.checked) {
              params.type = radioButton.value;
          }
      });
      
      if (params.type == "1"){
        params.return_date = document.getElementById("to-date").value;
      }
      params.travel_class = document.getElementById("travel-class").value;
      params.adults = document.getElementById("adults").value;
      params.children = document.getElementById("children").value;
      params.max_price = document.getElementById("max-price").value;
      params.email = sessionStorage.getItem("email");
      console.log(params);

      document.getElementById('loading-indicator').classList.remove('hidden');

      // Call backend to search
      
      const response = await fetch('http://localhost:5007/flights', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          mode: "cors",
          body: JSON.stringify(params)
      })
      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log(data);

      // Display search results
      const resultsContainer = document.getElementById('flight-results');
      resultsContainer.innerHTML = ''; // Clear previous results

      if (data) {
          let flights = [];
          if ("best_flights" in data){
            flights = data.best_flights;
            console.log(flights);
          }else{
            flights = data.other_flights;
            console.log(flights,1);
          }
          flights.forEach(flight => {
              const flightElement = createFlightCard(flight);
              resultsContainer.appendChild(flightElement);
          });
      } else {
          resultsContainer.innerHTML = 'No results found.';
      }

      document.getElementById('loading-indicator').classList.add('hidden');
      resultsContainer.classList.remove('hidden');
  });
  
});
