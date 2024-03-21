var hotel = JSON.parse(sessionStorage.getItem("hInfo"));

if (hotel === null){
    window.location.href = "../User Home/home.html";
}
console.log(hotel);
document.getElementsByClassName("hotel-name")[0].innerHTML = hotel.name;
if (hotel.description !== undefined){
    document.getElementsByClassName("description")[0].innerHTML = hotel.description;
}
if (hotel.extracted_hotel_class !== undefined){
    document.getElementsByClassName("hotel-class")[0].innerHTML = hotel.extracted_hotel_class + " star " + hotel.type;
}else{
    document.getElementsByClassName("hotel-class")[0].innerHTML = hotel.type.charAt(0).toUpperCase() + hotel.type.slice(1);
}

document.getElementsByClassName("lowest-rate")[0].innerHTML = "From $" + hotel.rate_per_night.lowest.slice(4) + " per night";
document.getElementsByClassName("check-in-out")[0].innerHTML = "Check-in: " + hotel.check_in_time + " | Check-out: " + hotel.check_out_time;
const amenities = document.getElementsByClassName("amenities-list")[0];
for (let a of hotel.amenities){
    const amenityElement = document.createElement("li");
    amenityElement.innerHTML = a
    amenities.appendChild(amenityElement)
}
const rating = hotel.overall_rating;
document.getElementsByClassName("rating-value")[0].innerHTML = rating;
for (let i = 0; i < Math.floor(rating); i++){
    document.getElementsByClassName("stars")[0].innerHTML += "<span class='star'>&#9733;</span>";
}

document.getElementsByClassName("reviews")[0].innerHTML = hotel.reviews + " Reviews";

const nearbyPlacesList = document.getElementsByClassName("nearby-places")[0].childNodes[3];
console.log(nearbyPlacesList)
for (let p of hotel.nearby_places){
    const placeElement = document.createElement("li");
    if (p.transportations.length > 0){
        placeElement.innerHTML = p.name + " (" + p.transportations[0].type + ": " + p.transportations[0].duration + ")";
    }
    
    nearbyPlacesList.appendChild(placeElement);
}

// Make booking

window.addEventListener('scroll', () => {
    // Show button when user scrolls down 200px from the top of the page
    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        scrollToTopBtn.style.display = 'block';
    } else {
        scrollToTopBtn.style.display = 'none';
    }
});
