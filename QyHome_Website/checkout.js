window.onload = function() {
    // Retrieve shopping cart information from localStorage
    let listCartHTML = localStorage.getItem('listCart');
    let totalPriceHTML = localStorage.getItem('totalPrice');

    // Display shopping cart information on the checkout page
    document.querySelector('.listCart').innerHTML = listCartHTML;
    document.querySelector('.totalPriceRow').innerHTML = totalPriceHTML;

    // Add event listener to the "Confirm To Payment" button
    document.querySelector('#paymentMethod input[value="Continue To Payment"]').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent form submission
        
        // Reset shopping cart information
        localStorage.removeItem('listCart');
        localStorage.removeItem('totalPrice');

        let selectedMethod = document.getElementById('selectMethod').value;

        switch (selectedMethod) {
            case 'Credit/Debit Card':
                // Redirect to card.html
                window.location.href = 'card.html';
                break;
            case 'Public Bank Online Banking':
                // Open Public Bank website in a new tab
                window.open('https://www2.pbebank.com/myIBK/apppbb/servlet/BxxxServlet?RDOName=BxxxAuth&MethodName=login', '_blank');
                // Redirect to paymentSuccess.html after a delay
                setTimeout(function() {
                    window.location.href = 'paymentSuccess.html';
                }, 4000);
                break;
            case 'Maybank Online Banking':
                // Open Maybank website in a new tab
                window.open('https://www.maybank2e.com/SEA/m2e/portal/portal.view', '_blank');
                // Redirect to paymentSuccess.html after a delay
                setTimeout(function() {
                    window.location.href = 'paymentSuccess.html';
                }, 4000);
                break;
            case 'Hong Leong Bank Online Banking':
                // Open Hong Leong Bank website in a new tab
                window.open('https://s.hongleongconnect.my/rib/app/fo/login?web=1', '_blank');
                // Redirect to paymentSuccess.html after a delay
                setTimeout(function() {
                    window.location.href = 'paymentSuccess.html';
                }, 4000);
                break;
            default:
                alert('Please select a payment method.');
        }
    });

    // Add event listener to the "Cancel" button
    document.querySelector('#paymentMethod input[value="Cancel"]').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent form submission
        
        // Reset shopping cart information
        localStorage.removeItem('listCart');
        localStorage.removeItem('totalPrice');

        // Redirect to product2.html
        window.location.href = 'product2.html';
    });
};