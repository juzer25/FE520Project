let loginForm = document.getElementById("loginForm")
let eDiv = document.getElementById("eDiv")
let pDiv = document.getElementById("pDiv")

if(loginForm){
    loginForm.onsubmit((e) => {
        e.preventDefault()

        eDiv.hidden = true
        pDiv.hidden = true

        let email= document.getElementsByName("email")[0];
        //console.log(email)
        let password= document.getElementsByName("password")[0];
        //console.log(password)
        //validating email
        if(email.value.trim()){
        //referred from https://www.w3docs.com/snippets/javascript/how-to-validate-an-e-mail-using-javascript.html
            const reg = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
            if(!reg.test(email.value.toLowerCase())){
                eDiv.hidden = false;
                eDiv.innerHTML = "Please enter a valid email.";
            //phrase.className = "errorText"; 
                loginForm.reset();
                email.focus();   
            }
        }
        else{
            eDiv.hidden = false;
            eDiv.innerHTML = "Please enter a valid email.";
            //phrase.className = "errorText"; 
            loginForm.reset();
            email.focus();
        }

        //validating password
        if(!password.value.trim()){
            pDiv.hidden = false;
            pDiv.innerHTML = "Password not valid";
            //phrase.className = "errorText"; 
            loginForm.reset();
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
        const pswreg = /^([a-zA-Z0-9-!$%^&*()_+|~=`{}\[\]:\/;<>?,.@#]{6,})*$/
        if(!pswreg.test(password.value)){
            pDiv.hidden = false;
            pDiv.innerHTML = "Password should have 6 or more characters";
            //phrase.className = "errorText"; 
            loginForm.reset();
            password.focus();
         
        }
    
    });
}