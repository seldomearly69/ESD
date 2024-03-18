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
            body: JSON.stringify({ email, password })
        })
        .then(response => {
            if (response.ok){
                
                // window.location.href = '/dashboard'; // Redirect to dashboard upon successful login
                window.location.href = '../Registration/register.html';
            }
            if (response.status == 404){
                throw new Error('User does not exist');
            }
            if (response.status == 400){
                throw new Error('Wrong password');
            }


            
        })
        .catch(error => {
            console.error('Error:', error.message);
            document.getElementById('error-message').textContent = error.message;
        });
    });
});
