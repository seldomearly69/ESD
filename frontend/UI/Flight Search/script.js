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


console.log(airports);
