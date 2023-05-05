
let myForm = document.getElementById('myForm');
let nameDiv = document.getElementById('nameError');
let emailDiv = document.getElementById('emailError');
let pswdDiv = document.getElementById('pswdError');


if(myForm){

myForm.onsubmit((e) =>{

    e.preventDefault()
    
    nameDiv.hidden = true
    emailDiv.hidden = true
    pswdDiv.hidden = true
    let name = document.getElementsByName("name")[0];
    //console.log(name)
    let email= document.getElementsByName("email")[0];
    //console.log(email)
    let password= document.getElementsByName("password")[0];
    //console.log(password)
    //validating name
    if(!name.value.trim()){
        nameDiv.hidden = false;
        nameDiv.innerHTML = "Please enter a String value.";
        //phrase.className = "errorText"; 
        myForm.reset();
        name.focus();

    }
    //validating email
    if(email.value.trim()){
        //referred from https://www.w3docs.com/snippets/javascript/how-to-validate-an-e-mail-using-javascript.html
        const reg = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
        if(!reg.test(email.value.toLowerCase())){
            emailDiv.hidden = false;
            emailDiv.innerHTML = "Please enter a valid email.";
            //phrase.className = "errorText"; 
            myForm.reset();
            email.focus(); 
     
        }
    }
    else{
        emailDiv.hidden = false;
        emailDiv.innerHTML = "Please enter a valid email.";
        //phrase.className = "errorText"; 
        myForm.reset();
        email.focus();

    }

    //validating password
    if(!password.value.trim()){
        pswdDiv.hidden = false;
        pswdDiv.innerHTML = "Password not valid";
        //phrase.className = "errorText"; 
        myForm.reset();
        password.focus();
 
    }
    /*if(password.value.length < 6){
        pswdDiv.hidden = false;
        pswdDiv.innerHTML = "Password should have 6 or more characters";
        //phrase.className = "errorText"; 
        myForm.reset();
        password.focus();
        return
    }*/
    const pswreg = /[A-Za-z]\w{6,}/ 
    if(!pswreg.test(password.value)){
        pswdDiv.hidden = false;
        pswdDiv.innerHTML = "Password should have 6 or more characters";
        //phrase.className = "errorText"; 
        myForm.reset();
        password.focus();
     
    }

})
}