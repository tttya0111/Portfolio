function validateLoginForm(formId, event) {
    event.preventDefault();
    var form = document.getElementById(formId);
    var inputs = form.getElementsByTagName("input");
    var isValid = true;
    var emailFilled = false;
    var passwordFilled = false;

    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].hasAttribute("required") && !inputs[i].value.trim()) {
            isValid = false;
            inputs[i].classList.add("error");
        } else {
            inputs[i].classList.remove("error");
        }
    }
    if (!isValid) {
        alert("Please fill in all required fields.");
        return;
    }
    var customerEmail = document.getElementById("email").value.trim();
    var customerPassword = document.getElementById("password").value.trim();
    if (!customerEmail || !customerPassword) {
        alert("Please fill in all required fields.");
        return;
    }
    const CONSTANT_EMAIL = "lowqy@gmail.com";
    const CONSTANT_PASSWORD = "Abc_12def";
    if (customerEmail === CONSTANT_EMAIL && customerPassword === CONSTANT_PASSWORD) {
        setLoginStatus('true');
        alert("Login successful!!");
        window.location.href = "account.html";
    } else {
        alert("Incorrect email or password. Note that both fields may be case-sensitive. Please try again.");
    }
}

function GoToPhoneLogin(event) {
    event.preventDefault();

    var formId = event.target.getAttribute('data-form');
    if (formId === 'emailLogin') {
        window.location.href = "plogin.html";
    }
}

function GoToEmailRegistration() {
    window.location.href = "eregister.html";
}

function validatePasswordStep(currentStep, nextStep, event) {
    event.preventDefault();
    const form = document.getElementById(currentStep);
    const inputs = form.getElementsByTagName("input");
    let isValid = true;

    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].hasAttribute("required") && !inputs[i].value.trim()) {
            isValid = false;
            inputs[i].classList.add("error");
        } else {
            inputs[i].classList.remove("error");
        }
    }

    if (!isValid) {
        alert("Please fill in all required fields.");
        return;
    }

    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type === "password") { 
            if (!isValidPassword(inputs[i].value.trim())) {
                isValid = false;
                inputs[i].classList.add("error");
                alert("Invalid password format. Must contain at least one number, one uppercase and lowercase letter, one special character, and be at least 8 or more characters.");
                return;
            }
        }
    }

    if (currentStep === 'step1') {
        alert("An verification email has been sent to you. Please click on the link to reset your password.");
    }
    if (currentStep === 'step2') {
        alert("Reset password successful!!");
        window.location.href = "elogin.html";
    }
    if (nextStep) {
        displayPasswordForm(nextStep);
    }
}