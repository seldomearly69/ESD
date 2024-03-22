var airports = [];

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

// function createFlightCard(flight) {
//   const flightElement = document.createElement('div');
//   flightElement.classList.add('flight-card');
//   let desc = hotel.description;
//   if (desc === undefined){
//       desc = "A " + hotel.type;
//       if (hotel.nearby_places.length > 0){
//           desc += " near " + hotel.nearby_places[0].name;
//       }else{
//           desc += "in the middle of nowhere"
//       }
//   }
//   flightElement.innerHTML = `
//       <div class="flight-info">
//           <div class="airports">
//               <span class="departure-airport">JFK</span> to <span class="arrival-airport">LAX</span>
//           </div>
//           <div class="flight-timing">
//               <span class="departure-time">08:00 AM</span> - <span class="arrival-time">11:00 AM</span>
//           </div>
//           <div class="flight-duration">Duration: 6h</div>
//           <div class="layovers">1 layover (ORD)</div>
//       </div>
//       <div class="flight-cost">
//           $349 per pax
//       </div>
//   `;
  
//   // Add event listener to the "Add to Booking Basket" button
//   hotelElement.addEventListener('click', () => {
//       seeHotelDetails(hotel);
//   });

//   return hotelElement;
// }

// function seeHotelDetails(hotel) {
//   sessionStorage.setItem("hInfo",JSON.stringify(hotel));
//   console.log(hotel);
//   window.location.href = "../Hotel Info/info.html";

// }

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

  //     // Display search results
  //     const resultsContainer = document.getElementById('hotel-results');
  //     resultsContainer.innerHTML = ''; // Clear previous results

  //     if (data && data.cachedData) {
  //         // Display cached results
  //         const cachedResult = data.cachedData;
  //         const hotels = cachedResult.cachedResult;
  //         hotels.forEach(hotel => {
  //             const hotelElement = createHotelCard(hotel);
  //             resultsContainer.appendChild(hotelElement);
  //         });
  //     } else if (data && data.data) {
  //         // Display fresh results
  //         const freshResult = data.data;
  //         const hotels = freshResult.cachedResult;
  //         hotels.forEach(hotel => {
  //             const hotelElement = createHotelCard(hotel);
  //             resultsContainer.appendChild(hotelElement);
  //         });
  //     } else {
  //         resultsContainer.innerHTML = 'No results found.';
  //     }

  //     document.getElementById('loading-indicator').classList.add('hidden');
  //     resultsContainer.classList.remove('hidden');
  });
  
});
