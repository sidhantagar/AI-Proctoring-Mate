const PasswordToggle = document.querySelector(".Toggle");
const PasswordField1 = document.querySelector(".passwordInput1");
const PasswordField2 = document.querySelector(".passwordInput2");

const handleToggleInput=(e)=>{

  if(PasswordToggle.textContent === "SHOW"){
    PasswordToggle.textContent = "HIDE"
    PasswordField1.setAttribute("type", "text");
    PasswordField2.setAttribute("type", "text");
  }else{
    PasswordToggle.textContent = "SHOW"
    PasswordField1.setAttribute("type", "password");
    PasswordField2.setAttribute("type", "password");
  }

}

PasswordToggle.addEventListener('click',handleToggleInput);
