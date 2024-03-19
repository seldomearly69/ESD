document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('login-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        fetch('http://localhost:5002/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            mode: "cors",
            body: JSON.stringify({ email, password })
        })
        .then(response => {
            
            if (response.status == 404){
                throw new Error('User does not exist');
            }
            if (response.status == 400){
                throw new Error('Wrong password');
            }
            return response.json();
        })
        .then(data=>{

            sessionStorage.setItem('email', email);
            console.log(data);
            if (data.data.usertype == "customer"){
                window.location.href = '../User Home/home.html';
            }
        })
        .catch(error => {
            console.error('Error:', error.message);
            document.getElementById('error-message').textContent = error.message;
        });
    });
});
