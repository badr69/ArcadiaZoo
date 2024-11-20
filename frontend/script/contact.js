
document.querySelector(".submit-contact").disabled = true;

document.querySelector("#Email").onkeyup = () => {
    if (document.querySelector("#Email").value.length > 0) {
        document.querySelector(".submit-contact").disabled = false;
    } else {
        document.querySelector(".submit-contact").disabled = true;
    }
};

document.querySelector("#tex-area-contact").onkeyup = () => {
    if (document.querySelector("#tex-area-contact").value.length > 0) {
        document.querySelector(".submit-contact").disabled = false;
   } else {
        document.querySelector(".submit-contact").disabled = true;
   }
};

document.querySelector("#form-contact").addEventListener("submit", function(event) {
    let Email = document.querySelector("#Email").value;
    let titre = document.querySelector("#titre").value;
    let description = document.querySelector("#tex-area-contact").value;
    console.log(Email);
    console.log(titre);
    console.log(description)

    alert("votre avis a bien été envoyer")
    event.preventDefault();
});
