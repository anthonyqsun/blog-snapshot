function redirect(x) {
    window.location.href = x;
}

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    let mybutton = document.getElementById("up");
    if (document.body.scrollTop > 1000 || document.documentElement.scrollTop > 1000) {
      mybutton.style.display = "flex";
    } else {
      mybutton.style.display = "none";
    }
  }

function topFunction() {
    document.body.scrollTop = 0; // Safari
    document.documentElement.scrollTop = 0; // Chrome, Firefox, IE and Opera
  }