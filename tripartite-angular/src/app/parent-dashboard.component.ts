// A component that acts as the parental dashboard. Allowing them to view
// their children's grades and feedback, including any feedback from teachers
// intended for them
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { APIService } from './api.service'; 

@Component({
    selector: 'parent-dashboard',
    styleUrls: ['./parent-dashboard.component.css', './app.component.css'],
    templateUrl: "./parent-dashboard.component.html"
  })
  export class ParentDashboard {
      constructor(private APIService: APIService, private router: Router){}
       
      student_data_arr:any = [];
      
      // Hook that calls the dashboardBuilder API using the user ID. The returned
      // data is then stored in the student_data_arr array
      ngOnInit(){
         var builder = this.APIService.dashboardBuilder(localStorage.getItem('u_id'));
         builder.subscribe((data:any) => {
             this.student_data_arr = Object.values(data);
             console.log(this.student_data_arr);
            }); 
      }

      // Function used to show or hide a students grades
      toggleView(e: HTMLElement) {
        e.classList.toggle('hidden');
      }
  }