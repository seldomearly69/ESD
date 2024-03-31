const express = require("express");
const axios = require('axios');
const cors = require('cors');


const app = express();
const PORT = process.env.PORT || 5013;

app.use(express.json());
app.use(cors());

// Endpoint for location validation
app.post('/validate-location', async (req, res) => {
    const { locationName, userCountry } = req.body;
    // console.log('Validating location:', locationName, userCountry);

    try {
        // Call the error_handling microservice to validate location
        const response = await axios.post('http://host.docker.internal:5012/validate-location', {
            locationName,
            userCountry
        });

        res.json(response.data);
    } catch (error) {
        console.error('Error validating location:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Plan Route microservice is listening on port ${PORT}`);
});