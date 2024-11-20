document.querySelector(".submit-conexion").disabled = true;

document.querySelector("#Email").onkeyup = () => {
    if (document.querySelector("#Email").value.length > 0) {
        document.querySelector(".submit-conexion").disabled = false;
    } else {
        document.querySelector(".submit-conexion").disabled = true;
    }
};


document.querySelector("#form-conexion").addEventListener("submit", function(event) {
    let Email = document.querySelector("#Email").value;
    let password = document.querySelector("#password").value
    console.log(Email);
    alert("votre avis a bien été envoyer")
    event.preventDefault();
});