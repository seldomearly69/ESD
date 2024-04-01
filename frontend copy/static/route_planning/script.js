var mapStyleSet = false;
var locations = [];
var currentMode = 'driving';
var savedRoutes = {};
mapboxgl.accessToken = 'pk.eyJ1IjoiY3lydXMtdGFuIiwiYSI6ImNscTBydXh6ZDAxZGsyaXAxMnV3Y2lwbWEifQ.jfAQQFTfeVegGsuoaNh6Ow'; // Your Mapbox access token


// Initialize the map
var map = new mapboxgl.Map({
    container: 'map',
    center: [-0.1276, 51.5072],
    zoom: 12,
});


async function getSavedRoutes() {
    const email = sessionStorage.getItem("email");
    const url = `http://localhost:8000/api/v1/routes/get/${email}`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            console.log(savedRoutes);
            savedRoutes = data.data.routes;
            console.log(savedRoutes);
        } else if (response.status === 404) {
            throw new Error("No saved routes");
        } else {
            throw new Error(response.status);
        }
    } catch (error) {
        console.log('Error:', error.message);
    }
    console.log(savedRoutes);
    return;
}



// Add event listener to save route button
document.getElementsByClassName('add-route-btn')[0].addEventListener('click', function (e) {

    // Get the modal
    var modal = document.getElementById("routeNamingModal");
    var span = document.getElementsByClassName("close-btn")[0];

    // When the user clicks the button, open the modal 
    modal.classList.remove("hidden");

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.classList.add("hidden");
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.classList.add("hidden");
        }
    }
    
})
function reloadSavedRoutes(){
    console.log(savedRoutes);
    const container = document.getElementsByClassName("saved-routes-content")[0];
    container.innerHTML = '';
    if (Object.keys(savedRoutes).length == 0){
        container.innerHTML = "<div>You have no saved routes</div>"
    }
    for (sr of Object.keys(savedRoutes)){
        const child = createSavedRouteElement(sr, savedRoutes[sr]);
        container.appendChild(child);
    }
    
}

function createSavedRouteElement(name, locs){
    const srElement = document.createElement('div');
    srElement.classList.add('saved-route-item');
    console.log(name);
    srElement.innerHTML = 
    `<span class="route-name">${name}</span>`;

    const btn = document.createElement('button');
    btn.classList.add('delete-route-btn');
    btn.innerHTML = `<i class="fa-solid fa-trash-can"></i>`;
    btn.addEventListener('click', function (e) {
        delete savedRoutes[name];
        reloadSavedRoutes();
    })
    srElement.appendChild(btn);
    // Add event listener to the "Add to Booking Basket" button
    srElement.addEventListener('click', () => {
        chooseRoute(locs);
    });


    return srElement;
}

function chooseRoute(locs){
    console.log(locs);
    const parent = document.getElementById('locationInputs');
    console.log(parent);
    parent.innerHTML = '';
    for (l of locs){
        console.log(l);
        addLocationInput(l);
    }
}
document.getElementById('route-naming-form').addEventListener('submit', function(event) {
    event.preventDefault();
    // Form is valid, you can proceed with your form submission actions here
    const routeName = document.getElementById('routeNameInput').value;
    console.log('Saving route with name:', routeName);
    document.getElementById('routeNamingModal').classList.add('hidden');
    const inputs = document.getElementsByName('location');
    var locs = [];
    for (i of inputs){
        locs.push(i.value);
    }
    savedRoutes[routeName] = locs;
    reloadSavedRoutes();
});



document.getElementsByClassName('save-all-btn')[0].addEventListener("click", function(event) {
    const email = sessionStorage.getItem("email");
    if (!email) {
        console.error("Email not found in session storage");
        return;
    }
    
    const url = `http://localhost:8000/api/v1/routes/save` + email;
    const options = {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(savedRoutes)
    };

    fetch(url, options)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error(response.status);
            }
        })
        .then(data => {
            console.log(data);
            alert("Routes saved successfully!");
        })
        .catch(error => {
            console.error('Error:', error.message);
            alert("Error saving routes. Please try again later.");
        });
});




// Add event listener to the location input field
document.querySelector('#locationInputs input[type="search"]').addEventListener('change', async function (e) {
    e.preventDefault(); // Prevent default form submission behavior

    // Get the entered location value
    const locationName = e.target.value;
    // Get the user's country
    try {
        const userCountry = await getUserCountry();
        const response = await fetch(`http://localhost:8000/api/v1/validate_location`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ locationName, userCountry }) // Include userCountry in the request body
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data);
            if (data.isValid)  {
                e.target.style.borderColor = 'grey';
                console.log('Location is valid');
            } else {
                // Reset the input field value if location is not valid
                e.target.value = '';
                e.target.style.borderColor = 'red';
                alert('Please enter a location within your country.');
            }
        } else {
            console.error('Server error:', response.statusText);
            alert('Error occurred while validating location. Please try again later.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred. Please try again later.');
    }
});






// Initialize event listeners for 'mouseenter' and 'mouseleave' for the route
map.on('mouseenter', 'route', function (e) {
    var coordinates = e.features[0].geometry.coordinates;
    var totalDistance = (distance / 1000).toFixed(2); // Convert meters to kilometers
    var totalTime = (duration / 60).toFixed(1); // Convert seconds to minutes

    var popup = new mapboxgl.Popup()
        .setLngLat(coordinates[0]) // Show popup on the first coordinate
        .setHTML(`<strong>Distance:</strong> ${totalDistance} km<br><strong>Time:</strong> ${totalTime} minutes`)
        .addTo(map);

    map.on('mouseleave', 'route', function () {
        popup.remove();
    });
});






// Event listeners for different mode buttons
var transportModesDropdown = document.getElementById('transportModes');

transportModesDropdown.addEventListener('change', function () {
    var selectedMode = transportModesDropdown.value;

    if (currentMode !== selectedMode) {
        updateMode(selectedMode);
    }
});


// Event listener for the "Bring me for a Tour!" button
var tourButton = document.getElementById('tourButton');
tourButton.addEventListener('click', function () {
    initiateTour();
});



// Event listeners for different time of day buttons
var dawnButton = document.getElementById('dawn');
dawnButton.addEventListener('click', function () {
    setLightPreset(6); // Set a specific hour for dawn
});

var dayButton = document.getElementById('day');
dayButton.addEventListener('click', function () {
    setLightPreset(12); // Set a specific hour for daytime
});

var duskButton = document.getElementById('dusk');
duskButton.addEventListener('click', function () {
    setLightPreset(18); // Set a specific hour for dusk
});





// Add event listener for automatic addition of waypoints when users input a location
document.getElementById('locationInputs').addEventListener('change', async function (e) {
    if (e.target.tagName === 'INPUT' && e.target.name === 'location' && e.target.value.trim() !== '') {
        // Get the entered location value
        const locationName = e.target.value;
        // Get the user's country
        try {
            const userCountry = await getUserCountry();
            const response = await fetch(`http://localhost:8000/api/v1/validate_location`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ locationName, userCountry }) // Include userCountry in the request body
            });

            if (response.ok) {
                const data = await response.json();
                console.log("SECOND HERE", data);

                if (data.isValid) {
                    await geocodeAndAddWaypoint(e.target.value);
                    setMapBounds(); // Set bounds based on new locations
                }
            }
        } catch (error) {
            console.error('Error adding waypoint:', error);
            // Handle errors here
        }
    }
});







document.getElementById('locationForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    
    // Clear old markers and route before adding new ones
    removeOldMarkersAndRoute();

    // Always set the mode to "driving"
    currentMode = "driving";

    var locationInputs = document.querySelectorAll('input[name="location"]');

    try {
        for (let i = 0; i < locationInputs.length; i++) {
            if (locationInputs[i].value.trim() !== '') {
                await geocodeAndAddWaypoint(locationInputs[i].value);
            }
        }
        setMapBounds(); // Set bounds based on new locations

        calculateRoute();
    } catch (error) {
        // Handle errors here
    }
});


var optimizeRouteButton = document.getElementById('optimizeRouteButton');

optimizeRouteButton.addEventListener('click', function () {
    calculateOptimalRoute();
});

// Function to update current mode
function updateMode(newMode) {
    currentMode = newMode;
    if (map.getLayer('route')) {
        map.removeLayer('route');
    }
    if (map.getSource('route')) {
        map.removeSource('route');
    }
    calculateRoute();
}


// Function to add the current location marker
function addCurrentLocationMarker() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var coordinates = [position.coords.longitude, position.coords.latitude];

            var marker = new mapboxgl.Marker({
                color: 'blue',
                draggable: false,
            });

            marker.setLngLat(coordinates).addTo(map);

            var popup = new mapboxgl.Popup({
                closeButton: false,
            })
                .setHTML('Your Current Location');

            marker.getElement().addEventListener('mouseover', function () {
                popup.setLngLat(marker.getLngLat()).addTo(map);
            });

            marker.getElement().addEventListener('mouseout', function () {
                popup.remove();
            });
        });
    } else {
        console.log('Geolocation is not supported by your browser');
    }
}




// Function to set the light preset based on time of day
function setLightPreset(userLocalTime) {
    var lightPreset = 'day'; // Default preset
    if (userLocalTime >= 5 && userLocalTime < 8) {
        lightPreset = 'dawn';
    } else if (userLocalTime >= 8 && userLocalTime < 18) {
        lightPreset = 'day';
    } else {
        lightPreset = 'dusk';
    }

    // Set the map's light preset based on the time of day
    map.setConfigProperty('basemap', 'lightPreset', lightPreset);
}






// Function to set the map style based on the user's local time
function setMapStyleBasedOnTime() {
    if (mapStyleSet) {
        return;
    }

    // Get the user's local time and set the appropriate style
    var userLocalTime = new Date().getHours();
    setLightPreset(userLocalTime);
    mapStyleSet = true;
}

// When the map is loaded and ready
map.on('style.load', function () {
    setMapStyleBasedOnTime();
});


// Function to get the user's country using Mapbox API
function getUserCountry() {
    return new Promise((resolve, reject) => {
        // Check if geolocation is supported by the browser
        if (navigator.geolocation) {
            // Get the user's current position with a success and error callback
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    // Retrieve the latitude and longitude coordinates
                    const latlng = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    };

                    // Use Mapbox API for reverse geocoding
                    fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${latlng.lng},${latlng.lat}.json?types=country&access_token=${mapboxgl.accessToken}`)
                        .then(response => {
                            if (!response.ok) {
                                throw new Error('Failed to fetch user country');
                            }
                            return response.json();
                        })
                        .then(data => {
                            if (data && data.features && data.features.length > 0) {
                                // Extract the country from the response
                                const userCountry = data.features[0].text;
                                resolve(userCountry);
                            } else {
                                reject(new Error('Country not found in response'));
                            }
                        })
                        .catch(error => {
                            console.error('Error getting user country:', error);
                            reject(error);
                        });
                },
                function(error) {
                    console.error('Error getting user location:', error);
                    reject(error);
                }
            );
        } else {
            console.log('Geolocation is not supported by your browser');
            reject(new Error('Geolocation not supported'));
        }
    });
}


// Function to add a new location input
function addLocationInput(value = null) {
    // Counter for location inputs
    let locationCount = document.querySelectorAll('input[name="location"]').length + 1;

    // Create a new location input field
    const newLocationInput = document.createElement('div');
    newLocationInput.classList.add('location-input');
    newLocationInput.innerHTML = `
        <label for="location${locationCount}">Location ${locationCount}:</label>
        <input type="search" name="location">
        <div class="location-images"></div>
    `;
    if (value != null){
        newLocationInput.children[1].value = value;
    }
    // Append the new location input
    document.getElementById('locationInputs').appendChild(newLocationInput);

    // Add event listener to the new location input field
    const newInputField = newLocationInput.querySelector('input[name="location"]');
    newInputField.addEventListener('change', async function (e) {
        e.preventDefault(); // Prevent default form submission behavior

        // Get the entered location value
        const locationName = e.target.value;
        // Get the user's country
        try {
            const userCountry = await getUserCountry();
            const response = await fetch(`http://localhost:8000/api/v1/validate_location`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ locationName, userCountry }) // Include userCountry in the request body
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data);
                if (data.isValid)  {
                    e.target.style.borderColor = 'grey';
                    console.log('Location is valid');
                } else {
                    // Reset the input field value if location is not valid
                    e.target.value = '';
                    e.target.style.borderColor = 'red';
                    alert('Please enter a location within your country.');
                }
            } else {
                console.error('Server error:', response.statusText);
                alert('Error occurred while validating location. Please try again later.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An unexpected error occurred. Please try again later.');
        }
    });
}





// Function to calculate the optimal route
async function calculateOptimalRoute() {
    const coordinates = locations.map(location => location.coordinates);

    const sequence = [0]; // Start with the first location as a seed

    while (sequence.length < coordinates.length) {
        let currentCoord = coordinates[sequence[sequence.length - 1]];
        let nearest = null;
        let minDistance = Number.MAX_VALUE;

        for (let i = 0; i < coordinates.length; i++) {
            if (!sequence.includes(i)) {
                try {
                    // Fetch the distance from the backend route
                    const response = await fetch(`http://localhost:8000/api/v1/calculate_distance`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ coord1: currentCoord, coord2: coordinates[i] })
                    });

                    if (!response.ok) {
                        throw new Error('Failed to fetch distance data');
                    }

                    const data = await response.json();
                    const dist = data.distance;

                    if (dist < minDistance) {
                        minDistance = dist;
                        nearest = i;
                    }
                } catch (error) {
                    console.error('Error fetching distance data:', error);
                    // Handle errors here
                }
            }
        }

        sequence.push(nearest);
    }


    const routeCoordinates = sequence.map(idx => coordinates[idx]);

    const waypoints = routeCoordinates.map(coord => ({
        coordinates: coord.join(','),
    }));

    const waypointsString = waypoints.map(waypoint => waypoint.coordinates).join(';');

    try {
        const response = await fetch(`https://api.mapbox.com/directions/v5/mapbox/${currentMode}/${waypointsString}?geometries=geojson&access_token=${mapboxgl.accessToken}`);
        const data = await response.json();

        if (data.routes && data.routes.length > 0) {
            const route = data.routes[0];
            const routeGeometry = route.geometry.coordinates;
            const distance = route.distance;
            const duration = route.duration;

            // Clear old route
            if (map.getLayer('route')) {
                map.removeLayer('route');
            }
            if (map.getSource('route')) {
                map.removeSource('route');
            }



            if (map.getLayer('optimizedRoute')) {
                map.removeLayer('optimizedRoute');
            }
            if (map.getSource('optimizedRoute')) {
                map.removeSource('optimizedRoute');
            }



            map.addLayer({
                id: 'optimizedRoute',
                type: 'line',
                source: {
                    type: 'geojson',
                    data: {
                        type: 'Feature',
                        properties: {},
                        geometry: {
                            type: 'LineString',
                            coordinates: routeGeometry,
                        },
                    },
                },
                layout: {
                    'line-join': 'round',
                    'line-cap': 'round',
                },
                paint: {
                    'line-color': 'blue',
                    'line-width': 5,
                },
            });

            map.on('mouseenter', 'optimizedRoute', function (e) {
                const totalDistance = (distance / 1000).toFixed(2); // Convert meters to kilometers
                const totalTime = (duration / 60).toFixed(1); // Convert seconds to minutes
        
                const coordinates = e.features[0].geometry.coordinates[0];
        
                const popup = new mapboxgl.Popup({
                    closeButton: false,
                })
                    .setLngLat(coordinates)
                    .setHTML(`<strong>Distance:</strong> ${totalDistance} km<br><strong>Time:</strong> ${totalTime} minutes`)
                    .addTo(map);
        
                map.on('mouseleave', 'optimizedRoute', function () {
                    popup.remove();
                });
            });
        }
    }
    catch (error) {
        console.error('Error calculating optimal route:', error);
        showErrorPopup('An error occurred while calculating the optimal route.');
    }
}





// Function to Geocode and Add Waypoint
function geocodeAndAddWaypoint(locationName) {
    return new Promise((resolve, reject) => {
        // Make a request to the backend route for geocoding
        fetch(`http://localhost:8000/api/v1/geocode`, {
        method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ locationName: locationName })
        })            
        .then(response => response.json())
            .then(data => {
                if (data.coordinates) {
                    var coordinates = data.coordinates;
    
                    var marker = new mapboxgl.Marker({
                        color: 'red',
                        draggable: false,
                    });

                    // Create a unique label for the waypoint
                    var label = document.createElement('div');
                    label.className = 'marker-label';
                    label.textContent = locations.length + 1;

                    // Add the label to the marker
                    marker.getElement().appendChild(label);

                    marker.setLngLat(coordinates).addTo(map);


                    var popup = new mapboxgl.Popup({
                        closeButton: false,
                    })
                        .setHTML(locationName);

                    marker.getElement().addEventListener('mouseover', function () {
                        popup.setLngLat(marker.getLngLat()).addTo(map);
                    });

                    marker.getElement().addEventListener('mouseout', function () {
                        popup.remove();
                    });

                    locations.push({
                        name: locationName,
                        coordinates: coordinates,
                        marker: marker,
                    });

                    resolve();
                } else {
                    console.error(`Location '${locationName}' not found.`);
                    reject();
                }
            })
            .catch(error => {
                console.error('Error geocoding location:', error);
                reject();
            });
    });
}


    

function calculateRoute() {
    var coordinates = locations.map(location => location.coordinates);
    var formattedCoordinates = coordinates.map(coords => coords.join(','));

    fetch(`https://api.mapbox.com/directions-matrix/v1/mapbox/${currentMode}/${formattedCoordinates.join(';')}?access_token=${mapboxgl.accessToken}`)
        .then(response => response.json())
        .then(data => {
            if (data.code === 'Ok') {
                var waypointsOrder = data.durations[0].reduce((order, _, index) => {
                    order[index] = locations[index];
                    return order;
                }, []);

                var orderedCoordinates = waypointsOrder.map(location => location.coordinates);

                fetch(`https://api.mapbox.com/directions/v5/mapbox/${currentMode}/${orderedCoordinates.join(';')}?geometries=geojson&access_token=${mapboxgl.accessToken}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.routes && data.routes.length > 0) {
                            var route = data.routes[0];
                            var routeCoordinates = route.geometry.coordinates;


                            var distance = route.distance;
                            var duration = route.duration;


                            map.addLayer({
                                id: 'route',
                                type: 'line',
                                source: {
                                    type: 'geojson',
                                    data: {
                                        type: 'Feature',
                                        properties: {},
                                        geometry: {
                                            type: 'LineString',
                                            coordinates: routeCoordinates,
                                        },
                                    },
                                },
                                layout: {
                                    'line-join': 'round',
                                    'line-cap': 'round',
                                },
                                paint: {
                                    'line-color': 'red',
                                    'line-width': 5,
                                },
                            });


                            // Event listener for showing route information on hover
                            map.on('mouseenter', 'route', function (e) {
                                var coordinates = e.features[0].geometry.coordinates;
                                var totalDistance = (distance / 1000).toFixed(2); // Convert meters to kilometers
                                var totalTime = (duration / 60).toFixed(1); // Convert seconds to minutes

                                var popup = new mapboxgl.Popup({
                                    closeButton: false,
                                })
                                    .setLngLat(coordinates[0]) // Show popup on the first coordinate
                                    .setHTML(`<strong>Distance:</strong> ${totalDistance} km<br><strong>Time:</strong> ${totalTime} minutes`)
                                    .addTo(map);

                                map.on('mouseleave', 'route', function () {
                                    popup.remove();
                                });
                            });


                        } else {
                            // Handle the case where no route is found
                            showErrorPopup('No route found for the selected mode.');
                            currentMode = 'driving'; // Set mode to 'driving' on error
                            calculateRoute();
                            setMapBounds();
                        }
                    })
                    .catch(error => {
                        console.error('Error calculating route:', error);
                        showErrorPopup('An error occurred while calculating the route.');
                        currentMode = 'driving'; // Set mode to 'driving' on error
                        calculateRoute();
                        setMapBounds();
                    });
            } else {
                console.error('Error calculating optimal waypoints order:', data.message);
                showErrorPopup('An error occurred while calculating waypoints order.');
                currentMode = 'driving'; // Set mode to 'driving' on error
                calculateRoute();
                setMapBounds();
            }
        })
        .catch(error => {
            console.error('Error calculating waypoints order:', error);
            showErrorPopup('An error occurred while calculating waypoints order.');
            currentMode = 'driving'; // Set mode to 'driving' on error
            calculateRoute();
            setMapBounds();
        });
}



// Function to show an error popup
function showErrorPopup(errorMessage) {
    // Get the current map center
    var center = map.getCenter();

    // Display the error popup at the current center
    new mapboxgl.Popup()
        .setLngLat(center)
        .setHTML(errorMessage)
        .addTo(map);
}

// Function to set map's bounds to fit all locations and routes
function setMapBounds() {
    if (locations.length === 0) {
        return;
    }

    var bounds = new mapboxgl.LngLatBounds();

    locations.forEach(location => {
        bounds.extend(location.coordinates);
    });

    map.fitBounds(bounds, {
        padding: 100,
        maxZoom: 15,
    });
}

// Function to remove old route and waypoints markers
function removeOldMarkersAndRoute() {
    // Remove old route line
    if (map.getLayer('route')) {
        map.removeLayer('route');
    }
    if (map.getSource('route')) {
        map.removeSource('route');
    }


    // Remove optimized route if it exists
    if (map.getLayer('optimizedRoute')) {
        map.removeLayer('optimizedRoute');
    }
    if (map.getSource('optimizedRoute')) {
        map.removeSource('optimizedRoute');
    }


    // Remove old waypoint markers
    locations.forEach(location => {
        location.marker.remove();
    });
    locations = [];
}


var defaultZoom = 12; // Define the default zoom level

// Function to initiate the tour
function initiateTour() {
    var locationsCoordinates = locations.map(location => location.coordinates);


    // Zoom and flyover to the first location
    map.flyTo({
        center: locationsCoordinates[0],
        zoom: 22,
        bearing: 0,
        pitch: 60,
        speed: 0.6, // Speed of the flyover
        essential: true
    });

    // Fly to the remaining locations one by one with a time delay between transitions
    for (let i = 1; i < locationsCoordinates.length; i++) {
        setTimeout(() => {
            map.flyTo({
                center: locationsCoordinates[i],
                zoom: 22,
                bearing: 0,
                pitch: 60,
                speed: 0.6,
                essential: true
            });

            if (i === locationsCoordinates.length - 1) {
                // After the last location, initiate the zoom-out to the default zoom level
                setTimeout(() => {
                    map.flyTo({
                        center: locationsCoordinates[i],
                        zoom: defaultZoom,
                        bearing: 0,
                        pitch: 20,
                        speed: 0.6,
                        essential: true
                    });
                }, 6000); // Adjust time delay before zooming out (6 seconds in this example)
            }

        }, i * 7000); // Time delay between transitions (7 seconds in this example)
    }
}



var customMarker = map.loadImage(
    'https://docs.mapbox.com/mapbox-gl-js/assets/custom_marker.png',
    function (error, image) {
        if (error) throw error;
        map.addImage('custom-marker', image);
    }
);

async function init(){
    await getSavedRoutes();
    reloadSavedRoutes();
    addCurrentLocationMarker();
}

init();

