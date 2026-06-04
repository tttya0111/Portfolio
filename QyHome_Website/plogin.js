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
    var customerPhone = document.getElementById("phone").value.trim();
    var customerPassword = document.getElementById("password").value.trim();
    if (!customerPhone || !customerPassword) {
        alert("Please fill in all required fields.");
        return;
    }
    const CONSTANT_PHONE = "0123456789";
    const CONSTANT_PASSWORD = "Abc_12def";
    if (customerPhone === CONSTANT_PHONE && customerPassword === CONSTANT_PASSWORD) {
        setLoginStatus('true');
        alert("Login successful!!");
        window.location.href = "account.html";
    } else {
        alert("Incorrect email or password. Note that both fields may be case-sensitive. Please try again.");
    }
}

function GoToEmailLogin(event) {
    event.preventDefault();

    var formId = event.target.getAttribute('data-form');
    if (formId === 'phoneLogin') {
        window.location.href = "elogin.html";
    }
}

function GoToPhoneRegistration() {
    window.location.href = "pregister.html";
}

function validatePasswordStep(currentStep, nextStep, event) {
    event.preventDefault();
    const form = document.getElementById(currentStep);
    const inputs = form.getElementsByTagName("input");
    let isValid = true;

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
        alert("An verification sms has been sent to you. Please click on the link to reset your password.");
    }
    if (currentStep === 'step2') {
        alert("Reset password successful!!");
        window.location.href = "plogin.html";
    }
    if (nextStep) {
        displayPasswordForm(nextStep);
    }
}