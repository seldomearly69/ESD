document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('login-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Invalid username or password');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message);
            window.location.href = '/dashboard'; // Redirect to dashboard upon successful login
        })
        .catch(error => {
            console.error('Error:', error.message);
            document.getElementById('error-message').textContent = error.message;
        });
    });
});
