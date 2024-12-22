document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const errorMessageDiv = document.getElementById('error-message'); // Div-ul pentru mesajele de eroare

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Previne trimiterea formularului

        const formData = new FormData(form);
        fetch(form.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())  // Răspunsul va fi în format JSON
        .then(data => {
            if (data.success) {
                // Dacă signup-ul a reușit, redirecționează utilizatorul
                window.location.href = data.redirect_url;
            } else {
                // Afișează mesajul de eroare
                errorMessageDiv.textContent = data.message || 'There was an error with your signup.';
                errorMessageDiv.style.display = 'block';
            }
        })
        .catch(error => {
            // Erori de rețea
            errorMessageDiv.textContent = 'Network error. Please try again later.';
            errorMessageDiv.style.display = 'block';
        });
    });

    form.addEventListener('input', function (event) {
        const target = event.target;

        switch (target.id) {
            case 'cnp':
                validateCNP(target);
                break;
            case 'password':
                validatePassword(target);
                break;
            case 'repeat_password':
                validateRepeatPassword(target);
                break;
            case 'first_name':
            case 'last_name':
                validateName(target);
                break;
            case 'email':
                validateEmail(target);
                break;
        }
    });

    function validateCNP(input) {
        const cnpRegex = /^[0-9]{13}$/;
        if (!cnpRegex.test(input.value)) {
            setInvalid(input, 'CNP must be exactly 13 digits and contain only numbers.');
        } else {
            clearInvalid(input);
        }
    }

    function validatePassword(input) {
        const password = input.value;
        if (password.length < 8) {
            setInvalid(input, 'Password must be at least 8 characters.');
        } else {
            clearInvalid(input);
        }
    }

    function validateRepeatPassword(input) {
        const password = document.getElementById('password').value;
        const repeatPassword = input.value;
        if (password !== repeatPassword) {
            setInvalid(input, 'Passwords do not match.');
        } else {
            clearInvalid(input);
        }
    }

    function validateName(input) {
        const nameRegex = /^[A-Z][a-z]*$/;
        if (!nameRegex.test(input.value)) {
            setInvalid(input, 'First and Last name must start with a capital letter.');
        } else {
            clearInvalid(input);
        }
    }

    function validateEmail(input) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(input.value)) {
            setInvalid(input, 'Please enter a valid email address.');
        } else {
            clearInvalid(input);
        }
    }

    function setInvalid(input, message) {
        input.classList.add('is-invalid');
        let error = input.nextElementSibling;
        if (!error || !error.classList.contains('form-text')) {
            error = document.createElement('div');
            error.classList.add('form-text');
            error.style.color = 'red'; // Mesajul de eroare în roșu
            input.after(error);
        }
        error.textContent = message;
    }

    function clearInvalid(input) {
        input.classList.remove('is-invalid');
        let error = input.nextElementSibling;
        if (error && error.classList.contains('form-text')) {
            error.remove();
        }
    }
});
