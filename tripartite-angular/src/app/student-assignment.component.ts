// Component for listing assignments with upcoming deadlines.
// Allows students to upload files with valid extensions
// (see: tripartite-flask/app.py: UPLOAD_EXTENSIONS)
import { Component } from '@angular/core';
import { APIService } from './api.service'; 
import { FormBuilder} from '@angular/forms';

@Component({
    selector: 'student-assignment',
    styleUrls: ['./student-assignment.component.css', './app.component.css'],
    templateUrl: "./student-assignment.component.html"
  })
  export class StudentAssignmnet {
      constructor(private APIService: APIService, private formBuilder: FormBuilder){}
       
      assignments_arr:any = []
      submissionForm:any;
      file:any;
      selected:boolean = false;

      // Hook where the studentAssignmentBuilder is called. The returned array
      // is assigned to the assignments_arr array and the submission form is instantiated
      ngOnInit(){
        var builder = this.APIService.studentAssignmentBuilder(localStorage.getItem('u_id'));
        builder.subscribe((data:any) => {
            this.assignments_arr = Object.values(data);
           }); 
        this.submissionForm = this.formBuilder.group({})
      }

      // Used to toggle the submit form for an assignment
      toggleSubmit(e: HTMLElement) {
        e.classList.toggle('hidden');
      }

      // Fired in the onChange of the file input. Adds the file
      // to the file variable and updates the selected boolean
      // so that the submit button can be used
      fileSelect(e:any){
        this.file = (e.target as HTMLInputElement).files || '';
        this.selected =true;
      }

      // Called when the new file is submitted.
      // The create submission API is called, passing the assignment & student ID's
      // along with the selected file. If a 200 response is returned, the form is cleared
      // and the selected variable is reset as false. Otherwise the user is alerted that the
      // file type is not acceptable.
      sendSubmission(form:any, assignmentId:any){
        this.APIService.createSubmission(assignmentId, localStorage.getItem('u_id'), this.file[0]).subscribe(
          res => {
            form.reset();
            this.selected = false;
            alert('Submission saved!')
          },
          err => alert("Invalid file type selected. Please try again."),
        );  
      }

      // Downloads the assignment file
      downloadAssignment(id:any){
        if(id != "" || null){
         let url = this.APIService.downloadAssignmentFile(id);
         window.open(url);
        }
      }
  }