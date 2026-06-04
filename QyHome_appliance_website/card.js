document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("card");

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        if (validateForm()) {
            window.location.href = "paymentSuccess.html";
            form.reset();
        }
    });

    const cancelButton = document.querySelector('input[value="Cancel"]');
    cancelButton.addEventListener("click", function() {
        window.location.href = "product2.html";
        form.reset();
    });

    const cardNumberInput = document.getElementById("cardNumber");
    const cvvInput = document.getElementById("cvv");

    cardNumberInput.addEventListener("input", function(event) {
        event.target.value = event.target.value.replace(/\D/g, "").slice(0, 16);
    });

    cvvInput.addEventListener("input", function(event) {
        event.target.value = event.target.value.replace(/\D/g, "").slice(0, 3);
    });

    function validateForm() {
        const name = document.getElementById("name").value;
        const cardNumber = cardNumberInput.value;
        const expirationMonth = document.getElementById("expirationDateMonth").value;
        const expirationYear = document.getElementById("expirationDateYear").value;
        const cvv = cvvInput.value;

        if (name === "" || cardNumber === "" || expirationMonth === "" || expirationYear === "" || cvv === "") {
            alert("Please fill in all fields.");
            return false;
        }

        return true;
    }
});