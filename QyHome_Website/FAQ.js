document.addEventListener("DOMContentLoaded", function() {
    let questions = document.querySelectorAll(".FAQ_question");
    questions.forEach(function(question) {
        question.addEventListener("click", function() {
            let answer = this.nextElementSibling;
            answer.classList.toggle("active");
        });
    });
});

function closeForm() {
    document.getElementById("accountform").style.display = "none";
}