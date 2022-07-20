// A component for updating an existing class.
// This includes changing the subject, day, period
// and students
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { APIService } from './api.service'; 
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';


@Component({
    selector: 'edit-class',
    styleUrls: ['./edit-class.component.css', './app.component.css'],
    templateUrl: "./edit-class.component.html"
  })
  export class EditClass {
      constructor(private APIService: APIService, private router: Router, private formBuilder: FormBuilder){}
       
      subject_arr:any = [];
      selected_subject:any;
      day_options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
      selected_day:any;
      class_data_arr:any = [];
      tenant_student_arr:any = [];
      classUpdateForm:any;
      
      // A hook that gets initialises the form with the class' details, obtains
      // a list of the tenant's students currently not listed in the class, and
      // instantiates the form
      ngOnInit(){
            this.APIService.getClass(localStorage.getItem('class_id')).subscribe(
                (data:any) => {
                    var current_selected_subject = localStorage.getItem('current_selected_subject');
                    var current_selected_day = localStorage.getItem('current_selected_day');
                    var data_arr = Object.values(data);

                    // set the day
                    if(current_selected_day == null){
                        this.selected_day = data_arr[1];
                    } else {
                        this.selected_day = current_selected_day
                    }
                    
                    // set the subject
                    if(current_selected_subject == null){
                        this.selected_subject = data_arr[4]
                    } else {
                        this.selected_subject = current_selected_subject
                    }

                    var class_data = {
                        '_id': data_arr[0],
                        'day': data_arr[1],
                        'period':data_arr[2],
                        'students':data_arr[3],
                        'subject':data_arr[4]
                    }
                    this.class_data_arr.push(class_data);
                },
                err => this.class_data_arr = []
            );
            this.APIService.getStudentList(localStorage.getItem('tenant_id')).subscribe(
                (data:any) => {
                    var dat:any = [];
                    dat = Object.values(data);
                    for(var index in dat){
                        if (!this.class_data_arr[0]['students'].find((x:any) => x['id'] == dat[index]['_id'])){
                            this.tenant_student_arr.push(dat[index]);
                        }
                    }
                },
                err => { this.tenant_student_arr = [];}
                );
            this.APIService.getSubjects().subscribe((data:any)=>{
                this.subject_arr = Object.values(data);
            }, err => {this.subject_arr = []; });

            this.classUpdateForm = this.formBuilder.group({
                subject:['', Validators.required],
                day:['', Validators.required],
                period:['', Validators.required]
            });
        }

        // Value change methods used to store a selected data to prevent reset when adding/removing students
        valueChangeSubject(val:any){
            localStorage.setItem('current_selected_subject', val.value);
        }

        valueChangeDay(val:any){
            localStorage.setItem('current_selected_day', val.value);
        }

        // Submits the edited class details
        completeEdit(subject:any, day:any, period:any) {
            if(parseInt(period) >= 1 && parseInt(period) <= 10){
                this.APIService.editClass(localStorage.getItem('class_id'), subject, day, parseInt(period)).subscribe(
                    response => {
                        localStorage.removeItem('class_id');
                        this.router.navigate(['dashboard']);
                    }, err => {
                        alert('Could not complete update. You have a class\nscheduled at this time.');
                    }
                );
            } else {
                alert('Invalid period selected! Please choose a number between 1 and 10');
            }
        }

        // Cancels the edit, returns the user to their dashboard, clears local storage
        cancelEdit(){
            localStorage.removeItem('class_id');
            localStorage.removeItem('current_selected_subject')
            localStorage.removeItem('current_selected_day')
            this.router.navigate(['dashboard']);
        }

        // Removes the student from the class, calls the initialisation to reset the arrays
        // and refreshes the page to update the view, the student will no longer be a member
        // of the class and will once again be listed in tenant student list
        removeStudent(id:any){
            this.APIService.removeStudentFromClass(localStorage.getItem('class_id'),id).subscribe(
                response => {
                    let currentUrl = this.router.url;
                    this.ngOnInit();
                    this.router.navigateByUrl('/', {skipLocationChange: true}).then(() => {
                        this.router.navigate([currentUrl]);
                    });
                }, err =>{alert(err);}
            );
        }

        // Adds a student to the class, calls the initialisation to reset the arrays
        // and refreshes the page to update the view, the student will  be a member
        // of the class and no longer listed in tenant student list 
        addStudent(id:any){
            this.APIService.addStudentToClass(localStorage.getItem('class_id'),id).subscribe(
                response => {
                    this.ngOnInit();
                    let currentUrl = this.router.url;
                    this.router.navigateByUrl('/', {skipLocationChange: true}).then(() => {
                        this.router.navigate([currentUrl]);
                    });
                }, err => {alert(err);}
            );
        }

        // Shows the delete confirmation modal
        deleteConfirm(modal:HTMLElement){
            modal.classList.toggle('hidden');
        }

        // Complete the deletion
        deleteClass(){
            this.APIService.deleteClass(localStorage.getItem('class_id')).subscribe(
                response => {
                    localStorage.removeItem('class_id')
                    this.router.navigate(['dashboard']);
                },
                err => alert(err)
                );
        }
  }