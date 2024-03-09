document.getElementById("registrationForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    var username = document.getElementById("regUsername").value;
    var password = document.getElementById("regPassword").value;
    
    // Perform registration request
    fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password_hash: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.code === 201) {
            document.getElementById("message").innerText = "Registration successful!";
        } else {
            document.getElementById("message").innerText = data.message;
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
