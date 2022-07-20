// A component which lists a teacher's current classes
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { APIService } from './api.service'; 

@Component({
    selector: 'teacher-classes',
    styleUrls: ['./teacher-classes.component.css', './app.component.css'],
    templateUrl: "./teacher-classes.component.html"
  })
  export class TeacherClasses {
      constructor(private APIService: APIService, private router: Router){}
       
      class_data_arr:any = [];
      
      // Hook calls the getClassesByTeacher API
      ngOnInit(){
          var builder = this.APIService.getClassesByTeacher(localStorage.getItem('u_id'));
          builder.subscribe((data:any) => this.class_data_arr = Object.values(data),
          err =>{
              this.class_data_arr = [];
            });
        }
        // used to hide or reveal html elements
        toggleView(e: HTMLElement) {
            e.classList.toggle('hidden');
        }

        // redirects user to the edit-class components
        editClass(id:any) {
            localStorage.setItem('class_id',id);
            this.router.navigate(['edit-class']);

        }

        //redirects user to the new-class component
        addNewClass(){
            this.router.navigate(['new-class']);
        }
  }