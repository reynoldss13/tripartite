// Component for Teachers: listing and creating assignments.
// Also allows teachers to download submissions for an assignment.
// Allows routing to add marks/feedback form
import { Component } from '@angular/core';
import { APIService } from './api.service'; 
import { FormBuilder, Validators } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { Router } from '@angular/router';

@Component({
    selector: 'teacher-assignment',
    styleUrls: ['./teacher-assignment.component.css', './app.component.css'],
    templateUrl: "./teacher-assignment.component.html"
  })
  export class TeacherAssignment {
    constructor(private APIService: APIService, private formBuilder: FormBuilder,
         private datePipe: DatePipe, private router: Router){
        // Constructor initialises the date_today & minimum date (for deadlines) with the date pipe
        // for use with the validation and form date input
        const dateFormat = 'yyyy-MM-dd';
        this.date_today = datePipe.transform(
            new Date().setDate(new Date().getDate()), dateFormat
        );
        this.minimum_date = datePipe.transform(
            new Date().setDate(new Date().getDate() +1), dateFormat
        );
        this.selected_deadline = this.minimum_date;
    }
    
    minimum_date:any;
    date_today:any;
    selected_deadline:any;
    assignments_arr:any = [];
    addAssignmentForm:any;
    editAssignmentForm:any
    assignment_file:any;
    current_class_subject:any;
    current_class_day:any;
    current_class_period:any;
    current_class_id:any;
    current_assignment_id:any;
    current_assignment_title:any;
    current_assignment_deadline:any;
    current_assignment_filename:any;

    // Hook that calls the teacher assignment builder API, assigning its values to the 
    // assignments_arr array. Also initialises the form for adding assignments and 
    // validators
    ngOnInit(){
        this.APIService.teacherAssignmentBuilder(localStorage.getItem('u_id')).subscribe(
            (data:any) => {
                this.assignments_arr = Object.values(data);
            },
            err => console.log(err)
        );

        this.addAssignmentForm = this.formBuilder.group({
            title:['', Validators.compose([Validators.minLength(5), Validators.required])],
            deadline:[this.minimum_date, Validators.required],
            upload:['', Validators.required]
        });

        this.editAssignmentForm = this.formBuilder.group({
            editTitle:['', Validators.minLength(5)],
            editDeadline:[this.minimum_date],
            editUpload:['']
        });
    }

    // Method for comparing dates. If the deadline has passed, this is used to determine
    // if a teacher can edit the class or download submissions and continue to add marks
    // and feedback
    dateCompare(assignment_deadline:any){
        var deadline = Date.parse(assignment_deadline);
        var today= Date.parse(this.date_today);
        return deadline < today;
    }

    // Used for getting and validating the selected deadline date. Assigns
    // the date to the variable, selected_deadline. Then checks this is
    // greater than, or equal to, the minimmum date. Returns boolean.
    dateSelection() {
        this.selected_deadline = this.addAssignmentForm.get('deadline').value;
        return Date.parse(this.selected_deadline) >= Date.parse(this.minimum_date)
    }

    // When a file is selcected, it is added to the assignment_file variable
    fileSelect(e:any){
        this.assignment_file = (e.target as HTMLInputElement).files || '';
    }

       // Used to toggle the list of assignments for a class
    toggle(e: HTMLElement) {
        e.classList.toggle('hidden');
    }

    // Calls the createAssignment API to save the new assignment, then calls ngOnInit to refresh the component
    saveAssignment(e:HTMLElement ,title:any) {
        this.APIService.createAssignment(localStorage.getItem('u_id'),
         this.current_class_id, title, this.selected_deadline, this.assignment_file[0]).subscribe(
            response => {
                alert('Assignment saved successfully!');
                this.assignment_file = "";
                this.ngOnInit();
                document.getElementById('add_422_error')?.classList.add('hidden');
                document.getElementById('add_name_error')?.classList.add('hidden');
                e.classList.toggle('hidden');
            }, 
            err => {
                if(err.status == 422){
                    document.getElementById('add_422_error')?.classList.remove('hidden');
                } else {
                    document.getElementById('add_name_error')?.classList.remove('hidden');
                }
            }
        );
    }

    // Opens the add assignment modal window, assigns the details
    // of the current class to the variables.
    InitiateSave(e: HTMLElement, class_id:any, subject:any, day:any, period:any) {
        e.classList.toggle('hidden');
        this.current_class_day = day;
        this.current_class_subject = subject;
        this.current_class_period = period;
        this.current_class_id = class_id;
    }

    // Closes the modal window, resetting the values of the forms
    cancelSave(e: HTMLElement) {
        e.classList.toggle('hidden');
        this.addAssignmentForm.get('title').setValue("");
        this.addAssignmentForm.get("upload").setValue("");
        document.getElementById('add_422_error')?.classList.add('hidden');
        document.getElementById('add_name_error')?.classList.add('hidden');
    }

    // Calls the download submissions API, retrieves all submissions (if any)
    // for the assignment as a zip file
    downloadSubmissions(id:any){
        if(id != "" || null){
            let url = this.APIService.downloadAssignmentSubmissions(id);
            window.open(url);
        }
    }

    // Initiates the edit function by opening the edit assignment modal
    // with the values of the current assignment.
    InitiateEdit(e:HTMLElement, assignment_id:any, assignment_title:any, assignment_deadline:any, assignment_filename:any) {
        e.classList.toggle('hidden');
        this.current_assignment_title = assignment_title;
        this.current_assignment_id = assignment_id;
        this.current_assignment_deadline = assignment_deadline;
        this.current_assignment_filename = assignment_filename;
    }

    // Completes the edit of the assignment by calling the edit assignment API.
    // If successful, the component is reloaded and a message is displayed to inform
    // the user.  If the user attempts to upload an unsupported file type, and error
    // will be thrown and the update will not complete
    completeEdit(e:HTMLElement, title:any, deadline:any) {
        this.APIService.editAssignment(
            this.current_assignment_id,localStorage.getItem('u_id'),
            title, deadline, this.assignment_file
            ).subscribe(response => {
                this.ngOnInit();
                document.getElementById('edit_422_error')?.classList.add('hidden');
                document.getElementById('edit_name_error')?.classList.add('hidden');
                e.classList.toggle('hidden');
                alert('Assignment updated successfully')
            }, err => {
                if(err.status == 422){
                    document.getElementById('edit_422_error')?.classList.remove('hidden');
                } else {
                    document.getElementById('edit_name_error')?.classList.remove('hidden');
                }
            });
    }

    // Closes the edit modal window, resetting the value of the file input
    // and clearing the assignment_file variable
    cancelEdit(e: HTMLElement) {
        e.classList.toggle('hidden');
        document.getElementById('add_422_error')?.classList.add('hidden');
        document.getElementById('add_name_error')?.classList.add('hidden');
        this.editAssignmentForm.get("editUpload").setValue("");
        this.assignment_file ="";
    }

    // Deletes the assignment by calling the delete assignment API.
    // If successful, it resets the current assignment variables,
    // refreshes the component and hides the modal
    deleteAssignment(e:HTMLElement, assignment_id:any) {
        this.APIService.deleteAssignment(assignment_id).subscribe(
            response => {
                this.current_assignment_title = '';
                this.current_assignment_id = '';
                this.current_assignment_deadline = '';
                this.current_assignment_filename = '';
                this.ngOnInit();
                e.classList.toggle('hidden');
            },
            err => console.log(err)
        );
    }

    // Redirects user to the MarksFeedback component
    marksFeedbackRedirect(assignment_id:any, class_id:any){
        localStorage.setItem('assignment_id', assignment_id);
        localStorage.setItem('class_id', class_id)
        this.router.navigate(['marks-feedback']);
    }
}