import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { APIService } from './api.service'; 

@Component({
    selector: 'student-classes',
    styleUrls: ['./student-classes.component.css'],
    templateUrl: "./student-classes.component.html"
  })
  export class StudentClasses {
      constructor(private APIService: APIService, private router: Router){}
       
      student_classes:any = [];
      student_name:any;
      
      // Hook that calls the resultsBuilder API, using the user's ID. The returned
      // data is then assigned to the student_data_arr array
      ngOnInit(){
        var builder = this.APIService.getClassesByStudent(localStorage.getItem('u_id'));
        builder.subscribe((data:any) => {
            this.student_classes = Object.values(data);
           }); 
        this.student_name = localStorage.getItem('u_name');
      }
  }