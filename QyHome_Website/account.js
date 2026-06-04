document.getElementById('loginIcon').addEventListener('click', function() {
    window.location.href = 'account.html';
});

function setLoginStatus(status) {
    localStorage.setItem('isLoggedIn', status);
}

function LogOut() {
    setLoginStatus('false');
    window.location.href = 'index.html';
}