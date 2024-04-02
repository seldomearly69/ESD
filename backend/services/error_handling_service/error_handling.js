const express = require("express");
const axios = require('axios');
const cors = require('cors');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');

const swaggerDocument = YAML.load('./swagger.yaml');

const app = express();
const PORT = process.env.PORT || 5012;

app.use(express.json());
app.use(cors());
app.use('/apidocs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// Function to check the validity of the location input
async function checkLocationValidity(locationName, userCountry) {

    try {
        const response = await axios.get(`https://api.mapbox.com/geocoding/v5/mapbox.places/${locationName}.json`, {
            params: {
                access_token: 'pk.eyJ1IjoiY3lydXMtdGFuIiwiYSI6ImNscTBydXh6ZDAxZGsyaXAxMnV3Y2lwbWEifQ.jfAQQFTfeVegGsuoaNh6Ow'
            }
        });
        const data = response.data;
        if (data.features && data.features.length > 0) {

            // Get the country of the location
            const country = data.features[0].place_name
            
            if (country.includes(userCountry)) {
                // Location is in the same country as the user's country
                return true;
            } else {
                // Location is not in the same country
                return false;
            }
        } else {
            // Location not found
            return false;
        }
    } catch (error) {
        // Error occurred during location validation
        console.error('Error while fetching location data:', error);
        return false;
    }
}

// Route for location validation
app.post('/validate-location', async (req, res) => {
    const locationName = req.body.locationName;
    const userCountry = req.body.userCountry;
    console.log(locationName, userCountry)
    
    try {
        const isValid = await checkLocationValidity(locationName, userCountry);
        return res.json({ isValid });
    } catch (error) {
        console.error('Error during location validation:', error);
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Error handling microservice is listening on port ${PORT}`);
});
