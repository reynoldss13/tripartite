// A component to add a new class 
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { APIService } from './api.service'; 
import { FormBuilder, Validators } from '@angular/forms'; 


@Component({
    selector: 'new-class',
    styleUrls: ['./edit-class.component.css', './app.component.css'],
    templateUrl: "./new-class.component.html"
  })
  export class NewClass {
      constructor(private APIService: APIService, private router: Router, private formBuilder: FormBuilder){}
       
      subject_arr:any = [];
      day_options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
      tenant_student_arr:any = [];
      addClassForm:any;
      class_students:any = [];
      selected_day:any;
      selected_subject:any;
      
      // A hook that gets initialises the form for the class' details, obtains
      // a list of the tenant's students currently not listed in the class, and
      // fetches any students held in the class_students array
      ngOnInit(){   
        if(localStorage.getItem('students_arr') == '' || localStorage.getItem('students_arr') == null){
            this.class_students =[]
        } else {
            var students_arr:any = localStorage.getItem('students_arr')
            this.class_students = JSON.parse(students_arr);
        }

        this.APIService.getStudentList(localStorage.getItem('tenant_id')).subscribe(
            (data:any) => {
                var dat:any = [];
                dat = Object.values(data);
                for(var index in dat){
                    if (!this.class_students.find((x:any) => x['id'] == dat[index]['_id'])){
                        this.tenant_student_arr.push(dat[index]);
                    }
                }
            },
            err => { this.tenant_student_arr = [];}
            );
         
        // Get subjects and set selected subject    
        this.APIService.getSubjects().subscribe((data:any)=>{
            this.subject_arr = Object.values(data);
            var current_selected_subject = localStorage.getItem('current_selected_subject');
            console.log(current_selected_subject)
            if(current_selected_subject == null) {
                this.selected_subject = this.subject_arr[0];
            } else {
                this.selected_subject = current_selected_subject;
            }
        }, err => {this.subject_arr = []; });

        // set day if previously selected before refresh
        var current_selected_day = localStorage.getItem('current_selected_day');
        if(current_selected_day == null){
            this.selected_day = this.subject_arr[0];
        } else {
            this.selected_day = current_selected_day;
        }

        this.addClassForm = this.formBuilder.group({
            subject:['', Validators.required],
            day:['', Validators.required],
            period:['', Validators.required]
        });
        }

        // Returns the user to their dashboard without saving
        cancelAdd(){
            localStorage.removeItem('current_selected_subject');
            localStorage.removeItem('current_selected_day');
            localStorage.removeItem('students_arr');
            this.router.navigate(['dashboard']);
        }

        // Saves a new class, fetches the teacher_id & students currently added to the the array
        // and calls the createClass API with the required parameters. If successful, the
        // user is notified of the success, they temp student array is removed from storage
        // and the user is redirected back to their dashboard. Otherwise, the user is notified
        // of the scheduling conflict, the class is not saved until the user chooses a free time slot
        saveClass(subject:any, day:any, period:any) {
            var students_arr:any = localStorage.getItem('students_arr');
            var teacher_id = localStorage.getItem('u_id');
            if(parseInt(period) >= 1 && parseInt(period) <= 10){
                this.APIService.createClass(teacher_id, subject, day, period, students_arr).subscribe(
                    response => {
                        alert('Class successfully saved')
                        localStorage.removeItem('students_arr');
                        this.router.navigate(['dashboard']);
                    },
                    err => {alert('Could not save class. You have a class\nscheduled at this time.')}
                );
            } else {
                alert('Invalid period selected! Please choose a number between 1 and 10');
            }

        }

        // Removes the student from the class, calls the initialisation to reset the arrays
        // and refreshes the page to update the view, the student will no longer be a member
        // of the class and will once again be listed in tenant student list
        removeStudent(id:any){
            var students_arr:any = localStorage.getItem('students_arr');
            this.class_students = JSON.parse(students_arr);
            var index = this.class_students.findIndex((student:any) => student['id'] === id);
            this.class_students.splice(index, index >= 0? 1 : 0); 
            localStorage.setItem('students_arr', JSON.stringify(this.class_students));
            let currentUrl = this.router.url;
            this.ngOnInit();
                   this.router.navigateByUrl('/', {skipLocationChange: true}).then(() => {
                       this.router.navigate([currentUrl]);
                    });
        }

        // Adds a student to the class, calls the initialisation to reset the arrays
        // and refreshes the page to update the view, the student will  be a member
        // of the class and no longer listed in tenant student list 
        addStudent(id:any, year_group:any, first_name:any, surname:any){
            var student = {
                'id': id,
                'year_group': parseInt(year_group),
                'name': first_name + " " + surname
            }
            this.class_students.push(student);
            localStorage.setItem('students_arr', JSON.stringify(this.class_students));
            let currentUrl = this.router.url;
            this.ngOnInit();
            this.router.navigateByUrl('/', {skipLocationChange: true}).then(() => {
                this.router.navigate([currentUrl]);
            });
        }

        // Value change methods used to store a selected data to prevent reset when adding/removing students
        valueChangeSubject(val:any){
            console.log(val.value)
            localStorage.setItem('current_selected_subject', val.value);
        }

        valueChangeDay(val:any){
            console.log(val.value)
            localStorage.setItem('current_selected_day', val.value);
        }
  }