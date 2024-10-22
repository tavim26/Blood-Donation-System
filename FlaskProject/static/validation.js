document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

    form.addEventListener('input', function (event) {
        const target = event.target;

        if (target.id === 'email') {
            validateEmail(target);
        } else if (target.id === 'cnp') {
            validateCNP(target);
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

    function setInvalid(input, message) {
        input.classList.add('is-invalid');
        let error = input.nextElementSibling;
        if (!error || !error.classList.contains('form-text')) {
            error = document.createElement('div');
            error.classList.add('form-text');
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
