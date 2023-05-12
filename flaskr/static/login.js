//Reference - https://github.com/juzer25/CS_546_Group8_Project/blob/main/public/js/signup.js
let loginForm = document.getElementById("loginForm")
let eDiv = document.getElementById("eDiv")
let pDiv = document.getElementById("pDiv")

loginForm.addEventListener("submit", (event) =>{
        event.preventDefault()
        eDiv.hidden = true
        pDiv.hidden = true
        //getting the elements from the form
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
                return   
            }
        }
        else{
            eDiv.hidden = false;
            eDiv.innerHTML = "Please enter a valid email.";
            //phrase.className = "errorText"; 
            loginForm.reset();
            email.focus();
            return
        }

        //validating password
        if(!password.value.trim()){
            pDiv.hidden = false;
            pDiv.innerHTML = "Password not valid";
            //phrase.className = "errorText"; 
            loginForm.reset();
            password.focus();
            return
     
        }
        
        const pswreg = /^([a-zA-Z0-9-!$%^&*()_+|~=`{}\[\]:\/;<>?,.@#]{6,})*$/
        if(!pswreg.test(password.value)){
            pDiv.hidden = false;
            pDiv.innerHTML = "Password should have 6 or more characters";
            //phrase.className = "errorText"; 
            loginForm.reset();
            password.focus();
            return
        }
    
        loginForm.submit()
});