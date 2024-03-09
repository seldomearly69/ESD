const mongoose = require("mongoose");

/**
 1) Checkin date
 2) Checkout date
 3) Query(q)
 4) gl(Parameter defines the country to use for the Google Hotels search. It's a two-letter country code)
 */


 /**
   {
      "type": "hotel",
      "name": "The Ritz-Carlton, Bali",
      "description": "Zen-like quarters, some with butler service, in an upscale property offering refined dining & a spa.",
      "logo": "https://www.gstatic.com/travel-hotels/branding/df3424c9-7799-4d27-aeb5-cdcabf8bf950.png",
      "sponsored": true,
      "gps_coordinates": {
        "latitude": -8.830670999999999,
        "longitude": 115.21533099999999
      },
      "check_in_time": "3:00 PM",
      "check_out_time": "12:00 PM",
      "rate_per_night": {
        "lowest": "$347",
        "extracted_lowest": 347,
        "before_taxes_fees": "$287",
        "extracted_before_taxes_fees": 287
      },
      "prices": [
        {
          "source": "The Ritz-Carlton, Bali",
          "logo": "https://www.gstatic.com/travel-hotels/branding/df3424c9-7799-4d27-aeb5-cdcabf8bf950.png",
          "rate_per_night": {
            "lowest": "$347",
            "extracted_lowest": 347,
            "before_taxes_fees": "$287",
            "extracted_before_taxes_fees": 287
          }
        }
      ],
      "nearby_places": [
        {
          "name": "I Gusti Ngurah Rai International Airport",
          "transportations": [
            {
              "type": "Taxi",
              "duration": "29 min"
            }
          ]
        },
        {
          "name": "Bejana, Indonesian Restaurant at The Ritz-Carlton, Bali",
          "transportations": [
            {
              "type": "Walking",
              "duration": "1 min"
            }
          ]
        }
      ],
      "hotel_class": "5-star hotel",
      "extracted_hotel_class": 5,
      "images": [
        {
          "thumbnail": "https://lh3.googleusercontent.com/proxy/3GU0rF7c5y00MbsWRPAkzdY0Mql0YhH7coFNK9nRDE8GwlzsRbc7xHB8lu8ZN6ApPUiuM7GvjB4RWoJaQCcD4kjARaoyDitH27WhWiAdz8dfG4TCY6pafMo52UQH5W76rgH3JESuGN3ohZ20fEwSgBKGmdQZOA=s287-w287-h192-n-k-no-v1",
          "original_image": "https://d2hyz2bfif3cr8.cloudfront.net/imageRepo/7/0/151/470/91/rz-dpssw-private-pool-29237_Classic-Hor_O.jpg"
        },
        {
          "thumbnail": "https://lh5.googleusercontent.com/proxy/IUakfiu-4guLHoPdx1ippkGtRxwdDW9pxf3j8kRq8FtIKOnnCepdr1DBB1vDftDvbY1IDqTCsgzrvgXdzBB6sJU8-z-7yawWRg-tsLlqSy9XI9mbudAurUnJBm9tmF4sJJFZXkuiyUc7zaNMZ6XPZ3MJDhEzWw=s287-w287-h192-n-k-no-v1",
          "original_image": "https://d2hyz2bfif3cr8.cloudfront.net/imageRepo/7/0/147/874/299/dpssw-villa-0105-hor-clsc_O.jpg"
        },
        {
          "thumbnail": "https://lh6.googleusercontent.com/proxy/MWhomwXIPhVXgnq1drMsEuPzTr2FB1f5ePbnpGxtyxwOcB0zr7xKrN34pDzJQVEPRJxFtaSFKfGngytJW4jO2c_9jiVCQuOb6OgRBqn-TEAI172VO2Ptx3G1bx1OpnvBsIcIhTk4ZoNH4EWwUIRxEgVoYQg2EQ=s287-w287-h192-n-k-no-v1",
          "original_image": "https://d2hyz2bfif3cr8.cloudfront.net/imageRepo/7/0/147/874/243/dpssw-villa-0107-hor-clsc_O.jpg"
        },
        ...
      ],
      "overall_rating": 4.6,
      "reviews": 3614,
      "location_rating": 2.8,
      "reviews_breakdown": [
        {
          "name": "Property",
          "description": "Property",
          "total_mentioned": 605,
          "positive": 534,
          "negative": 44,
          "neutral": 27
        },
        {
          "name": "Service",
          "description": "Service",
          "total_mentioned": 599,
          "positive": 507,
          "negative": 74,
          "neutral": 18
        },
        {
          "name": "Nature",
          "description": "Nature and outdoor activities",
          "total_mentioned": 256,
          "positive": 212,
          "negative": 29,
          "neutral": 15
        }
      ],
      "amenities": [
        "Free Wi-Fi",
        "Free parking",
        "Pools",
        "Hot tub",
        "Air conditioning",
        "Fitness centre",
        "Spa",
        "Beach access",
        "Bar",
        "Restaurant",
        "Room service",
        "Kitchen in some rooms",
        "Airport shuttle",
        "Full-service laundry",
        "Accessible",
        "Business centre",
        "Child-friendly",
        "Smoke-free property"
      ],
      "property_token": "ChcIyo2FjenOuZ8xGgsvZy8xdGYyMTV2aBAB",
      "serpapi_property_details_link": "<SerpApi JSON endpoint>"
    },
  */


const transportationSchema = new mongoose.Schema({
    type: String,
    duration: String
});

const nearbyPlaceSchema = new mongoose.Schema({
    name: String,
    transportations: [transportationSchema]
});

const ratePerNightSchema = new mongoose.Schema({
    lowest: String,
    extracted_lowest: Number,
    before_taxes_fees: String,
    extracted_before_taxes_fees: Number
});

const priceSchema = new mongoose.Schema({
    source: String,
    logo: String,
    rate_per_night: ratePerNightSchema
});

const reviewsBreakdownSchema = new mongoose.Schema({
    name: String,
    description: String,
    total_mentioned: Number,
    positive: Number,
    negative: Number,
    neutral: Number
});

const imageSchema = new mongoose.Schema({
    thumbnail: String,
    original_image: String
});

const hotelSchema = new mongoose.Schema({
    type: String,
    name: String,
    description: String,
    logo: String,
    sponsored: Boolean,
    gps_coordinates: {
    latitude: Number,
    longitude: Number
    },
    check_in_time: String,
    check_out_time: String,
    rate_per_night: ratePerNightSchema,
    prices: [priceSchema],
    nearby_places: [nearbyPlaceSchema],
    hotel_class: String,
    extracted_hotel_class: Number,
    images: [imageSchema],
    overall_rating: Number,
    reviews: Number,
    location_rating: Number,
    reviews_breakdown: [reviewsBreakdownSchema],
    amenities: [String],
    property_token: String,
    serpapi_property_details_link: String
});

    
const hotel_search = new mongoose.Schema({
    searchParams: {
        type: mongoose.Schema.Types.Mixed,
        required: [true, "Pls provide what you are searching for."],
        unique: true,
    },
    cachedResult: [hotelSchema]
})

module.exports = new mongoose.model("HotelSearch", hotel_search);