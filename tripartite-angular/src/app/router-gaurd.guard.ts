import { Injectable } from '@angular/core';
import { Router, CanActivate, } from '@angular/router';

// Protect routes from being accessed by an aunauthorised user
@Injectable()
export class RouteGuard implements CanActivate {

    constructor(private router: Router) { }

    // If access token is present, authorisation is granted
    // otherwise the user is routed to login 
    canActivate() {
        if (sessionStorage.getItem('access_token')) {
            return true;
        } else {
            this.router.navigate(['login']);
            return false;
        }     
    }
}