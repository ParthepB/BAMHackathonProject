const loginText = document.querySelector(".title-text .login");
const loginForm = document.querySelector("form.login");
const loginBtn = document.querySelector("label.login");
const signupBtn = document.querySelector("label.signup");
const signupLink = document.querySelector("form .signup-link a");

signupBtn.onclick = () => {
  loginForm.style.marginLeft = "-50%";
  loginText.style.marginLeft = "-50%";
};

loginBtn.onclick = () => {
  loginForm.style.marginLeft = "0%";
  loginText.style.marginLeft = "0%";
};

signupLink.onclick = () => {
  signupBtn.click();
  return false;
};

// Handle Sign Up
document.querySelector("form.signup").addEventListener("submit", function (e) {
  e.preventDefault();
  const email = this.querySelector("input[placeholder='Email Address']").value;
  const password = this.querySelector("input[placeholder='Password']").value;
  const confirmPassword = this.querySelector("input[placeholder='Confirm Password']").value;

  if (password !== confirmPassword) {
    alert("Passwords do not match!");
    return;
  }

  const users = JSON.parse(localStorage.getItem("users") || "{}");
  if (users[email]) {
    alert("User already exists!");
    return;
  }

  users[email] = password;
  localStorage.setItem("users", JSON.stringify(users));
    window.location.href = "/templates/home.html";
});

// Handle Login
document.querySelector("form.login").addEventListener("submit", function (e) {
  e.preventDefault();
  const email = this.querySelector("input[placeholder='Email Address']").value;
  const password = this.querySelector("input[placeholder='Password']").value;

  const users = JSON.parse(localStorage.getItem("users") || "{}");

  if (users[email] && users[email] === password) {
    window.location.href = "/templates/home.html";
  } else {
    alert("Invalid email or password.");
  }
});