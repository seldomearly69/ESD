document.getElementById("register-form").addEventListener("submit", function(event) {
    event.preventDefault();
    
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    
    // Perform registration request
    if (document.getElementById("confirm-password").value==password){
        fetch("http://localhost:5002/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({email,password})
        })
        .then(response => {
            if (response.status == 201){
                alert("Registration Successful!");
                window.location.href = '../Login/login.html';
            }
            if (response.status == 400){
                throw new Error('Account already exists!');
            }
        })
        .catch(error => {
            console.error('Error:', error.message);
            document.getElementById('error-message').textContent = error.message;
        });
    }else{
        document.getElementById('error-message').textContent = "Password mismatch";
    }
});
