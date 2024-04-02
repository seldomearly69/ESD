const express = require("express");
const axios = require('axios');
const cors = require('cors');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');

const swaggerDocument = YAML.load('./swagger.yaml');
const app = express();
const PORT = process.env.PORT || 5013;

app.use(express.json());
app.use(cors());
app.use('/apidocs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));
// Endpoint for location validation
app.post('/validate-location', async (req, res) => {
    const { locationName, userCountry } = req.body;
    console.log('Validating location:', locationName, userCountry);

    try {
        // Call the error_handling microservice to validate location
        const response = await axios.post('http://host.docker.internal:5012/validate-location', {
            locationName,
            userCountry
        });
        console.log(response.data)
        res.json(response.data);
    } catch (error) {
        console.error('Error validating location:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});



// Endpoint for calculating distance between two points
app.post('/calculate-distance', async (req, res) => {
    console.log(req.body)
    const { coord1, coord2 } = req.body;

    try {
        // Call the simple microservice to calculate distance
        const response = await axios.post('http://host.docker.internal:5006/calculate-distance', {
            coord1,
            coord2
        });
        console.log(response.data)
        res.json(response.data);
    } catch (error) {
        console.error('Error calculating distance:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});



// Endpoint for geocoding a location
app.post('/geocode', async (req, res) => {
    console.log(req.body)
    const { locationName } = req.body;

    try {
        // Call the simple microservice for geocoding
        const response = await axios.post('http://host.docker.internal:5006/geocode', {
            locationName
        });
        console.log(response.data, "hi")
        res.json(response.data);
    } catch (error) {
        console.error('Error geocoding location:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});



// Endpoint to find booking by email
app.get('/routes/get/:email', async (req, res) => {
    const { email } = req.params;

    try {
        // Call the backend simple microservice to find bookings by email
        const response = await axios.get(`http://host.docker.internal:5001/routes/get/${email}`);
        console.log(response.data)
        res.json(response.data);
    } catch (error) {
        console.error('Error finding booking by email:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});



// Endpoint to save routes
app.put("/routes/save/:email", async (req, res) => {
    const { email } = req.params;
    console.log("Saving routes:", email, req.body)

    try {
        // Call the backend simple microservice to save routes
        const response = await axios.put(`http://host.docker.internal:5001/routes/save/${email}`, req.body, {
            headers: {
                "Content-Type": "application/json",
            },
        });
        console.log(response.data)
        res.json(response.data);
    } catch (error) {
        console.error("Error saving routes:", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Plan Route microservice is listening on port ${PORT}`);
});