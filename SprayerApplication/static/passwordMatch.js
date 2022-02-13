// This works with signUp.html and login.html It ensures that passwords match before submiting 
//source codepen.io/diegoleme/pen/surlK

//on signUp submit fucntion is called to make sure password matches
function validatePassword(){
  var password = document.getElementById("password")
  , confirm_password = document.getElementById("confirm_password");
  if(password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Passwords Don't Match");
  } else {
    confirm_password.setCustomValidity('');
  }
  password.onchange = validatePassword();
confirm_password.onkeyup = validatePassword();
}
//After error message is displayed, clicking on username or password(on login form only) removes the errorMessage
function messageOff(){ 
  var message = document.getElementById('usernameMessage');
  var otherMessage = document.getElementById('errorMessage');
  message.style.display = 'none';
  otherMessage.style.display = 'none';
}