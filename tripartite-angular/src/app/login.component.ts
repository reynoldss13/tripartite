import { FormBuilder} from '@angular/forms';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { APIService } from './api.service'; 
import { Validators} from "@angular/forms";

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./app.component.css']
})
export class LoginComponent {
    // Initialise the login form
    loginForm: any

    constructor(
        private APIService: APIService,
          private router: Router,
           private formBuilder: FormBuilder){}

           ngOnInit() {
            // Validators for the login form:
            // emailInput is required and must be in format of valid email address
            // passwordInput is required and must be at least 8 characters long
            // login button is diabled until these conditions are met
            this.loginForm = this.formBuilder.group({
                emailInput: ['', Validators.compose([Validators.required,Validators.email])],
                passwordInput: ['', Validators.compose([Validators.minLength(8),Validators.required])],
            });
        }

    // onSubmit()
    // Function checks if the form has the required fields and prompts completion,
    // if the validators fail. Successful login will add the access key to session
    // storage and the additional claims to local storage
    onSubmit(){
        if(this.loginForm.pristine){
            alert("Please complete all fields")
        } else {
            var credentials = this.loginForm.value;
            var email = credentials.emailInput;
            var pw = credentials.passwordInput;
             this.APIService.login(email,pw).subscribe((res:any) => {
                 localStorage.setItem('tenant_id', res["data"]["tenant_id"]);
                 localStorage.setItem('tenant_name', res["data"]["tenant_name"]);
                 localStorage.setItem('u_id', res["data"]["_id"]);
                 localStorage.setItem('u_name', res["data"]["first_name"] + " " + res["data"]["surname"]);
                 localStorage.setItem('u_type', res["data"]["user_type"]);
                 sessionStorage.setItem('access_token', res['token']);
                 this.router.navigate(['dashboard']);   
             }, err => {
                 document.getElementById('error')?.classList.remove('hidden');

            });
        }
    }
}
