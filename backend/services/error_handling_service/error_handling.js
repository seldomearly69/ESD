// const express = require('express')

// const api = express()

// const HOST = 'localhost'
// const PORT = 5006

// api.get('/test', (req,res) => {
//     res.send('Success')
// })


// api.listen(PORT, () => console.log(`API running at ${HOST}:${PORT}!`))





// TO DO: ADD LINK TO MAPBOX AND MAPBOX DIRECTIONS HERE


// Replace 'YOUR_MAPBOX_ACCESS_TOKEN' with your actual Mapbox access token
mapboxgl.accessToken = 'pk.eyJ1IjoiY3lydXMtdGFuIiwiYSI6ImNscTBydXh6ZDAxZGsyaXAxMnV3Y2lwbWEifQ.jfAQQFTfeVegGsuoaNh6Ow'; // Your Mapbox access token





// Function to check the validity of the location input
async function checkLocationValidity(locationName) {
    const response = await fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${locationName}.json?access_token=${mapboxgl.accessToken}`);
    const data = await response.json();
    if (data.features && data.features.length > 0) {
        const feature = data.features[0];
        const country = feature.context.find(context => context.id.startsWith('country'));
        const userCountry = await getUserCountry(); // Get the user's country
        if (country && country.text !== userCountry) {
            // Location is not in the same country
            return false;
        } else {
            // Location is in the same country
            return true;
        }
    } else {
        console.error(`Location '${locationName}' not found.`);
        return false; // Location not found
    }
}




// Event listener for input field change
document.getElementById('locationInputs').addEventListener('change', async function (e) {
    if (e.target.tagName === 'INPUT' && e.target.name === 'location') {
        const isValid = await checkLocationValidity(e.target.value);
        if (!isValid) {
            // Reset the input field value if location is not valid
            e.target.value = '';
            e.target.style.borderColor = 'red';
            // Display a message to the user indicating the restriction
            alert('Please enter a location within your country.');
        }
        else{
            e.target.style.borderColor = '';
        }
    }
});