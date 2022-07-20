// A component which lists all student grades & feedback
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { APIService } from './api.service'; 

@Component({
    selector: 'student-results',
    styleUrls: ['./student-results.component.css'],
    templateUrl: "./student-results.component.html"
  })
  export class StudentResults {
      constructor(private APIService: APIService, private router: Router){}
       
      student_data_arr:any = [];
      
      // Hook that calls the resultsBuilder API, using the user's ID. The returned
      // data is then assigned to the student_data_arr array
      ngOnInit(){
        var builder = this.APIService.resultsBuilder(localStorage.getItem('u_id'));
        builder.subscribe((data:any) => {
            this.student_data_arr = Object.values(data);
           }); 
      }
  }