const express = require("express");
const axios = require('axios');
const cors = require('cors');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');

const swaggerDocument = YAML.load('./swagger.yaml');

const app = express();
const PORT = process.env.PORT || 5006;

app.use(express.json());
app.use(cors());
app.use('/apidocs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));



// Helper function to calculate distance between two points, helper function for optimized route
function calculateDistance(coord1, coord2) {
    const [x1, y1] = coord1;
    const [x2, y2] = coord2;
    return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
}

// Route for calculate distance between two points
app.post('/calculate-distance', (req, res) => {
    const { coord1, coord2 } = req.body;
    if (!coord1 || !coord2 || coord1.length !== 2 || coord2.length !== 2) {
        return res.status(400).json({ error: 'Invalid coordinates' });
    }
    const distance = calculateDistance(coord1, coord2);
    console.log(distance)
    res.json({ distance });
});





// Function to Geocode
async function geocode(locationName) {
    try {
        const response = await axios.get(`https://api.mapbox.com/geocoding/v5/mapbox.places/${locationName}.json`, {
            params: {
                access_token: 'pk.eyJ1IjoiY3lydXMtdGFuIiwiYSI6ImNscTBydXh6ZDAxZGsyaXAxMnV3Y2lwbWEifQ.jfAQQFTfeVegGsuoaNh6Ow'
            }
        });
        const data = response.data;
        if (data.features && data.features.length > 0) {
            const feature = data.features[0];
            const coordinates = feature.center;
            return coordinates;
        } else {
            console.error(`Location '${locationName}' not found.`);
            throw new Error(`Location '${locationName}' not found.`);
        }
    } catch (error) {
        console.error('Error geocoding location:', error);
        throw error;
    }
}

// Route for geocoding a location
app.post('/geocode', async (req, res) => {
    const { locationName } = req.body;
    try {
        const coordinates = await geocode(locationName);
        res.json({ coordinates });
    } catch (error) {
        res.status(500).json({ error: 'Failed to geocode location.' });
    }
});






// Start the server
app.listen(PORT, () => {
    console.log(`Route service microservice is listening on port ${PORT}`);
});