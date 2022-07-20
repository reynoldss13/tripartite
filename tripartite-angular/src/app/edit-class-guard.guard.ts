import { Injectable } from '@angular/core';
import { Router, CanActivate, } from '@angular/router';

// Used to prevent access to the edit class form if
// a specific class_id is not held in memory
@Injectable()
export class EditGuard implements CanActivate {

    constructor(private router: Router) { }

    // If class_id is found, access is granted
    canActivate() {
        // IF the class_id is null or undefined, the user will be redirected to the dashboard
        if (localStorage.getItem('class_id') === null || localStorage.getItem('class_id') === undefined) {
            this.router.navigate(['dashboard']);
            return false;
        } else {
            return true;
        }     
    }
}