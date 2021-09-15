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
function changeList() {
    var sg=document.getElementById("events").value;
    
    if(sg=="Club_events"){
        document.getElementById("All_events").style.display="none";
        document.getElementById("Club_events").style.display="flex";
        document.getElementById("society").style.display="none";
        document.getElementById("other").style.display="none";
    }
    if(sg=="All_events"){
        document.getElementById("All_events").style.display="flex";
        document.getElementById("Club_events").style.display="none";
        document.getElementById("society").style.display="none";
        document.getElementById("other").style.display="none";
    }
    if(sg=="Society_events"){
        document.getElementById("All_events").style.display="none";
        document.getElementById("Club_events").style.display="none";
        document.getElementById("society").style.display="flex";
        document.getElementById("other").style.display="none";
    }
    if(sg=="Other_events"){
        document.getElementById("All_events").style.display="none";
        document.getElementById("Club_events").style.display="none";
        document.getElementById("society").style.display="none";
        document.getElementById("other").style.display="flex";
    }
    
}