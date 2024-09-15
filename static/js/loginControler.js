document.getElementById('floatingCpf').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, ''); // Remove all non-digit characters
    if (value.length > 11) {
        value = value.slice(0, 11); // Ensure it's no more than 11 digits
    }

    // Format: 000.000.000-00
    value = value.replace(/(\d{3})(\d)/, '$1.$2'); // Add the first dot
    value = value.replace(/(\d{3})(\d)/, '$1.$2'); // Add the second dot
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2'); // Add the dash

    e.target.value = value; // Set the formatted value back to the input
});

document.addEventListener('DOMContentLoaded', function () {
var toastEl = document.getElementById('liveToast');

// Verifica se o elemento do toast existe, para não tentar exibir o toast quando não há erro
if (toastEl) {
    var toast = new bootstrap.Toast(toastEl);
    toast.show(); // Exibe o toast apenas se ele estiver presente
}
});


const togglePassword = document.querySelector('#togglePassword');
const passwordField = document.querySelector('#floatingPassword');
const eyeIcon = document.querySelector('#eyeIcon');

togglePassword.addEventListener('click', function () {
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordField.setAttribute('type', type);
    
    if (type === 'password') {
        eyeIcon.classList.remove('bi-eye-slash-fill');
        eyeIcon.classList.remove('secondary-color-custom');
        eyeIcon.classList.add('bi-eye-fill');
        eyeIcon.classList.add('primary-color-custom');
    } else {
        eyeIcon.classList.remove('bi-eye-fill');
        eyeIcon.classList.remove('primary-color-custom');
        eyeIcon.classList.add('bi-eye-slash-fill');
        eyeIcon.classList.add('secondary-color-custom')
    }
});