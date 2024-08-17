function validateForm() {
    let name = document.signupForm.name.value
    let email = document.signupForm.email.value
    let password = document.signupForm.password.value
  
    // Add your validation criteria here
    let nameRegex = /^[a-zA-Z]+( [a-zA-Z]+)*$/
    let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    let passwordRegex = /^(?=.*[a-zA-Z\d])[a-zA-Z\d!@#$%^&*()]{6,}$/
  
    if (!nameRegex.test(name)) {
      element=document.getElementById('validationError')
      element.innerHTML = 'Name must be in alphabets'
      element.classList.remove('none')
      return false
    } 
    else {
      document.getElementById('validationError').innerHTML = ''
    }
  
    if (!emailRegex.test(email)) {
      element=document.getElementById('validationError')
      element.innerHTML = "Email is't valid"
      element.classList.remove('none')
      return false
    } else {
      document.getElementById('validationError').innerHTML = ''
    }
  
    if (!passwordRegex.test(password)) {
      
      element=document.getElementById('validationError')
      element.innerHTML = 'Create Stronge Password'
      element.classList.remove('none')
      
      return false
    } else {
      document.getElementById('validationError').innerHTML = ''
    }
  
    return true // Submit the form if all validations pass
  }
  
  document.signupForm.addEventListener('submit', function (event) {
    if (!validateForm()) {
      event.preventDefault() // Prevent form submission if validations fail
    }
  })
