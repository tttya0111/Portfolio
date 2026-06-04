 // JavaScript to toggle the visibility of the content based on scroll position
 window.addEventListener('scroll', function() {
    var scrollPosition = window.scrollY || document.documentElement.scrollTop;
    
    // Adjust these values based on where you want the content to become visible
    var triggerScrollPosition1 = 300;
    var triggerScrollPosition2 = 1250;
    var triggerScrollPosition3 = 3000;
    var triggerScrollPosition4 = 3900;

    // Add more trigger scroll positions as needed
    
    // Toggle visibility of hidden content 1
    var hiddenContent1 = document.getElementById('videoContent');
    if (scrollPosition >= triggerScrollPosition1) {
        hiddenContent1.classList.add('visible');
    } else {
        hiddenContent1.classList.remove('visible');
    }
    
    // Toggle visibility of hidden content 2
    var hiddenContent2 = document.getElementById('productContent');
    if (scrollPosition >= triggerScrollPosition2) {
        hiddenContent2.classList.add('visible');
    } else {
        hiddenContent2.classList.remove('visible');
    }

     
    // Toggle visibility of hidden content 2
    var hiddenContent2 = document.getElementById('commentContent');
    if (scrollPosition >= triggerScrollPosition3) {
        hiddenContent2.classList.add('visible');
    } else {
        hiddenContent2.classList.remove('visible');
    }

     
    // Toggle visibility of hidden content 2
    var hiddenContent2 = document.getElementById('brandsContent');
    if (scrollPosition >= triggerScrollPosition4) {
        hiddenContent2.classList.add('visible');
    } else {
        hiddenContent2.classList.remove('visible');
    }
    
});