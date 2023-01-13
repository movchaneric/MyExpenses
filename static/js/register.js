console.log('register.js is working')

// get username field by id
const userNameField = document.getElementById('usernameField')
const invalidUserField = document.getElementById('invalidNameField')
const emailField = document.getElementById('emailField')
const invalidEmailField = document.getElementById('invalidEmail')

const userUrl = "http://127.0.0.1:8000/authentication/user-validate/"
const emailUrl = "http://127.0.0.1:8000/authentication/email-validate/"




emailField.addEventListener('keyup', (event) => {
	const emailVal = event.currentTarget.value;

	if(emailVal.length > 0){
		fetch(emailUrl, {
			method:"POST",
			body: JSON.stringify({email: emailVal})
		})

		.then((res) => {
			return res.json();
		})

		.then((data) => {
    		console.log('email success:', data);
    		if(data.email_error){
    			emailField.classList.add('is-invalid')

    			// show message on screen
    			invalidEmail3Field.innerHTMl = '<p>${data.email_error}</p>'
    			invalidEmailField.style.display = "block"
    		}else{
    			emailField.classList.remove('is-invalid')
    			invalidEmailField.style.display = "none"
    		}
  		})
	}
})



// Add eventlistener when user is typing USERNAME
userNameField.addEventListener('keyup', (event) => {
	// get user typing data
	const userNameVal = event.currentTarget.value;

	// fetch call
	if (userNameVal.length > 0) {
		fetch(userUrl, {
			method: "POST",
			body: JSON.stringify({username: userNameVal}),
		})

		.then((res) => {
			return res.json();
		})

		.then((data) => {
    		console.log('user success:', data);
    		if(data.username_error){
    			userNameField.classList.add('is-invalid')
    			// show message on screen
    			invalidUserField.style.display = "block"
    			invalidUserField.innerHTML = '<p>${data.username_error}</p>'
    		}else{
    			userNameField.classList.remove('is-invalid')
    			// show message on screen
    			invalidUserField.style.display = "none"
    		}
  		})
	}
})