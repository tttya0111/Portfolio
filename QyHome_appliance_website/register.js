const togglePassword1 = document.getElementById('togglepassword1');
const togglePassword2 = document.getElementById('togglepassword2');
const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirmpassword');
togglePassword1.addEventListener('click', function(e) {
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    if (togglePassword1.src.match("Icon/LoginRegister/visibleeye.webp")){
        togglePassword1.src = "Icon/LoginRegister/eyenotvisible.png"; 
    } else{
        togglePassword1.src = "Icon/LoginRegister/visibleeye.webp";
    }
});
togglePassword2.addEventListener('click', function(e) {
    const type = confirmPassword.getAttribute('type') === 'password' ? 'text' : 'password';
    confirmPassword.setAttribute('type', type);
    if (togglePassword2.src.match("Icon/LoginRegister/visibleeye.webp")){
        togglePassword2.src = "Icon/LoginRegister/eyenotvisible.png"; 
    } else{
        togglePassword2.src = "Icon/LoginRegister/visibleeye.webp";
    }
});

function isValidEmail(email) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPhoneNumber(phone) {
    var phoneRegex = /^\d{10,11}$/; 
    return phoneRegex.test(phone);
}

function isValidPostalCode(postal) {
    var postalRegex = /^\d{5}$/; 
    return postalRegex.test(postal);
}

function isValidPassword(password) {
    var passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{8,}$/;
    return passwordRegex.test(password);
}

function displaySignUpForm(formId) {
    hideAllForms();  
    document.getElementById(formId).style.display = "block";
}

function hideAllForms() {
    var forms = document.getElementsByClassName("loginregister");
    for (var i = 0; i < forms.length; i++) {
        forms[i].style.display = "none";
    }
}

const passwordInput = document.getElementById('password');
const requirementsLayout1 = document.querySelector('.requirementsLayout1');
const requirementsLayout2 = document.querySelector('.requirementsLayout2');
passwordInput.addEventListener('input', function() {
    const password = passwordInput.value.trim();
    const requirements = [
        /\d/.test(password),
        /[A-Z]/.test(password),
        /[a-z]/.test(password),
        /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password),
        password.length >= 8
    ];

    const listItems1 = requirementsLayout1.getElementsByTagName('li');
    const listItems2 = requirementsLayout2.getElementsByTagName('li');

    for (let i = 0; i < requirements.length; i++) {
        listItems1[i].classList.toggle('met', requirements[i]);
        listItems2[i].classList.toggle('met', requirements[i + 3]); 
    }
});
requirementsLayout1.style.display = 'block';
requirementsLayout2.style.display = 'block';