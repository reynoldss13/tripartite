import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { APIService } from '../api.service'; 

@Component({
  selector: 't1dashboard',
  templateUrl: './T1-dashboard.component.html',
  styleUrls: ['./T1.css'],
  template:""
})
export class Tenant1DashboardComponent {
    constructor(private APIService: APIService, private router: Router){}

        tenant:any;
        user:any;
        userType:any;
        fullName:any;

    ngOnInit(){
        if(localStorage.getItem("tenant_id") != "1"){
            this.router.navigate(["t2dashboard"])
        }
        this.fullName = localStorage.getItem('u_name');
        this.userType = localStorage.getItem('u_type');
        this.APIService.getTenant(localStorage.getItem('tenant_id')).subscribe((res:any) => {
        this.tenant = res["data"];
        });
        this.APIService.getUser(localStorage.getItem('u_id')).subscribe((res:any) => {
            this.user = res["data"];
        });
    }

    logout() {
        localStorage.clear();
        sessionStorage.removeItem('access_token');
        this.router.navigate(['login']);
    }

    studentViewToggle(a:HTMLElement, b:HTMLElement, c:HTMLElement, d:HTMLElement) {
        a.classList.toggle('hidden');
        b.classList.add('hidden');
        c.classList.add('hidden');
        d.classList.add('hidden');
    }

    teacherViewToggle(a:HTMLElement, b:HTMLElement, c:HTMLElement) {
        a.classList.toggle('hidden');
        b.classList.add('hidden');
        c.classList.add('hidden');
    }
}