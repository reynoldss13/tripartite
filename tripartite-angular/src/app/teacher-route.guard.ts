import { Injectable } from '@angular/core';
import { Router, CanActivate, } from '@angular/router';

// Protect routes from being accessed by an aunauthorised user
// Specificially, routes only intended for tenant faculty members
@Injectable()
export class TeacherGuard implements CanActivate {

    constructor(private router: Router) { }

    // If user type is 1, access is granted 
    canActivate() {
        if (Number(localStorage.getItem('u_type')) === 1) {
            return true;
        } else {
            this.router.navigate(['dashboard']);
            return false;
        }     
    }
}