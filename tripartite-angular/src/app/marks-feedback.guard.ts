import { Injectable } from '@angular/core';
import { Router, CanActivate, } from '@angular/router';

// Used to prevent access to the marks and feedback form if
// an assignment_id is not held in memory
@Injectable()
export class MarkAndFeedbackGuard implements CanActivate {

    constructor(private router: Router) { }

    // If assignment_id is found, access is granted
    canActivate() {
        // IF the assignment_id is null or undefined, the user will be redirected to the dashboard
        if (localStorage.getItem('assignment_id') === null || localStorage.getItem('assignment_id') === undefined) {
            this.router.navigate(['dashboard']);
            return false;
        } else {
            return true;
        }     
    }
}