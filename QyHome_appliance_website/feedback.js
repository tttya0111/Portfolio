let stars = document.getElementsByClassName("str");
let output = document.getElementById("output");

function star(n) {
    remove();
    for (let i = 0; i < n; i++) {
        if (n == 1) cls = "one";
        else if (n == 2) cls = "two";
        else if (n == 3) cls = "three";
        else if (n == 4) cls = "four";
        else if (n == 5) cls = "five";
        stars[i].className = "str " + cls;
    }
    output.innerText = "Rating is: " + n + "/5";
}

function remove() {
    let i = 0;
    while (i < 5) {
        stars[i].className = "str";
        i++;
    }
}

function openForm() {
    document.getElementById("commentForm").style.display = "block";
    document.body.classList.add('stopScroll');
}

function closeForm1() {
    document.getElementById("commentForm").style.display = "none";
    document.body.classList.remove('stopScroll');
}

$(document).ready(()=> {
    $("#open-button").click(function() {
        $("#commentForm").toggleClass("form-popup");
        if ($("#commentForm").hasClass("hidden")) {
            $("body").removeClass('stopScroll');
        } else {
            $("body").addClass('stopScroll');
        }
    });
});

function closeForm() {
    document.getElementById("accountform").style.display = "none";
}