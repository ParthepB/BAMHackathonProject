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
  const username = this.querySelector("input[placeholder='Username']").value.trim();
  const email = this.querySelector("input[placeholder='Email Address']").value.trim();
  const password = this.querySelector("input[placeholder='Password']").value;
  const confirmPassword = this.querySelector("input[placeholder='Confirm Password']").value;

  if (password !== confirmPassword) {
    alert("Passwords do not match!");
    return;
  }

  const users = JSON.parse(localStorage.getItem("users") || "{}");

  // Check for duplicate username or email
  for (let key in users) {
    if (users[key].username === username) {
      alert("Username already exists!");
      return;
    }
    if (users[key].email === email) {
      alert("Email already exists!");
      return;
    }
  }

  // Save user with username as key
  users[username] = { username, email, password };
  localStorage.setItem("users", JSON.stringify(users));
  localStorage.setItem("currentUser", username);
  window.location.href = "/templates/home.html";
});

// Handle Login
document.querySelector("form.login").addEventListener("submit", function (e) {
  e.preventDefault();
  const identifier = this.querySelector("input[placeholder='Email or Username']").value.trim();
  const password = this.querySelector("input[placeholder='Password']").value;

  const users = JSON.parse(localStorage.getItem("users") || "{}");
  let matchedUser = null;

  for (let key in users) {
    if (
      (users[key].username === identifier || users[key].email === identifier) &&
      users[key].password === password
    ) {
      matchedUser = users[key];
      break;
    }
  }

  if (matchedUser) {
    localStorage.setItem("currentUser", matchedUser.username);
    window.location.href = "/templates/home.html";
  } else {
    alert("Invalid email/username or password.");
  }
});

// Show username on home page if available
document.addEventListener("DOMContentLoaded", function () {
  const username = localStorage.getItem("currentUser");
  const display = document.getElementById("username-display");
  if (username && display) {
    display.textContent = username + ". ";
  }
});