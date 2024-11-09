document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

    form.addEventListener('input', function (event) {
        const target = event.target;

        switch (target.id) {
            case 'email':
                validateEmail(target);
                break;
            case 'cnp':
                validateCNP(target);
                break;
            case 'first_name':
            case 'last_name':
                validateName(target);
                break;
            case 'password':
                validatePassword(target);
                break;
            case 'age':
                validateAge(target);
                break;
        }
    });

    function validateEmail(input) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(input.value)) {
            setInvalid(input, 'Please enter a valid email address.');
        } else {
            clearInvalid(input);
        }
    }

    function validateCNP(input) {
        const cnpRegex = /^[1-9]\d{12}$/;
        if (!cnpRegex.test(input.value)) {
            setInvalid(input, 'CNP must be 13 digits.');
        } else {
            clearInvalid(input);
        }
    }

    function validateName(input) {
        if (input.value.trim() === '') {
            setInvalid(input, 'This field cannot be empty.');
        } else {
            clearInvalid(input);
        }
    }

    function validatePassword(input) {
        if (input.value.length < 6) {
            setInvalid(input, 'Password must be at least 6 characters.');
        } else {
            clearInvalid(input);
        }
    }

    function validateAge(input) {
        const age = parseInt(input.value, 10);
        if (isNaN(age) || age < 18) {
            setInvalid(input, 'You must be at least 18 years old.');
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
