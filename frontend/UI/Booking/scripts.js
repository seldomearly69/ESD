console.log(sessionStorage);

if (sessionStorage.getItem("hInfo") !== null){
    const hInfo = JSON.parse(sessionStorage.getItem("hInfo"));
    console.log(hInfo);
    document.getElementsByClassName("selection")[0].innerHTML += `<h3>Hotel Details:</h3><br>`;
    document.getElementsByClassName("selection")[0].innerHTML += `
        <div class="hotel-card">
        <div class="hotel-info">
            <div class="hotel-name">` + hInfo.name + `</div>
            <div class="check-in-out">
                <div>Check-in: ` + String(new Date(hInfo.stay[0])).slice(0,-44) + `</div>
                <div>Check-out: ` + String(new Date(hInfo.stay[1])).slice(0,-44) + `</div>
            </div>
            <div class="number-of-rooms">No. of rooms: ` + hInfo.num_rooms + `</div>
        </div>
        <div class="sub-total">$` + hInfo.rate_per_night.lowest.slice(1) * hInfo.num_rooms + `</div>
    </div>`;
}


if (sessionStorage.getItem("fInfo") !== null){
    const fInfo = JSON.parse(sessionStorage.getItem("fInfo"));
    console.log(fInfo);
    document.getElementsByClassName("selection")[0].innerHTML += `<h3>Flight Details:</h3>`;
    fInfo.forEach((f,index) => {
        f.html = f.html.replace("Total:", "");
        let icon = "";
        if (index == 0){
            icon = "<i class='fa-solid fa-plane-departure'></i>";
        }else{
            icon = "<i class='fa-solid fa-plane-arrival'></i>";
        }
        
        document.getElementsByClassName("selection")[0].innerHTML += icon + "</div>" + f.html;
    });
}

document.getElementsByClassName("selection")[0].innerHTML+="<div class='total'> 750 </div>"
