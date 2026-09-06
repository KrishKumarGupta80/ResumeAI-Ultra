window.onload = function () {

    let fill = document.querySelector(".fill");
    let score = fill.getAttribute("data-score");

    setTimeout(() => {
        fill.style.width = score + "%";
    }, 400);

    // animated counter
    let counter = document.getElementById("score");
    let val = 0;

    let interval = setInterval(() => {
        if (val >= score) clearInterval(interval);
        else counter.innerText = val++;
    }, 20);
};