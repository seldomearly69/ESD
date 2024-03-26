const express = require("express");
const mongoose = require("mongoose")
const cors = require('cors');
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
app.use(cors())


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


app.post("/hotels", fetchHotels)


app.listen(5003, async () => {
    try{
        connectDB(process.env.mongoURL);
    }catch(e){
        console.log(e)
    }
    console.log(`Listening on port 5003...`)
    
})
