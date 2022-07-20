// A component to add/edit marks and feedback to work
// submited by students
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { APIService } from './api.service'; 
import { FormBuilder, Validators } from '@angular/forms'; 


@Component({
    selector: 'marks-feedback',
    styleUrls: ['./marks-feedback.component.css', './app.component.css'],
    templateUrl: "./marks-feedback.component.html"
  })
  export class MarksFeedback {
      constructor(private APIService: APIService, private router: Router, private formBuilder: FormBuilder){

      }
       
    current_assignment_title:any;
    current_assignment_id:any;
    assignment_submissions:any;
    students_no_submission:any = [];

    // Calls all data for the current assignment & the related submissions
    ngOnInit(){
        var a_id = localStorage.getItem('assignment_id');
        this.APIService.getAssignment(a_id).subscribe(
            response => {
                var data = Object.values(response);
                this.current_assignment_title = data[0]['title'];
                this.current_assignment_id = data[0]['_id']
            },
            err => {
                console.log(err);
            }
        );

        this.APIService.getAllSubmissions(a_id).subscribe(
            response => {
                var data = Object.values(response);
                this.assignment_submissions = data;
                localStorage.setItem('submissions', JSON.stringify(data))

            },
            err => {
                console.log(err)
            }
        );

        var c_id = localStorage.getItem('class_id');
        this.APIService.getClass(c_id).subscribe((response:any) => {
            var submissions:any = localStorage.getItem('submissions')
            var sub_arr = JSON.parse(submissions);

            console.log("submissions",sub_arr)
            var data = response['students'];
            var stud_arr = [];

            for(var index in data){
                if (!sub_arr.find((x:any) => x['student_id'] == data[index]['id'])){
                    stud_arr.push(data[index]);
                }
            }
            console.log("no submissions",stud_arr)
            this.students_no_submission = stud_arr
        })
    }

    // Returns the user to their dashboard
    return(){
        localStorage.removeItem('assignment_id');
        localStorage.removeItem('class_id');
        localStorage.removeItem('submissions')
        this.router.navigate(['dashboard']);
    }

    // Calls the addMarksAnd Feedback API, providing the assignment ID,
    // mark and feedback. If no parent feedback is provided, it is
    // set as null in the API call.
    addFeedback(id:any, mark:any, feedback:any, parent_feedback:any){
        if(parent_feedback ==""){
            this.APIService.addMarksAndFeedback(id, mark, feedback, null).subscribe(
                response => {
                    console.log(response)
                    let currentUrl = this.router.url;
                    this.ngOnInit();
                    this.router.navigateByUrl('/', {skipLocationChange: true}).then(() => {
                        this.router.navigate([currentUrl]);
                    });
                },
                err => { console.log(err) }
            );
        } else {
            this.APIService.addMarksAndFeedback(id, mark, feedback, parent_feedback).subscribe(
                response => {
                    console.log(response)
                    let currentUrl = this.router.url;
                    this.ngOnInit();
                    this.router.navigateByUrl('/', {skipLocationChange: true}).then(() => {
                        this.router.navigate([currentUrl]);
                    });
                },
                err => { console.log(err) }
            );
        }
    }
  }