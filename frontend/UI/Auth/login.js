// if (sessionStorage.getItem("email") !== null){
//     windows.location.href("../Nav/home.html");
// }

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('login-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

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
                window.location.href = '../Nav/home.html';
            }
        })
        .catch(error => {
            console.error('Error:', error.message);
            const errorDiv = document.getElementById('auth-error')
            errorDiv.innerHTML = error.message;
            errorDiv.classList.remove('hidden');
            errorDiv.classList.add('show');

        });
    });
});
