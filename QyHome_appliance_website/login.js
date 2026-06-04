const togglePassword1 = document.getElementById('togglepassword1');
const togglePassword = document.getElementById('togglepassword');
const togglePassword2 = document.getElementById('togglepassword2');
const password = document.getElementById('password');
const resetpassword = document.getElementById('resetpassword');
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
togglePassword.addEventListener('click', function(e) {
    const type = resetpassword.getAttribute('type') === 'password' ? 'text' : 'password';
    resetpassword.setAttribute('type', type);
    if (togglePassword.src.match("Icon/LoginRegister/visibleeye.webp")){
        togglePassword.src = "Icon/LoginRegister/eyenotvisible.png"; 
    } else{
        togglePassword.src = "Icon/LoginRegister/visibleeye.webp";
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

function setLoginStatus(status) {
    localStorage.setItem('isLoggedIn', status);
}

function resetpassword1() {
    hideAllForms();
    document.getElementById("step1").style.display = "block";
}

function hideAllForms() {
    var forms = document.getElementsByClassName("popupForm2");
    for (var i = 0; i < forms.length; i++) {
    forms[i].style.display = "none";
    }
}

function isValidPassword(password) {
    var passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{8,}$/;
    return passwordRegex.test(password);
}

function displayPasswordForm(formId) {
    hideAllForms();  
    document.getElementById(formId).style.display = "block";
}

const passwordInput = document.getElementById('resetpassword');
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