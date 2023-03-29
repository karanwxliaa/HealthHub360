function showSignup(){
    document.getElementById("signUp").style.display = "flex";
    document.getElementById("login").style.display = "none";
    document.getElementById("btns2").style.backgroundColor = "white";
    document.getElementById("btns1").style.backgroundColor = "#cdb4db";
}
function showLogin(){
    document.getElementById("signUp").style.display = "none";
    document.getElementById("login").style.display = "flex";
    document.getElementById("btns1").style.backgroundColor = "white";
    document.getElementById("btns2").style.backgroundColor = "#cdb4db";
}