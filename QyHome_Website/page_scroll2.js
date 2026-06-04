 // JavaScript to toggle the visibility of the content based on scroll position
 window.addEventListener('scroll', function() {
    var scrollPosition = window.scrollY || document.documentElement.scrollTop;
    
    // Adjust these values based on where you want the content to become visible
    var triggerScrollPosition6 = 500;
    var triggerScrollPosition7 = 1000;
    var triggerScrollPosition8 = 1500;

    // Add more trigger scroll positions as needed

    var hiddenContent2 = document.getElementById('mission');
    if (scrollPosition >= triggerScrollPosition6) {
        hiddenContent2.classList.add('visible');
    } else {
        hiddenContent2.classList.remove('visible');
    }

    var hiddenContent2 = document.getElementById('product');
    if (scrollPosition >= triggerScrollPosition7) {
        hiddenContent2.classList.add('visible');
    } else {
        hiddenContent2.classList.remove('visible');
    }

    var hiddenContent2 = document.getElementById('commitment');
    if (scrollPosition >= triggerScrollPosition8) {
        hiddenContent2.classList.add('visible');
    } else {
        hiddenContent2.classList.remove('visible');
    }


    
});