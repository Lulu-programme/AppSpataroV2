function openMain(x) {
    let contents = document.querySelectorAll(".main-content");
    let btns = document.querySelectorAll(".btn-main");

    for (let i = 0; i < contents.length; i++) {
        contents[i].style.display = "none";
        btns[i].classList.remove("active");
    }

    contents[x].style.display = "block";
    btns[x].classList.add("active");
}

openMain(2)