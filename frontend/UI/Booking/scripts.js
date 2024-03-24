console.log(sessionStorage);
if (sessionStorage.getItem("fInfo") !== null){
    const fInfo = JSON.parse(sessionStorage.getItem("fInfo"));
    console.log(fInfo);
    document.getElementsByClassName("selection")[0].innerHTML += `<h3>Flight Details:</h3>` + fInfo[1].html;
}