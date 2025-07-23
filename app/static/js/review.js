
document.querySelector(".submit").disabled = true;

document.querySelector("#pseudo").onkeyup = () => {
    if (document.querySelector("#pseudo").value.length > 0) {
        document.querySelector(".submit").disabled = false;
    } else {
        document.querySelector(".submit").disabled = true;
    }
};

document.querySelector("#tex-area-review").onkeyup = () => {
    if (document.querySelector("#tex-area").value.length > 0) {
        document.querySelector(".submit").disabled = false;
   } else {
        document.querySelector(".submit").disabled = true;
   }
};

document.querySelector("#form-avis").addEventListener("submit", function(event) {
    let pseudo = document.querySelector("#pseudo").value;
    let avis = document.querySelector("#tex-area-avis").value;
    console.log(pseudo);
    console.log(avis);
    alert("votre avis a bien été envoyer")
    event.preventDefault();
});
