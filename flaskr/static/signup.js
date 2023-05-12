//Reference - https://github.com/juzer25/CS_546_Group8_Project/blob/main/public/js/signup.js
let myForm = document.getElementById('myForm');
let firstDiv = document.getElementById('firstError');
let lastDiv = document.getElementById('lastError')
let emailDiv = document.getElementById('emailError');
let pswdDiv = document.getElementById('pswdError');

myForm.addEventListener('submit',(event)=>{
    event.preventDefault()
    //alert("This is bein called")
    firstDiv.hidden = true
    lastDiv.hidden = true
    emailDiv.hidden = true
    pswdDiv.hidden = true
    //getting the elements from the form
    let firstName = document.getElementsByName("firstName")[0];
    let lastName = document.getElementsByName("lastName")[0];
    console.log(lastName)
    let email= document.getElementsByName("email")[0];
    console.log(email)
    let password= document.getElementsByName("password")[0];
    //console.log(password)
    //validating name
    if(!firstName.value){
        firstDiv.hidden = false;
        firstDiv.innerHTML = "Please enter a value.";
        //phrase.className = "errorText"; 
        myForm.reset();
        firstName.focus();
        //return false
        return
    }
    if(!firstName.value.trim()){
        firstDiv.hidden = false;
        firstDiv.innerHTML = "Please enter a String value.";
        //phrase.className = "errorText"; 
        myForm.reset();
        firstName.focus();
        //return false
        return
    }

    fnameReg = /^[A-Za-z]+[A-Za-z]{2,}$/
    if(!fnameReg.test(firstName.value)){
        firstDiv.hidden = false;
        firstDiv.innerHTML = "Please enter a valid value.";
        //phrase.className = "errorText"; 
        myForm.reset();
        firstName.focus();
        //return false
        return
    }
    if(!lastName.value){
        lastDiv.hidden = false;
        lastDiv.innerHTML = "Please enter a value.";
        //phrase.className = "errorText"; 
        myForm.reset();
        lastName.focus();
        //return false
        return
    }

    if(!lastName.value.trim()){
        lastDiv.hidden = false;
        lastDiv.innerHTML = "Please enter a String value.";
        //phrase.className = "errorText"; 
        myForm.reset();
        lastName.focus();
        //return false
        return
    }

    lnameReg = /^[A-Za-z]+[A-Za-z]{2,}$/
    if(!lnameReg.test(lastName.value)){
        lastDiv.hidden = false;
        lastDiv.innerHTML = "Please enter a valid value.";
        //phrase.className = "errorText"; 
        myForm.reset();
        lastName.focus();
        //return false
        return
    }


    //validating email
    if(!email.value){
        emailDiv.hidden = false;
        emailDiv.innerHTML = "Please enter a valid email.";
        //phrase.className = "errorText"; 
        myForm.reset();
        email.focus(); 
        //return false
        return
    }
    if(email.value.trim()){
        //referred from https://www.w3docs.com/snippets/javascript/how-to-validate-an-e-mail-using-javascript.html
        const reg = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        if(!reg.test(email.value.toLowerCase())){
            emailDiv.hidden = false;
            emailDiv.innerHTML = "Please enter a valid email.";
            //phrase.className = "errorText"; 
            myForm.reset();
            email.focus();
            //return false 
            return
        }
    }
    else{
        emailDiv.hidden = false;
        emailDiv.innerHTML = "Please enter a valid email.";
        //phrase.className = "errorText"; 
        myForm.reset();
        email.focus();
        //return false
        return
    }

    //validating password
    if(!password.value){
        pswdDiv.hidden = false;
        pswdDiv.innerHTML = "Please provide a password";
        //phrase.className = "errorText"; 
        myForm.reset();
        password.focus();
        //return false
        return
    }

    if(!password.value.trim()){
        pswdDiv.hidden = false;
        pswdDiv.innerHTML = "Password not valid";
        //phrase.className = "errorText"; 
        myForm.reset();
        password.focus();
        return
 
    }
    
    const pswreg = /^([a-zA-Z0-9-!$%^&*()_+|~=`{}\[\]:\/;<>?,.@#]{6,})*$/
    if(!pswreg.test(password.value)){
        pswdDiv.hidden = false;
        pswdDiv.innerHTML = "Password should have 6 or more characters";
        //phrase.className = "errorText"; 
        myForm.reset();
        password.focus();
        return
    }
    myForm.submit()
});
