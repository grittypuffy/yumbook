/* Validates form input */

const email = document.getElementById("mail");

email.addEventListener("input", (event) => {
  if (email.validity.typeMismatch) {
	email.setCustomValidity("Please enter a valid e-mail address");
  } else {
	email.setCustomValidity("");
  }
});
