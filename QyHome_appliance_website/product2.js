let iconCart = document.querySelector('.icon-cart');
let closeCart = document.querySelector('.close');
let body = document.querySelector('body');
let totalQuantity = 0; // Variable to store the total quantity in the cart

iconCart.addEventListener('click', () => {
    body.classList.toggle('showCart');
});

closeCart.addEventListener('click', () => {
    body.classList.toggle('showCart');
});

// Add event listener to the "Reset" button
let resetButton = document.querySelector('.reset');

resetButton.addEventListener('click', () => {
    // Clear the content of the shopping cart
    let listCart = document.querySelector('.listCart');
    listCart.innerHTML = '';

    // Reset total quantity and update cart icon
    totalQuantity = 0;
    updateCartIconQuantity();

    // Reset total price
    let totalPriceRow = document.querySelector('.totalPriceRow');
    totalPriceRow.textContent = 'Total Price:';

    // Optionally, you can also reset any other related variables or state
});

// Function to update the total quantity displayed in the cart icon
function updateCartIconQuantity() {
    iconCart.querySelector('span').textContent = totalQuantity;
}

// Select all the "Add to Cart" buttons inside the product sections
let addToCartButtons = document.querySelectorAll('.addCart');

// Add click event listener to each button
addToCartButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Retrieve product information
        let productBox = button.closest('.box');
        let productName = productBox.querySelector('h3').textContent;
        let productPriceText;
        let productPrices = Array.from(productBox.querySelectorAll('.price2')).map(priceElement => {
            return parseFloat(priceElement.textContent.replace('RM', ''));
        });

        // Check if the product has a promotion price
        if (productPrices.length > 0) {
            // Select the lowest price from the promotion prices
            productPrice = Math.min(...productPrices);
        } else {
            // If no promotion price, use regular price
            productPriceText = productBox.querySelector('.price').textContent.trim();
            productPrice = parseFloat(productPriceText.replace('RM', ''));
        }

        // Create new item element for the cart
        let newItem = document.createElement('div');
        newItem.classList.add('item');
        newItem.dataset.name = productName;

        // Construct the HTML for the item
        newItem.innerHTML = `
            <div class="image">
                <img src="${productBox.querySelector('img').src}" alt="">
            </div>
            <div class="name">${productName}</div>
            <div class="quantity">1</div>
            <div class="price">${productPrice.toFixed(2)}</div>
        `;

        // Append the new item to the shopping cart
        let listCart = document.querySelector('.listCart');
        listCart.appendChild(newItem);

        // Increment total quantity and update cart icon
        totalQuantity++;
        updateCartIconQuantity();

        // Calculate total price
        let totalPrice = 0;
        let cartItems = document.querySelectorAll('.item');
        cartItems.forEach(item => {
            let price = parseFloat(item.querySelector('.price').textContent);
            let quantity = parseInt(item.querySelector('.quantity').textContent);
            totalPrice += price * quantity;
        });

        // Display total price
        let totalPriceRow = document.querySelector('.totalPriceRow');
        totalPriceRow.textContent = `Total Price: RM${totalPrice.toFixed(2)}`;
    });
});

// Add event listener to the CHECK OUT button
let checkOutButton = document.querySelector('.checkOut');

checkOutButton.addEventListener('click', () => {
    // Retrieve shopping cart information
    let listCartHTML = document.querySelector('.listCart').innerHTML;
    let totalPriceHTML = document.querySelector('.totalPriceRow').innerHTML;

    // Store the shopping cart information in localStorage
    localStorage.setItem('listCart', listCartHTML);
    localStorage.setItem('totalPrice', totalPriceHTML);

    // Redirect to the checkout page
    window.location.href = 'checkOut.html';
});

function closeForm() {
    document.getElementById("accountform").style.display = "none";
}