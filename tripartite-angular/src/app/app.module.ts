import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { APIService } from './api.service';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
import { LoginComponent } from './login.component';
import { DashboardRoutingComponent } from './dashboard-router.component';
import { JwtHelperService, JWT_OPTIONS } from '@auth0/angular-jwt';
import { RouteGuard } from './router-gaurd.guard';
import { TeacherGuard } from './teacher-route.guard';
import { Tenant1DashboardComponent } from './tenant_one/T1-dashboard.component';
import { Tenant2DashboardComponent } from './tenant_two/T2-dashboard.component';
import { AvatarModule } from 'ngx-avatar'; 
import { ParentDashboard } from './parent-dashboard.component';
import { StudentResults } from './student-results.component';
import { StudentAssignmnet } from './student-assignment.component';
import { ObjTForm } from './object-pipe.pipe';
import { TeacherClasses } from './teacher-classes.component';
import { EditClass } from './edit-class.component';
import { EditGuard } from './edit-class-guard.guard';
import { ObjSortPipe } from './object-sort-pipe';
import { NewClass } from './new-class.component';
import { StudentClasses } from './student-classes.component';
import { TeacherAssignment } from './teacher-assignment.component';
import { DatePipe } from '@angular/common';
import { MarksFeedback } from './marks-feedback.component';
import { MarkAndFeedbackGuard } from './marks-feedback.guard';

// Routes, all protected by RouteGuard component. Will redirect to
// login if user has not been authenticated.
// The edit/new class routes will also redirect back to the dashboard
// if the user is not a teacher. Additionally, the edit class form
// will redirect back to the dashboard if a valid class ID has not been
// passed to it during redirect
var routes: any = [
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardRoutingComponent, canActivate: [RouteGuard] },
  { path: 'edit-class', component: EditClass, canActivate: [RouteGuard, TeacherGuard, EditGuard] },
  { path: 'new-class', component: NewClass, canActivate: [RouteGuard, TeacherGuard] },
  { path: 't1dashboard', component: Tenant1DashboardComponent, canActivate: [RouteGuard] },
  { path: 't2dashboard', component: Tenant2DashboardComponent, canActivate: [RouteGuard] },
  { path: 'marks-feedback', component: MarksFeedback, canActivate: [RouteGuard, TeacherGuard, MarkAndFeedbackGuard] },
  { path: "**",redirectTo:"dashboard"}
];

@NgModule({
  declarations: [
    AppComponent, LoginComponent, DashboardRoutingComponent, Tenant1DashboardComponent,
    Tenant2DashboardComponent, ParentDashboard, StudentResults, StudentAssignmnet, ObjTForm,
    TeacherClasses, EditClass, ObjSortPipe, StudentClasses, NewClass, TeacherAssignment,
    MarksFeedback
  ],
  imports: [
    BrowserModule, HttpClientModule, ReactiveFormsModule, AvatarModule,
    AppRoutingModule, RouterModule.forRoot(routes, {onSameUrlNavigation: 'reload'})
  ],
  providers: [APIService, 
    {provide: JWT_OPTIONS, useValue: JWT_OPTIONS}, JwtHelperService,
    RouteGuard, DatePipe, TeacherGuard, EditGuard, MarkAndFeedbackGuard
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
