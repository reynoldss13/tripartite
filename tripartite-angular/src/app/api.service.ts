// API Service component is used to call the Flask API
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable()
export class APIService {
    constructor(private http: HttpClient, private router: Router) {}

    login(email:any, pw:any){
        return this.http.post('http://localhost:5000/api/v1.0/login', null, {
            headers: new HttpHeaders({
                 'email':  email,
                 'password':pw
            })
        }).pipe();
    }

    getTenant(id:any){
        return this.http.get('http://localhost:5000/api/v1.0/tenant/'+id);
    }

    getUser(id:any){
        return this.http.get('http://localhost:5000/api/v1.0/user/'+id);
    }

    getStudentByStudentId(id:any){
        return this.http.get('http://localhost:5000/api/v1.0/student/'+id);
    }

    getStudentList(tenant_id:any){
        return this.http.get('http://localhost:5000/api/v1.0/students/'+tenant_id);
    }

    getSubjects(){
        return this.http.get('http://localhost:5000/api/v1.0/subjects');
    }

    getClass(class_id:any) {
        return this.http.get('http://localhost:5000/api/v1.0/class/'+class_id);
    }

    getClassesByStudent(student_id:any){
        return this.http.get('http://localhost:5000/api/v1.0/student_classes/' + student_id);
    }

    getClassesByTeacher(teacher_id:any){
        return this.http.get('http://localhost:5000/api/v1.0/teacher_classes/'+teacher_id);
    }

    getAssignment(assignment_id:any){
        return this.http.get('http://localhost:5000/api/v1.0/assignment/'+assignment_id);
    }

    getAssignmentsByClass(class_id:any){
        return this.http.get('http://localhost:5000/api/v1.0/assignment/'+class_id+'/find');
    }

    getAssignmentsByTeacher(teacher_id:any){
        return this.http.get('http://localhost:5000/api/v1.0/teacher_assignments/'+teacher_id);
    }

    getSubmission(student_id:any, assignment_id:any){
        return this.http.get('http://localhost:5000/api/v1.0/'+student_id+'/submission/'+assignment_id);
    }

    getAllSubmissions(assignment_id:any){
        return this.http.get('http://localhost:5000/api/v1.0/'+assignment_id+'/submissions');
    }

    createSubmission(assignment_id:any, student_id:any, file:File){
        let fd = new FormData();
        fd.append('file',file);
        return this.http.post('http://localhost:5000/api/v1.0/assignment/'+assignment_id+'/submission/'+student_id, fd);
    }

    createClass(teacher_id:any, subject:any, day:any, period:any, students:any){
        let fd = new FormData();
        fd.append('teacher_id', teacher_id);
        fd.append('subject', subject);
        fd.append('day', day);
        fd.append('period', period);
        fd.append('students', students);
        return this.http.post('http://localhost:5000/api/v1.0/class', fd);
    }

    createAssignment(teacher_id:any, class_id:any, title:any, deadline:any, file:File){
        let fd = new FormData();
        fd.append('title', title);
        fd.append('deadline', deadline);
        fd.append('file', file);
        return this.http.post('http://localhost:5000/api/v1.0/'+class_id+'/assignment/'+teacher_id+'/create', fd);
    }

    editClass(class_id:any, subject:any, day:any, period:any){
        let fd = new FormData();
        fd.append('subject', subject);
        fd.append('day', day);
        fd.append('period', period);
        return this.http.put('http://localhost:5000/api/v1.0/class/'+class_id, fd);
    }

    editAssignment(assignment_id:any, teacher_id:any, title:any, deadline:any, file:any){
        let fd = new FormData();
        if(file == "" || file == undefined){
            fd.append('title', title);
            fd.append('deadline', deadline);
            fd.append('teacher_id', teacher_id)
        } else {
            fd.append('title', title);
            fd.append('deadline', deadline);
            fd.append('file', file[0])
            fd.append('teacher_id', teacher_id)
        }
        return this.http.put('http://localhost:5000/api/v1.0/assignment/'+assignment_id, fd);
    }

    addStudentToClass(class_id:any, student_id:any){
        return this.http.put('http://localhost:5000/api/v1.0/class/'+class_id+'/add/'+student_id, null);
    }

    removeStudentFromClass(class_id:any, student_id:any){
        return this.http.put('http://localhost:5000/api/v1.0/class/'+class_id+'/remove/'+student_id, null);
    }

    deleteClass(class_id:any){
        return this.http.delete('http://localhost:5000/api/v1.0/class/'+class_id);
    }

    deleteAssignment(assignment_id:any){
        return this.http.delete('http://localhost:5000/api/v1.0/assignment/'+assignment_id);
    }

    addMarksAndFeedback(submission_id:any, mark:any, feedback:any, feedbackPrivate:any){
        let fd = new FormData();
        console.log('mark', mark)
        console.log('feedback', feedback)
        console.log('feedbackPrivate', feedbackPrivate)
        if(feedbackPrivate == null){
            fd.append('mark', mark);
            fd.append('feedback', feedback);
        } else {
            fd.append('mark', mark);
            fd.append('feedback', feedback);
            fd.append('feedback_private', feedbackPrivate);
        } 
        return this.http.put('http://localhost:5000/api/v1.0/submission/'+submission_id, fd);
    }
    
    dashboardBuilder(id:any) {
        return this.http.get('http://localhost:5000/api/v1.0/dashboard/'+id);
    }

    resultsBuilder(id:any) {
        return this.http.get('http://localhost:5000/api/v1.0/results/'+id);
    }

    studentAssignmentBuilder(id:any){
        return this.http.get('http://localhost:5000/api/v1.0/assignments/'+id);
    }

    teacherAssignmentBuilder(id:any){
        return this.http.get('http://localhost:5000/api/v1.0/teacher-assignments/'+id);
    }

    // Returns the URL for a file download that calls the flask 
    // download_assignment_file API
    downloadAssignmentFile(assignment_id:any){
        return 'http://localhost:5000/api/v1.0/assignment/'+assignment_id+'/download';
    }

    // Returns the URL for downloading all submissions for an assignment
    // calls the flask download_assignment_submissions API
    downloadAssignmentSubmissions(assignment_id:any){
        return 'http://localhost:5000/api/v1.0/assignment/'+assignment_id+'/submission_download';

    }
}