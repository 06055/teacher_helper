document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("myModal");
    const openModalBtn = document.getElementById("openModal");
    const closeBtn = document.getElementsByClassName("close")[0];

openModalBtn.onclick = function() {
    modal.style.display = "block";
};

closeBtn.onclick = function() {
    modal.style.display = "none";
};

window.onclick = function(event) {
    if (event.target === modal) {
    modal.style.display = "none";
    }
};
});



window.onload = function() {
    openCustomModal();
};

function openCustomModal() {
    var modal = document.getElementById('customModal');
    modal.style.display = 'block';
}


function closeCustomModal() {
    var modal = document.getElementById('customModal');
    modal.style.display = 'none';
}





