document.addEventListener("DOMContentLoaded", function() {
    var isLoggedIn = localStorage.getItem('isLoggedIn');

    if (isLoggedIn === 'true') {
        document.getElementById('loginIcon').setAttribute('href', 'account.html');
    }

    document.getElementById('loginIcon').addEventListener('click', function() {
        var isLoggedIn = localStorage.getItem('isLoggedIn');
    
        if (isLoggedIn === 'true') {
            window.location.href = 'account.html';
        } else {
            formzoomout(); 
        }
    });
});

function formzoomout() {
    document.getElementById("accountform").style.display = "block";
    form.classList.add("zoomout");
}
