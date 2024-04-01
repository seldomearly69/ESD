
document.getElementById("register-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const errorDiv = document.getElementById('auth-error')
    var email = document.getElementById("register-email").value;
    var password = document.getElementById("register-password").value;
    
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
                window.location.href = '/login';
            }
            if (response.status == 400){
                throw new Error('Account already exists!');
            }
        })
        .catch(error => {
            console.error('Error:', error.message);
            errorDiv.innerHTML = error.message;
            errorDiv.classList.remove('hidden');
            errorDiv.classList.add('show');
            });
    }else{
        
        errorDiv.innerHTML = "Password mismatch";
        errorDiv.classList.remove('hidden');
        errorDiv.classList.add('show');
    }
});
