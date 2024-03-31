const express = require("express");
const mongoose = require("mongoose")
const cors = require('cors');
const Hotel = require("./models/searchResults");
const { getJson } = require("serpapi");

const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');

const options = {
    failOnErrors: true, // Whether or not to throw when parsing errors. Defaults to false.
    definition: {
      openapi: '3.0.0',
      info: {
        title: 'Hotel search microservice',
        version: '1.0.0',
      },
      servers: [
            {
                url: "http://localhost:5003/"
            },
        ]
    },
    
    apis: ['./app.js'],
  };
  
const openapiSpecification = swaggerJsdoc(options);
//function to connect to DB 
const connectDB = async (url) => {
    max_tries = 20;
    attempt = 0;
    while(attempt < max_tries) {
        try{
            await mongoose.connect(url);
            console.log("Connected to DB!");
            break
        }catch(err){
            console.log("Connection to DB failed.Trying again...");
            console.log(err)
            attempt+=1;
        }
    }
    
}

const app = express();

app.use(express.json())
app.use(cors())
app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(openapiSpecification))

//get api results from google hotel and store in DB
const fetchHotels = async (req, res) => {
    console.log(req.body);
    const cachedData = await Hotel.findOne({searchParams: req.body});

    if(cachedData){
        console.log("I am a cached data...")
        return res.status(200).json({cachedData})
    }else{
        query_obj = {api_key: process.env.serpapiKey,...req.body};
        try{
            const result = await getJson(query_obj);
            console.log("I am fresh data...")
            const data = await Hotel.create({searchParams: result["search_parameters"], cachedResult: result["properties"]});
            return res.status(200).json({data})

        }catch(err) {
            console.log(err)
            return res.status(500).json({err})
        }
    }
}

/**
 * @swagger
 * /hotels:
 *  post:
 *    summary: Fetch hotels matching the user's query
 *    requestBody:
 *      required: true
 *      content:
 *        application/json:
 *          schema:
 *            type: object
 *            properties:
 *              engine:
 *                type: string
 *                description: The search engine to use (e.g., "google_hotels")
 *              q:
 *                type: string
 *                description: The search query (e.g., "Bali Resorts")
 *              check_in_date:
 *                type: string
 *                format: date
 *                description: The check-in date in YYYY-MM-DD format
 *              check_out_date:
 *                type: string
 *                format: date
 *                description: The check-out date in YYYY-MM-DD format
 *              adults:
 *                type: string
 *                description: The number of adults
 *              currency:
 *                type: string
 *                description: The currency for pricing (e.g., "USD")
 *              gl:
 *                type: string
 *                description: The geographic location (e.g., "us")
 *              hl:
 *                type: string
 *                description: The language (e.g., "en")
 *    responses:
 *      '200':
 *        description: Successful operation
 *        content:
 *          application/json:
 *            schema:
 *              type: object
 *              properties:
 *                data:
 *                  type: object
 *                  description: Data returned from the API
 *      '500':
 *        description: Internal server error
 *        content:
 *          application/json:
 *            schema:
 *              type: object
 *              properties:
 *                error:
 *                  type: string
 *                  description: Could not fetch hotels
 */
app.post("/hotels", fetchHotels)


app.listen(5003, async () => {
    try{
        connectDB(process.env.mongoURL);
    }catch(e){
        console.log(e)
    }
    console.log(`Listening on port 5003...`)
    
})
