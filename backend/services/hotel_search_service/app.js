const express = require("express");
const mongoose = require("mongoose")
const Hotel = require("./models/searchResults");
const { getJson } = require("serpapi");

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


//get api results from google hotel and store in DB
const fetchHotels = async (req, res) => {
    console.log(req.body);
    const cachedData = await Hotel.findOne({searchParams: {engine: "google_hotels",...req.body}});
    if(cachedData){
        console.log("I am a cached data...")
        return res.status(201).json({cachedData})
    }else{
        query_obj = {engine: "google_hotels",...req.body,api_key: process.env.serpapiKey};
        try{
            const result = await getJson(query_obj);
            console.log("I am fresh data...")
            const data = await Hotel.create({searchParams: result["search_parameters"], cachedResult: result["properties"]});
            return res.status(201).json({data})

        }catch(err) {
            console.log(err)
            return res.status(500).json({err})
        }
    }
}


app.post("/hotels", fetchHotels)


app.listen(3000, async () => {
    try{
        connectDB(process.env.mongoURL);
    }catch(e){
        console.log(e)
    }
    console.log(`Listening on port 3000...`)
    
})
