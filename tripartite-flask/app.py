import uuid, json
from flask import Flask, request, jsonify, make_response, send_file, send_from_directory
from bson import ObjectId
from datetime import timedelta
import datetime
import bcrypt
import os
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from flask_jwt_extended.utils import unset_jwt_cookies
from werkzeug.utils import secure_filename
import zipfile, io, re
from db_config import *

app = Flask(__name__)
CORS(app, supports_credentials=True)
jwt = JWTManager(app)
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config['JWT_SECRET_KEY'] = 'secretkey'

# Permitted file extensions for uploads
# Currently supports txt, word/excel files and some images
UPLOAD_EXTENSIONS = {
    'txt', 'pdf', 'doc', 'docx', 'docm',
     'dot', 'odt', 'rtf', 'png', 'jpg',
      'jpeg', 'xlsm', 'xlsx'
      }

# UPLOAD_Path wasset to local storage, must be updated to reflect cloud storage in production 
UPLOAD_PATH = r' '

## AUTHENTICATION ##
# login
# Checks a valid email has been supplied.
# Searches use collections for an email match.  IF this is found, 
# the password is verified. Upon successful verification of the user's
# credentials, an access token is created and saved in a cookie 
@app.route('/api/v1.0/login', methods=["POST"])
def login():
    try:
        auth_mail = request.headers['email']
        auth_pw = request.headers['password']
    except:
        return make_response(jsonify({"Error":"Missing form data"}),400)
    if __validate_email(auth_mail):
        if auth_mail and auth_pw:
            user_search_student =  student.find_one({'email':auth_mail}) 
            user_search_teacher = teacher.find_one({'email':auth_mail})
            user_search_parent = parent.find_one({'email':auth_mail})
            results = [user_search_student, user_search_parent, user_search_teacher]
            for result in results:
                if result is not None:
                    if bcrypt.checkpw(bytes(auth_pw, 'UTF-8'), result["password"]):
                        current_tenant = tenant.find_one({'tenant_id':result['tenant_id']})
                        additional_claims = {
                            '_id':str(result['_id']),
                            'first_name':result['first_name'],
                            'surname':result['surname'],
                            'user_type':result['user_type'],
                            'tenant_id':current_tenant['tenant_id'],
                            'tenant_name':current_tenant['tenant_name']
                        }
                        token = create_access_token(result["email"], additional_claims=additional_claims, fresh=True)
                        response = jsonify({'token':token,'data':additional_claims})
                        return make_response(response, 200)
                    else:
                        return make_response(jsonify({'error':'Authentication failed'}), 401)
                else:
                    continue
            return make_response(jsonify({'error':'Authentication failed'}),401)
        else:
            return make_response(jsonify({'error':'Email not found'}),401)
    else:
        return make_response(jsonify({'error':'Authentication failed'}),401)
# Logout
# The current cookie is unset, removing authorisation from the user
# effectively logging them out
@app.route('/api/v1.0/logout', methods=["GET"])
@jwt_required(fresh=True)
def logout():
    response = jsonify({'message':'logged out'})
    unset_jwt_cookies(response)
    return make_response(response, 200)

#### API ####

## 1. USERS ##

# get_tenant_count
# For getting a count of all tenants
# Note: currently for testing purposes only
@app.route("/api/v1.0/tenant", methods=["GET"])
def get_tenant_count():
    count = 0
    for i in tenant.find():
        count = count +1
    return make_response(jsonify({"count":count}),200)

# get_tenant
# searches for a tenant by its tenant_id
@app.route("/api/v1.0/tenant/<string:id>", methods=["GET"])
def get_tenant(id):
    try:
        tn = tenant.find_one({'tenant_id': int(id)},{'_id':0})
    except:
        return make_response(jsonify({"error":"invalid ID"}),404)
    if tn is not None:
        return make_response(jsonify({'data':tn}),200)
    else:
        return make_response(jsonify({'error':'Not found'}),404)

# get_user
# Generalised search that searches all collections for a given _id
@app.route('/api/v1.0/user/<string:id>', methods=['GET'])
def get_user(id):
    if ObjectId.is_valid(id):
        user_search_student =  student.find_one({"_id":ObjectId(id)},{'password':0}) 
        user_search_teacher = teacher.find_one({"_id":ObjectId(id)},{'password':0})
        user_search_parent = parent.find_one({"_id":ObjectId(id)},{'password':0})
        results = [user_search_teacher, user_search_parent, user_search_student]
        for result in results:
            if result is not None:
                result['_id'] = str(result['_id'])
                return make_response(jsonify({'data':result}),200)
        return make_response(jsonify({'error':'Not found'}),404)
    else:
        return make_response( jsonify({"error": "Invalid user ID"}), 404) 

# get_all_students
# A method that will return a list of all students for a Tenant.
# The method first ensures that the given ID is valid. If not, an error
# message is returned with the 404 response. Otherwise, it will retrieve
# all students belonging to the tenant, appending them to a list, which
# is returned with a 200 response. If there are no students, an empty
# list is returned
@app.route('/api/v1.0/students/<string:tenant_id>', methods=["GET"])
def get_all_students(tenant_id):
    try:
        tenant = get_tenant(tenant_id).get_json()["data"]
    except:
        return make_response(jsonify({"error":"invalid Tenant ID"}),404)
    student_list = []
    for i in student.find({'tenant_id':tenant['tenant_id']},{
        'password':0,'DOB':0,'email':0,
        'address':0,'postcode':0,'city':0,
        'country':0,'tenant_id':0,'guardians':0,
        'enrolled_date':0, 'user_type':0
        }):
        i["_id"] = str(i["_id"])
        student_list.append(i)
    if len(student_list) > 0:
        return make_response( jsonify(student_list), 200)
    else:
        return make_response(jsonify({"message":"no students found"}), 200) 


## 2. CLASSES ##

# get_class
# Public get_class method, utlises the private helper
# method to find a single class by the given ID.
@app.route('/api/v1.0/class/<string:class_id>', methods=["GET"])
def get_class(class_id):
    if ObjectId.is_valid(class_id):
        class_obj = __get_class_by_id(class_id)
        return class_obj
    else:
        return make_response(jsonify({'error':'invalid object ID'}),400)

# create_class
# Creates and saves a new class instance, storing the teacher's ID, subject,
# tenant ID and default empty sub document to store the student IDs.
#
# Checks that the appropriate data has been found in the body, identifies the teacher, and
# attempts to insert it into the classes collection. If the teacher already has a class
# booked for this slot, it will return a 403 error.  IF the database connection fails
# this returns a 404 error. Otherwise, the new _id will be returned with the 201 response
@app.route('/api/v1.0/class', methods=["POST"])
def create_class():
    if "teacher_id" in request.form and "subject" in request.form and "day" in request.form and "period" in request.form:
        try:
            teacher = get_user(request.form["teacher_id"]).get_json()["data"]
        except:
            return make_response(jsonify({"error":"invalid ID"}),404)
        try:
            class_subject = request.form["subject"]
            class_day = request.form["day"]
            period = int(request.form["period"])
        except:
            return make_response(jsonify({"error":"invalid input"}),422)
        if "students" in request.form:
            student_list_json = json.loads(request.form["students"])
            if student_list_json is not None:
                student_list = []
                for i in student_list_json:
                    try:
                        id_check = student.find({"_id":ObjectId(i['id'])})
                        if id_check is not None:
                            this_student = {
                                'id': i['id'],
                                'year_group':int(i['year_group']),
                                'name': i['name']
                            }
                            student_list.append(this_student)
                        else:
                            continue
                    except:
                        return make_response(jsonify({"error":"invalid input"}),422)
                new_class = {
                    "teacher_id": teacher["_id"],
                    "tenant_id": teacher["tenant_id"],
                    "subject": class_subject,
                    "students": student_list,
                    "day": class_day,
                    "period":period,
                    "teacher_name": teacher["first_name"] + " " + teacher["surname"]
                }
                try:
                    conflict_check = __conflict_checker(teacher["_id"], None, request.form["day"], request.form["period"])
                    if conflict_check is None:    
                        new_class_id = classes.insert_one(new_class)
                        return make_response(jsonify({"class_id": str(new_class_id.inserted_id)}),201)
                    else:
                        return make_response(jsonify({"error":"scheduling conflict"}),409)
                except:
                    return make_response( jsonify({"error":"database not found"}), 404)
            else:
                new_class = {
                "teacher_id": teacher["_id"],
                "tenant_id": teacher["tenant_id"],
                "subject": class_subject,
                "students": [],
                "day":class_day,
                "period":period,
                "teacher_name": teacher["first_name"] + " " + teacher["surname"]
            }
            try:
                conflict_check = __conflict_checker(teacher["_id"], '', request.form["day"], request.form["period"])
                if conflict_check is None:    
                    new_class_id = classes.insert_one(new_class)
                    return make_response(jsonify({"class_id": str(new_class_id.inserted_id)}),201)
                else:
                    return make_response(jsonify({"error":"scheduling conflict"}),409)
            except:
                return make_response( jsonify({"error":"database not found"}), 404)
        else:
            new_class = {
                "teacher_id": teacher["_id"],
                "tenant_id": teacher["tenant_id"],
                "subject": class_subject,
                "students": [],
                "day":class_day,
                "period":period,
                "teacher_name": teacher["first_name"] + " " + teacher["surname"]
            }
            try:
                conflict_check = __conflict_checker(teacher["_id"], '', request.form["day"], request.form["period"])
                if conflict_check is None:    
                    new_class_id = classes.insert_one(new_class)
                    return make_response(jsonify({"class_id": str(new_class_id.inserted_id)}),201)
                else:
                    return make_response(jsonify({"error":"scheduling conflict"}),409)
            except:
                return make_response( jsonify({"error":"database not found"}), 404)
    else:
        return make_response(jsonify({"Error":"Missing form data"}),400)

# edit_class
# Edit a previously created class
# Editable fields: day, period, subject.
@app.route('/api/v1.0/class/<string:class_id>', methods=["PUT"])
def edit_class(class_id):
    class_to_edit = __get_class_by_id(class_id)
    if class_to_edit is not None:
        if "subject" in request.form and "day" in request.form and "period" in request.form:
            try:
                class_subject = request.form["subject"]
                class_day = request.form["day"]
                period = int(request.form["period"])
            except:
                return make_response(jsonify({"error":"invalid input"}),422)
            conflict_check = __conflict_checker(class_to_edit["teacher_id"], class_to_edit["_id"], request.form["day"], request.form["period"])
            if conflict_check is None:
                classes.update_one({'_id':ObjectId(class_id)},{
                    '$set': {
                        'subject': class_subject,
                        'day': class_day,
                        'period': period
                    }
                })
                return make_response(jsonify({"class_id":str(class_to_edit["_id"])}),200)
            else:
                return make_response(jsonify({"error":"scheduling conflict"}),409)
        else:
            return make_response(jsonify({"Error":"Missing form data"}),400)
    else:
        return make_response(jsonify({"error":"class not found"}),404)
 
# delete_class
# Finds and deletes the class using its object ID
@app.route('/api/v1.0/class/<string:class_id>', methods=["DELETE"])
def delete_class(class_id):
    if ObjectId.is_valid(class_id):
        class_to_delete = classes.delete_one({'_id':ObjectId(class_id)})
        if class_to_delete.deleted_count == 1:
            return make_response(jsonify({"success":"class deleted"}),204)
        else:
            return make_response(jsonify({"error":"No class with this ID"}),404)
    else:
        return make_response(jsonify({"error":"invalid object ID"}),400)

# get_subjects
# Getter for all subjects in the subject document
@app.route('/api/v1.0/subjects', methods=["GET"])
def get_subjects():
    subjects = []
    for sub in subject.find({},{'_id':0,'sub_id':0}):
        subjects.append(sub)
    return make_response(jsonify(subjects),200)

# get_classes_teacher
# Uses the provided Teacher ID to first confirm the teacher's identity
# and then search for all classes beloning to that teacher.
#
# If the Teacher does not exist, returns an error message with a  404 reponse
# Any classes found are appended to a list which is returned as JSON. otherwise,
# if there are no, classes associated with the Teacher ID, a message is returned
# with the 200 reponse. 
@app.route('/api/v1.0/teacher_classes/<string:teacher_id>', methods=["GET"])
def get_classes_teacher(teacher_id):
    try:
        teacher = get_user(teacher_id).get_json()["data"]
    except:
        return make_response(jsonify({"error":"teacher ID not found"}), 404)
    classes_list = []
    for i in classes.find({'teacher_id':teacher['_id']}):
        i["_id"] = str(i["_id"])
        classes_list.append(i)
    if len(classes_list) > 0:
        return make_response( jsonify(classes_list), 200)
    else:
        return make_response(jsonify({"message":"no classes found"}), 200) 

# add_student
# Function that adds a student's ID to the student sub document of an existing class.
# Function confirms the class & student exists in respective collections.
# If the student is a member of the current tenant, their data is added to a list
# which is then used to update the student sub document.
# If the student ID already exists in the sub document, a message is returned and
# the ID is not added again.  
@app.route('/api/v1.0/class/<string:class_id>/add/<string:student_id>', methods=["PUT"])
def add_student(class_id, student_id):
    try:
        class_to_update = __get_class_by_id(class_id)
    except:
        return make_response(jsonify({"error":"invalid class ID"}),404)
    if class_to_update is not None:
        try:
            current_student = get_user(student_id).get_json()["data"]  
        except:
            return make_response(jsonify({"error":"Invalid student ID"}),404)
        if current_student["tenant_id"] == class_to_update["tenant_id"]:
            student_list = class_to_update["students"]
            for i in student_list:
                if i['id'] == current_student['_id']:
                    return make_response(jsonify({'error':'student already in class'}),409)
                else:
                    continue
            student_list.insert(-1,{
                        'id':current_student['_id'], 
                        'name':current_student['first_name']+ " " + current_student['surname'],
                        'year_group': current_student['year_group']
                        })
            classes.update_one({'_id':ObjectId(class_to_update['_id'])},{
                    '$set':{
                        'students': student_list
                    }
                })
            return make_response(jsonify({'message':'student added to class'}),200)
        else:
            return make_response(jsonify({"error":"ID does not belong to tenant"}),403)
    else:
        return make_response(jsonify({"error":"Invalid class ID"}),404)

# remove_student
# A function to remove a student from an existing class.
@app.route('/api/v1.0/class/<string:class_id>/remove/<string:student_id>', methods=["PUT"])
def remove_student(class_id, student_id):
    try:
        class_to_update = __get_class_by_id(class_id)
    except:
        return make_response(jsonify({"error":"invalid class ID"}),404)
    if class_to_update is not None:
        try:
            current_student = get_user(student_id).get_json()["data"]  
        except:
            return make_response(jsonify({"error":"Invalid student ID"}),404)
        if current_student["tenant_id"] == class_to_update["tenant_id"]:
            student_list = class_to_update["students"]
            for i in student_list:
                if i['id'] == current_student['_id']:
                    student_list.remove(i)
                else:
                    continue
            classes.update_one({'_id':ObjectId(class_to_update['_id'])},{
                '$set':{
                    'students': student_list
                }
            })
            return make_response(jsonify({'message':'student removed from class'}),200)        
        else:
            return make_response(jsonify({"error":"ID does not belong to tenant"}),403)
    else:
        return make_response(jsonify({"error":"Invalid class ID"}),404)

# get_classes_student
# Uses the provided student ID to confirm the student's identity
# and then search for all classes beloning to that student.
#
# The search is accomplished by retrieving any documents where
# the student ID is found in the 'students' sub document
#
# If the student does not exist, returns an error message with a  404 reponse
# Any classes found are appended to a list which is returned as JSON. otherwise,
# if there are no, classes associated with the Teacher ID, a message is returned
# with the 200 reponse. 
@app.route('/api/v1.0/student_classes/<string:student_id>', methods=["GET"])
def get_classes_student(student_id):
    try:
        student = get_user(student_id).get_json()["data"]
    except:
        return make_response(jsonify({"error":"student ID not found"}), 404)
    classes_list = []
    for i in classes.find({'students.id':student["_id"]},{'students':0}):
        i["_id"] = str(i["_id"])
        classes_list.append(i)
    if len(classes_list) > 0:
        return make_response( jsonify(classes_list), 200)
    else:
        return make_response(jsonify({"message":"no classes found"}), 200) 


## 3. ASSIGNMENTS ##

# create_assignment
# Function that instantiates a new assignment.
# First confirms the teacher's ID. Teacher's storage is found, or created if required.
# Function then checks that the file being uploaded is permitted and the assignment's
# details are initialised. A check is then performed to ensure that this an assignment
# of the given title does not already exist for the class.
# Following this, the storage is checked to ascertain if a file exists with the same
# name as the file being uploaded. If so, a UUID is appended to the file name.
# The filename and path the file are appended to the new_assignment dict.
# The file is saved to the user's storage file and the associated JSON object
# is inserted into the assignment collection
@app.route('/api/v1.0/<string:class_id>/assignment/<string:teacher_id>/create',methods=["POST"])
def create_assignment(teacher_id, class_id):
    try:
        teacher = get_user(teacher_id).get_json()["data"]
        clas = __get_class_by_id(class_id)
    except:
        return make_response(jsonify({"error":"ID not found"}), 404)
    if clas is not None:
        if clas['tenant_id'] == teacher['tenant_id']:
            if 'file' in request.files and 'title' in request.form and 'deadline' in request.form:
                dir = __storage_directory(teacher['_id'], teacher['tenant_id'])
                file_to_upload = request.files['file']
                date_time = datetime.date.today()
                if file_to_upload.filename != '':
                    if __extension_checker(file_to_upload.filename):
                        new_assignment = {
                            'title': request.form["title"],
                            'teacher_id': teacher["_id"],
                            'class_id': clas['_id'],
                            'created_date': str(date_time),
                            'deadline': str(request.form['deadline']),
                            'tenant_id': teacher['tenant_id']
                        }
                        assignment_check = assignment.find_one({'title':new_assignment['title'], 'class_id':new_assignment['class_id']})
                        if assignment_check is None:
                            filename_check = __filename_checker(dir, file_to_upload.filename)
                            if filename_check == 0:
                                filename = secure_filename(file_to_upload.filename)
                                file_to_upload.save(os.path.join(dir, filename))
                                new_assignment["filename"] = filename
                                new_assignment["filepath"] = dir + "/"
                            else:
                                split = file_to_upload.filename.split('.')
                                filename_edit = split[0] + str(uuid.uuid4()) + '.' + split[1]
                                filename = secure_filename(filename_edit)
                                file_to_upload.save(os.path.join(dir, filename))
                                new_assignment["filename"] = filename
                                new_assignment["filepath"] = dir + "/"
                            assignment_id = assignment.insert_one(new_assignment)            
                            return make_response(jsonify({'assignment_id':str(assignment_id.inserted_id)}),200)
                        else:
                            return make_response(jsonify({"error":"assignment with this title already exists for this class"}),409)
                    else:
                        return make_response(jsonify({"error":"invalid file format"}),422)
                else:
                    return make_response(jsonify({"error":"no file found"}), 404)
            else:
                return make_response(jsonify({"error":"missing form data"}), 400)
        else:
            return make_response(jsonify({'error':'user request outside tenant group. Permission denied'}),403)
    else:
        return make_response(jsonify({"error":"no class found"}), 404)

# edit_assignment
# A function to update the title, deadline or file for a saved
# assignment.  Begins by confirming that the assignment exists by
# performing a search with the given ID.  If the required fields are
# found in tje request body, the fields are updated in the appropriate
# document. Additionally, if a file is provided, it overwrites the previously
# uploaded document
@app.route('/api/v1.0/assignment/<string:assignment_id>', methods=["PUT"])
def edit_assignment(assignment_id):
    try:
        assignment_to_edit = get_assignment(assignment_id).get_json()['data']
    except:
        return make_response(jsonify({"error":"Assignment not found"}),404)
    if 'file' in request.files:
        file_to_upload = request.files['file']
        if __extension_checker(file_to_upload.filename):
            if 'title' in request.form and 'deadline' in request.form and 'teacher_id' in request.form:
                try:
                    current_teacher = get_user(request.form["teacher_id"]).get_json()['data']
                except:
                    return make_response(jsonify({'error':'invalid teacher ID'}),404)
                if current_teacher["tenant_id"] == assignment_to_edit['tenant_id']:
                    file_to_replace = assignment_to_edit['filepath'] + assignment_to_edit['filename']
                    dir = __storage_directory(current_teacher['_id'], current_teacher['tenant_id'])
                    if os.path.exists(file_to_replace):
                        os.remove(file_to_replace)
                        filename = secure_filename(file_to_upload.filename)
                        file_to_upload.save(os.path.join(dir, filename))
                        assignment.update_one({"_id":ObjectId(assignment_to_edit['_id'])},{
                                        '$set':{
                                            'title':request.form["title"],
                                            'deadline':str(request.form['deadline']),
                                            'filename': filename,
                                            'filepath': dir + '/'
                                            }
                                        })
                        return make_response(jsonify({"message":"update successful"}),200)
                    else:
                        filename = secure_filename(file_to_upload.filename)
                        file_to_upload.save(os.path.join(dir, filename))
                        assignment.update_one({"_id":ObjectId(assignment_to_edit['_id'])},{
                        '$set':{
                            'title':request.form["title"],
                            'deadline':str(request.form['deadline']),
                            'filename': filename,
                            'filepath': dir + '/'
                            }
                        })
                        return make_response(jsonify({"message":"update successful"}),200)
                else:
                    return make_response(jsonify({"error":"user forbidden to edit this content"}),403)
            else:
                return make_response(jsonify({"error":"missing form data"}), 400)
        else:
            return make_response(jsonify({"error":"invalid file format"}),422)
    else:
        if 'title' in request.form and 'deadline' in request.form and 'teacher_id' in request.form:
            try:
                current_teacher = get_user(request.form["teacher_id"]).get_json()['data']
            except:
                return make_response(jsonify({'error':'invalid teacher ID'}),404)
            if current_teacher["tenant_id"] == assignment_to_edit['tenant_id']:
                assignment.update_one({"_id":ObjectId(assignment_to_edit['_id'])},{
                    '$set':{
                        'title':request.form["title"],
                        'deadline':str(request.form['deadline'])
                    }
                })
                return make_response(jsonify({'message':'assignment updated'}),200)
            else:
                return make_response(jsonify({"error":"user forbidden to edit this content"}),403)
        else:
            return make_response(jsonify({"error":"missing form data"}), 400)

# get_assignment
# Function to retrieve an assignment from the assignment collection
# using the object ID. Checks if a valid object ID has been provided.
# If so, searches the collection and returns the assignment object or
# an error if no object exists with the given ID
@app.route('/api/v1.0/assignment/<string:assignment_id>', methods=["GET"])
def get_assignment(assignment_id):
    if ObjectId.is_valid(assignment_id):
        assignment_to_find = assignment.find_one({"_id":ObjectId(assignment_id)})
        if assignment_to_find is not None:
            assignment_to_find["_id"] = str(assignment_to_find["_id"])
            return make_response(jsonify({"data":assignment_to_find}),200)
        else:
            return make_response(jsonify({"error":"No assignment found"}),404)
    else:
        return make_response(jsonify({"error":"invalid ID"}),404)

# get_assignments_teacher
# A function to find all assignments attributed to a teacher.
# First the given ID is verified by finding the teacher. This is followed
# by a search of the assignment collection.  Any assignment whose teacher_id
# field matches the teacher's own ID, will be added to a list.  This list
# is returned.
@app.route('/api/v1.0/teacher_assignments/<string:teacher_id>', methods=["GET"])
def get_assignments_teacher(teacher_id):
    try:
        teacher = get_user(teacher_id).get_json()["data"]
    except:
        return make_response(jsonify({"error":"teacher ID not found"}), 404)
    if teacher is not None:
        assignment_list = []
        for i in assignment.find({"teacher_id":teacher['_id']}):
            i['_id'] = str(i['_id'])
            assignment_list.append(i)
        return make_response(jsonify({'data':assignment_list}),200)
    else:
        return make_response(jsonify({"error":"teacher ID not found"}), 404)

# get_assignments_class
# A method to retrieve all assignments associated with a class.
# A search of the assignment collection is completed using the given
# class ID. Any records found are appended to a list and returned to the
# user
#ToDo: only retrieve where today >= deadline
@app.route('/api/v1.0/assignment/<string:class_id>/find', methods=["GET"])
def get_assignments_class(class_id):
    class_check = __get_class_by_id(class_id)
    if class_check is not None:
        assignment_list = []
        for i in assignment.find({"class_id":class_id}):
            i['_id'] = str(i['_id'])
            assignment_list.append(i)
        return make_response(jsonify({'data':assignment_list}),200)
    else:
        return make_response(jsonify({"error":"invalid ID"}),404)

# download_assignment_file
# Function that retreives an assignment file from storage. First it checks
# that the reference exists in the collection and that the filepath exists.
# If so, the file is then downloaded onto the user's machine
@app.route('/api/v1.0/assignment/<string:assignment_id>/download', methods=["GET"])
def download_assignment_file(assignment_id):
    try:
        assignment_check = get_assignment(assignment_id).get_json()['data']
    except:
        return make_response(jsonify({'error':'assignment not found'}),404)
    if os.path.exists(assignment_check['filepath']):
        try:
            return send_from_directory(assignment_check['filepath'], assignment_check['filename'])
        except:
            return make_response(jsonify({'error':'file not found'}),404)
    else:
        return make_response(jsonify({'error':'file not found'}),404)

# delete_assignment
# Deletes an instance of an assignment from the assignment collection in the
# database, including the affiliated file uploaded to storage.
# Checks there is a reference for the assignment in the collection, then
# checks the file exists in the storage using the saved filepath.
# If it is found, the file is deleted, and then the document is deleted
# from the collection.
@app.route('/api/v1.0/assignment/<string:assignment_id>', methods=["DELETE"])
def delete_assignment(assignment_id):
    try:
        assignment_to_delete = get_assignment(assignment_id).get_json()['data']
    except:
        return make_response(jsonify({'error':'assignment ID not found'}),404)
    if assignment_to_delete is not None:
        filepath = assignment_to_delete['filepath'] + assignment_to_delete['filename']
        if os.path.exists(filepath):
            os.remove(filepath)
            try:
                result = assignment.delete_one({'_id':ObjectId(assignment_to_delete['_id'])})
                if result.deleted_count == 1:
                    return make_response(jsonify({}),204)
                else:
                    return make_response(jsonify({'error':'Invalid assignment ID'}),404)
            except:
                return make_response(jsonify({'error':'error occured, assigment not deleted'}),500)
        else:
            try:
                result = assignment.delete_one({'_id':ObjectId(assignment_to_delete['_id'])})
                if result.deleted_count == 1:
                    return make_response(jsonify({}),204)
                else:
                    return make_response(jsonify({'error':'Invalid assignment ID'}),404)
            except:
                return make_response(jsonify({'error':'error occured, assigment not deleted'}),500)
    else:
        return make_response(jsonify({'error':'assignment not found'}),404)

## 4. SUBMISSIONS ##

# download_assignment_submissions
# Enables a teacher to fetch all submissions for a submission.  First, the assignment ID
# is verified by searching the collection with the get_assignment function. If found, a binary
# stream is instantiated, along with a zipfile. All submissions associated with the assignment
# are found, and their uploaded document added to the zip. The file name is created using the
# assignment ID and the current date.  This is then sent for download using the send_file function
#
# ToDo: strong input validation required to ensure security? re: send_file lacks sanitation checks
@app.route('/api/v1.0/assignment/<string:assignment_id>/submission_download', methods=["GET"])
def download_assignment_submissions(assignment_id):
    try:
        current_assignment = get_assignment(assignment_id).get_json()['data']
    except:
        return make_response(jsonify({'error':'assignment not found, invalid ID'}))
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as zfile:
        for i in submission.find({'assignment_id':current_assignment["_id"]}):
            if os.path.exists(i['filepath']):
                path = i['filepath']+i['filename']
                zfile.write(path, os.path.basename(path))
    data.seek(0)
    filename =  current_assignment["_id"] + str(datetime.date.today()) + '.zip'
    return send_file(data, mimetype='application/zip', as_attachment= True, attachment_filename= filename)

# get_all_submissions
# Retrieves all submission references, associated with the given assignment ID, from the database 
@app.route('/api/v1.0/<string:assignment_id>/submissions', methods=["GET"])
def get_all_submissions(assignment_id):
    try:
        current_assignment = get_assignment(assignment_id).get_json()['data']
    except:
        return make_response(jsonify({'error':'assignment not found, invalid ID'}),404)
    submission_list = []
    for i in submission.find({'assignment_id':current_assignment["_id"]}):
        i['_id'] = str(i['_id'])
        submission_list.append(i)
    return make_response(jsonify(submission_list),200)

# get_submission
# A function to fetch a submission by its student_id and assignment_id
# First checks the ID is valid by finding the submission ref in the submission collection
# and returns the submission data as JSON if found. Otherwise an error is returned
@app.route('/api/v1.0/<string:student_id>/submission/<string:assignment_id>', methods=["GET"])
def get_submission(student_id, assignment_id):
    try:
        submission_to_find = submission.find_one({'student_id':student_id,'assignment_id':assignment_id})
    except:
        return make_response(jsonify({'error':'invalid ID'}),404)
    if submission_to_find is not None:
        submission_to_find['_id'] = str(submission_to_find['_id'])
        return make_response(jsonify({'data':submission_to_find}),200)
    else:
        return make_response(jsonify({'error':'No submission found'}),404)

# create_submission
# Upload's a students submission for an assignment and creates a reference within the submission collection.
# First confirms the student and assignment exist. After ascertaining that a file is ready for upload,
# the student's storage is found, or created if requried. Following this, it is confirmed that the file
# is valid, according to the upload extensions. A new submission is set up and a check is performed 
# to see if the student has already submitted for the assignment.  If not, the storage is checked
# for any files with the same name. If so, the filename is appended with an integer equal to the count
# of files with the same name. The file and reference are both saved.  
# If the student has previously made a submission for this assignment, the newly uploaded file
# overwrites the previous upload and the filename, filepath and date_submitted fields of the document
# are updated.  
@app.route('/api/v1.0/assignment/<string:assignment_id>/submission/<string:student_id>', methods=["POST"])
def create_submission(assignment_id, student_id):
    try:
        current_student = get_user(student_id).get_json()['data']
        current_assignment = get_assignment(assignment_id).get_json()['data']
    except:
        return make_response(jsonify({'error':'user or assignment not found'}),404)
    if current_student['tenant_id'] == current_assignment['tenant_id']:
        if 'file' in request.files:
            dir = __storage_directory(current_student['_id'], current_student['tenant_id'])
            file_to_upload = request.files['file']
            date_time = datetime.date.today()
            if file_to_upload.filename != '':
                if __extension_checker(file_to_upload.filename):
                    new_submission = {
                        'student_id':current_student['_id'],
                        'firstname': current_student['first_name'],
                        'surname': current_student['surname'],
                        'assignment_id': current_assignment['_id'],
                        'class_id':current_assignment['class_id'],
                        'mark':'',
                        'feedback':'',
                        'feedback_private':'',
                        'submission_date':str(date_time),
                        'marked': False
                    }
                    submission_check = submission.find_one({'student_id':current_student['_id'],'assignment_id':current_assignment['_id']})
                    if submission_check is None:
                        filename_check = __filename_checker(dir, file_to_upload.filename)
                        if filename_check == 0:
                            filename = secure_filename(file_to_upload.filename)
                            file_to_upload.save(os.path.join(dir, filename))
                            new_submission["filename"] = filename
                            new_submission["filepath"] = dir + "/"           
                        else:
                            split = file_to_upload.filename.split('.')
                            filename_edit = split[0] + str(filename_check) + '.' + split[1]
                            filename = secure_filename(filename_edit)
                            file_to_upload.save(os.path.join(dir, filename))
                            new_submission["filename"] = filename
                            new_submission["filepath"] = dir + "/"
                        submission_id = submission.insert_one(new_submission)            
                        return make_response(jsonify({'submission_id':str(submission_id.inserted_id)}),200)
                    else:
                        file_to_replace = submission_check['filepath'] + submission_check['filename']
                        if os.path.exists(file_to_replace):
                            os.remove(file_to_replace)
                            filename = secure_filename(file_to_upload.filename)
                            file_to_upload.save(os.path.join(dir, filename))
                            submission.find_one_and_update({'_id':ObjectId(submission_check['_id'])},{
                                '$set':{
                                    'submission_date':str(date_time),
                                    'filename': filename,
                                    'filepath': dir + "/"
                                }
                            })
                        else:
                            filename = secure_filename(file_to_upload.filename)
                            file_to_upload.save(os.path.join(dir, filename))
                            submission.find_one_and_update({'_id':ObjectId(submission_check['_id'])},{
                                '$set':{
                                    'submission_date':str(date_time),
                                    'filename': filename,
                                    'filepath': dir + "/"
                                }
                            })
                        return make_response(jsonify({'submission_id':str(submission_check['_id'])}),200)
                else:
                    return make_response(jsonify({"error":"invalid file format"}),422)
            else:
                return make_response(jsonify({"error":"file must have a valid filename"}), 400)
        else:
            return make_response(jsonify({"error":"no file found"}), 400)
    else:
        return make_response(jsonify({'error':'user request outside tenant group. Permission denied'}),403)

# add_marks_and_feedback
# Function that updates a submission document with a mark/grade and feedback
# from the teacher.  Can also include feedback_private. This comment will
# only be available to the teacher and parent/guardian of the student.
# First, the submission is found. If the required fields are found within
# the body of the request, the document is updated accordingly
@app.route('/api/v1.0/submission/<string:submission_id>', methods=['PUT'])
def add_marks_and_feedback(submission_id):
    try:
        submission_check = submission.find_one({'_id':ObjectId(submission_id)})
    except:
        return make_response(jsonify({"error":"submission not found"}),404)
    if 'mark' in request.form and 'feedback' in request.form:
        if 'feedback_private' in request.form:
            submission.find_one_and_update({'_id':ObjectId(submission_check['_id'])},{
                            '$set':{
                                'mark':request.form['mark'],
                                'feedback':request.form['feedback'],
                                'feedback_private':request.form['feedback_private'],
                                'marked': True
                            }
                        })
            return make_response(jsonify({'message':'submission marked'}),200)
        else:
            submission.find_one_and_update({'_id':ObjectId(submission_check['_id'])},{
                            '$set':{
                                'mark':request.form['mark'],
                                'feedback':request.form['feedback'],
                                'feedback_private':'',
                                'marked': True
                            }
                        })
            return make_response(jsonify({'message':'submission marked'}),200)
    else:
        return make_response(jsonify({"error":"missing form data"}), 400)

## ToDo: convert dashboard_builder & student_result_builder to single function ## 

# dashboard_builder
# single function to return all data required for the parent dashboard component.
# this includes all students connected with the user, their classes and any
# marked assignments
@app.route('/api/v1.0/dashboard/<string:parent_id>', methods=['GET'])
def dashboard_builder(parent_id):
    try:
        parent =  get_user(parent_id).get_json()["data"]
    except:
        return make_response(jsonify({'error':'user not found'}),404)
    data = {}
    for id in parent["registered_students"]:
        class_list = []
        stdnt = get_user(id).get_json()["data"]
        name = stdnt['first_name'] + " " + stdnt['surname']
        student_classes = get_classes_student(stdnt['_id']).get_json()
        for c in student_classes:
            submission_list = []
            for i in submission.find({'student_id':stdnt['_id'],'class_id':c['_id'],'marked':True},{'filename':0,'filepath':0}):
                i['_id'] = str(i['_id'])
                submission_list.append(i)
            class_list.append({'class':c, 'results':submission_list})
        data[str(id)] = {
            'name': name,
            'classes':class_list,
            }
    return make_response(jsonify(data),200)

# student_result_builder
# A function used to deliver all results for marked work for the student
# my results view
@app.route('/api/v1.0/results/<string:student_id>', methods=['GET'])
def student_results_builder(student_id):
    try:
        current_student = get_user(student_id).get_json()["data"]
    except:
        return make_response(jsonify({'error':'user not found'}),404)
    class_list = []
    student_classes = get_classes_student(current_student['_id']).get_json()
    for c in student_classes:
        submission_list = []
        for i in submission.find({
            "student_id":current_student["_id"],"class_id":c["_id"],"marked":True },
            {'filename':0,'filepath':0,'feedback_private':0 }):
            i["_id"] = str(i["_id"])
            submission_list.append(i)
            class_list.append({"class":c, "results":submission_list})
    return make_response(jsonify(class_list),200)

# student_assignment_builder
# A function used to deliver all current assignments to the student for
# the assignment view.  Only assignments that have not gone passed
# their deadline will be returned
@app.route('/api/v1.0/assignments/<string:student_id>', methods=['GET'])
def student_assignment_builder(student_id):
    try:
        current_student = get_user(student_id).get_json()["data"]
    except:
        return make_response(jsonify({'error':'user not found'}),404)
    data = []
    date = datetime.datetime.fromisoformat(str(datetime.datetime.today() - timedelta(days=1)).split(" ")[0])
    student_classes = get_classes_student(current_student["_id"]).get_json()
    for c in student_classes:
        assignment_list = []
        for i in assignment.find({"class_id":c["_id"]}):
            i["_id"] = str(i["_id"])
            deadline = datetime.datetime.fromisoformat(i["deadline"])
            if deadline >= date:
                assignment_list.append(i)
        data.append({"class":c, "assignments":assignment_list})
    return make_response(jsonify(data),200)

# teacher_assignment_builder
@app.route('/api/v1.0/teacher-assignments/<string:teacher_id>', methods=['GET'])
def teacher_assignment_builder(teacher_id):
    try:
        current_teacher = get_user(teacher_id).get_json()['data']
    except:
        return make_response(jsonify({'error':'user not found'}),404)
    data = []
    teacher_classes = get_classes_teacher(current_teacher['_id']).get_json()
    for c in teacher_classes:
        assignment_list = []
        for i in assignment.find({"class_id":c["_id"]}):
            i["_id"] = str(i["_id"])
            assignment_list.append(i)
        data.append({"class":c, 'assignments':assignment_list })
    return make_response(jsonify(data),200)


#### HELPER FUNCTIONS ####

# conflict_checker
# Private function, used to check that a teacher does not already
# have an existing class. Utilsed in the create_class & edit_class methods.
# Method also ensures that, if a class is found, that it is not the class
# being 
def __conflict_checker(teacher_id, class_id, day, period):
    try:
        conflict_check = classes.find_one({'teacher_id':teacher_id,'day':day, 'period':int(period)})
    except:
        return make_response(jsonify({"error":"invalid input"}),422)
    if conflict_check is not None:
        conflict_check['_id'] = str(conflict_check['_id'])
        if conflict_check['_id'] == class_id:
            return None
        else:
            return conflict_check

# get_class
# Private function, used to retrieve a specific class by its ID.
def __get_class_by_id(class_id):
    if ObjectId.is_valid(class_id):
        class_to_find = classes.find_one({"_id":ObjectId(class_id)})
        if class_to_find is not None:
            class_to_find["_id"] = str(class_to_find["_id"])
            return class_to_find
        else:
            return None
    else: 
        return None 

# storage_directory
# Searches for user's directory.  If it exists, returns
# path as a string. If it doesn't exist, first creates 
# the directory and returns the new filepath
def __storage_directory(id, tenant):
    path = UPLOAD_PATH + str(tenant)
    if not os.path.exists(path + '/' + id):
        os.makedirs(path + '/'+ str(id))
        return path + '/'+ str(id)
    else:
        return str(path + '/'+ str(id))

# extension_checker
# Used to check that the file being uploaded has a valid extensions as defined in
# UPLOAD_EXTENSIONS
def __extension_checker(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in UPLOAD_EXTENSIONS

# filename_checker
# When a user is uploading a file, the name is checked against others
# within the filepath directory. For each file found with the same name,
# a count (num) is incremented.  This count is returned in the method where the 
# filename_checker was called
def __filename_checker(filepath, filename):
    num = 0
    files = next(os.walk(filepath), (None, None, []))[2]
    for i in files:
        if str(i) == filename:
            num = num + 1
    return num

# Validation function for ensuring a valid email has been provided during login
def __validate_email(email):
    rgx = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(rgx, email)


## SCHEDULED TASKS ##
# Function that will execute any daily scheduled tasks
def scheduled_tasks():
    db_backup()

## ToDo: Add annual scheduled task to update year groups

# Initialises the scheduler, adds the scheduled tasks and sets execution
# time to run daily at 23.54pm, creating a backup of the database
schedule = BackgroundScheduler()
schedule.add_job(scheduled_tasks, trigger='cron', hour=23, minute=00)
schedule.start()

if __name__ == "__main__":
    app.run(debug=True)