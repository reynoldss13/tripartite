// When a user is successfully authenticated, they are
// directed to this component which then checks the
// tenant's ID and forwards them to the the relevant
// dashboard

import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'dashboard',
  styleUrls: ['./app.component.css'],
  template:""
})
export class DashboardRoutingComponent {
    constructor(private router: Router,){}
     
    // Use of a switch statement for sorting. This can be expanded
    // as tenants are added to the app.
    ngOnInit(){
      var tenant_id:any = localStorage.getItem("tenant_id");
      switch(tenant_id){
          case "1":
              this.router.navigate(['t1dashboard']);
              break;
          case "2":
              this.router.navigate(['t2dashboard']);
              break;
          default:
              this.router.navigate(['login']);
              break;
      }
    }
}