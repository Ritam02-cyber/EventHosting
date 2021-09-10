window.addEventListener('scroll', function () {
    let header = document.querySelector('nav');
    let windowposition = window.scrollY > 300;
    header.classList.toggle('scroll-active', windowposition);
})

function w3_open() {
    document.getElementById("mySidebar").style.width = "55vw";
   

}
function w3_close() {
    document.getElementById("mySidebar").style.width = "0vw";
}