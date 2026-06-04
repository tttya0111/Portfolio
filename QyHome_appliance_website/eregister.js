function validateSignUpForm(formId, nextFormId, event) {
    event.preventDefault();
    var form = document.getElementById(formId);
    var inputs = form.getElementsByTagName("input");
    var isValid = true;

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
        if (inputs[i].type === "email") {
            if (!isValidEmail(inputs[i].value.trim())) {
                isValid = false;
                inputs[i].classList.add("error");
                alert("Invalid email format.");
                return;
            }
        } else if (inputs[i].type === "tel") { 
            if (!isValidPhoneNumber(inputs[i].value.trim())) {
                isValid = false;
                inputs[i].classList.add("error");
                alert("Invalid phone number format.");
                return;
            }
        } else if (inputs[i].name === "custpostal") { 
            if (!isValidPostalCode(inputs[i].value.trim())) {
                isValid = false;
                inputs[i].classList.add("error");
                alert("Invalid postal code format. Five digits postal code.");
                return;
            }
        } else if (inputs[i].type === "password") { 
            if (!isValidPassword(inputs[i].value.trim())) {
                isValid = false;
                inputs[i].classList.add("error");
                alert("Invalid password format. Must contain at least one number, one uppercase and lowercase letter, one special character, and be at least 8 or more characters.");
                return;
            }
        }
    }

    var agreementCheckbox = document.getElementById("agreement");
    if (formId === 'eregister1') {
        alert("An verification email has been sent to you. Please click on the link to complete the verification process.");
        alert("Verify email successful!!");
    }
    
    if (formId === 'eregister4') {
        if (!agreementCheckbox.checked) {
            alert("Please agree to the terms before continuing.");
            return;
        } else {
            alert("Sign up successful!!");
            window.location.href = "elogin.html";
            return;
        }
    }

    if (nextFormId) {
        displaySignUpForm(nextFormId);
    }
}

function goToPhoneRegistration(event) {
    event.preventDefault();

    var formId = event.target.getAttribute('data-form');
    if (formId === 'eregister') {
        window.location.href = "pregister.html";
    }
}