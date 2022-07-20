# Used to generate dummy data for classes, assignments & submissions for the
# generated users
import random

from pymongo import MongoClient

# MongoDB client and documents
mongo_client = MongoClient(" ")
db = mongo_client.projectDB
classes = db.classes
subject = db.subject
assignment = db.assignment
submission = db.submission
student = db.student
teacher = db.teacher

# Generates subjects to be stored in the subject collection
def generate_subjects():
    subjects = ['Math','English','Geography','Physics','Biology','Chemistry','History','Programming']
    index = 0
    for i in subjects:
        subject.insert_one({'sub_id':index,'subject':i})
        index = index + 1

# Generates 2 classes for each tenant using the pre-generated user data for
# Teachers & Students in user_tenant_factory. This data is stored in the 
# class collection
def generate_classes():
    subjects = ['Math','English','Geography','Physics','Biology','Chemistry','History','Programming']
    days =  ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    teachers_ten1 = []
    teachers_ten2 = []
    students_ten1_year3 =  []
    students_ten2_year3 =  []
    students_ten1_year4 =  []
    students_ten2_year4 =  []
    students_ten1_year5 =  []
    students_ten2_year5 =  []

    for i in teacher.find():
        i["_id"] = str(i["_id"])
        if i['tenant_id'] == 1:
            teachers_ten1.append(i)
        else:
            teachers_ten2.append(i)

    for i in student.find():
        i["_id"] = str(i["_id"])
        if i['tenant_id'] == 1:
            if i["year_group"] == 3:
                students_ten1_year3.append({'id':i['_id'],'name':i['first_name'] + " "+i['surname'], 'year_group':i['year_group'] })
            elif i["year_group"] == 4:
                students_ten1_year4.append({'id':i['_id'],'name':i['first_name'] + " "+i['surname'], 'year_group':i['year_group'] })
            elif i["year_group"] == 5:
                students_ten1_year5.append({'id':i['_id'],'name':i['first_name'] + " "+i['surname'], 'year_group':i['year_group'] })
        elif i['tenant_id'] == 2:
            if i["year_group"] == 3:
                students_ten2_year3.append({'id':i['_id'],'name':i['first_name'] + " "+i['surname'], 'year_group':i['year_group'] })
            elif i["year_group"] == 4:
                students_ten2_year4.append({'id':i['_id'],'name':i['first_name'] + " "+i['surname'], 'year_group':i['year_group'] })
            elif i["year_group"] == 5:
                students_ten2_year5.append({'id':i['_id'],'name':i['first_name'] + " "+i['surname'], 'year_group':i['year_group'] })

    for i in teachers_ten1:
        class_1= {
            'subject': random.choice(subjects),
            'students':students_ten1_year3,
            'teacher_id': i['_id'],
            'tenant_id':1,
            'day': random.choice(days),
            'period': random.randint(1,10),
            'teacher_name': i['first_name'] + " " + i['surname']
        }

        class_2= {
            'subject': random.choice(subjects),
            'students':students_ten1_year4,
            'teacher_id': i['_id'],
            'tenant_id':1,
            'day': random.choice(days),
            'period': random.randint(1,10),
            'teacher_name': i['first_name'] + " " + i['surname']
        }

        class_3= {
            'subject': random.choice(subjects),
            'students':students_ten1_year5,
            'teacher_id': i['_id'],
            'tenant_id':1,
            'day': random.choice(days),
            'period': random.randint(1,10),
            'teacher_name': i['first_name'] + " " + i['surname']
        }

        class_list = [class_1, class_2, class_3]
        classes.insert_many(class_list)

    for i in teachers_ten2:
        class_1= {
            'subject': random.choice(subjects),
            'students':students_ten2_year3,
            'teacher_id': i['_id'],
            'tenant_id':2,
            'day': random.choice(days),
            'period': random.randint(1,10),
            'teacher_name': i['first_name'] + " " + i['surname']
        }

        class_2= {
            'subject': random.choice(subjects),
            'students':students_ten2_year4,
            'teacher_id': i['_id'],
            'tenant_id':2,
            'day': random.choice(days),
            'period': random.randint(1,10),
            'teacher_name': i['first_name'] + " " + i['surname']
        }
        
        class_3= {
            'subject': random.choice(subjects),
            'students':students_ten2_year5,
            'teacher_id': i['_id'],
            'tenant_id':2,
            'day': random.choice(days),
            'period': random.randint(1,10),
            'teacher_name': i['first_name'] + " " + i['surname']
        }

        class_list = [class_1, class_2, class_3]
        classes.insert_many(class_list)

# Generates 2 assignments for the pre-generated classes for each tenant. 
# Data is saved to the assignment collection
def generate_assignments():

    for i in classes.find():
        i["_id"] = str(i["_id"])
        assignment_1 = {
            'title':'Assignment 1',
            'teacher_id':i['teacher_id'],
            'class_id': i['_id'],
            'created_date':'2022-01-01',
            'deadline':'2022-02-15',
            'tenant_id':i['tenant_id'],
            'filename':'',
            'filepath':''
        }
        assignment_2 = {
            'title':'Assignment 2',
            'teacher_id':i['teacher_id'],
            'class_id': i['_id'],
            'created_date':'2022-01-01',
            'deadline':'2022-02-15',
            'tenant_id':i['tenant_id'],
            'filename':'',
            'filepath':''
        }
        assignment_3 = {
            'title':'Assignment 3',
            'teacher_id':i['teacher_id'],
            'class_id': i['_id'],
            'created_date':'2022-03-01',
            'deadline':'2022-06-15',
            'tenant_id':i['tenant_id'],
            'filename':'',
            'filepath':''
        }
        assignment_4 = {
            'title':'Assignment 4',
            'teacher_id':i['teacher_id'],
            'class_id': i['_id'],
            'created_date':'2022-03-01',
            'deadline':'2022-06-15',
            'tenant_id':i['tenant_id'],
            'filename':'',
            'filepath':''
        }
        assignment_list = [assignment_1, assignment_2, assignment_3, assignment_4]
        assignment.insert_many(assignment_list)

# Generates submission data for the pre-generated assingments. 
# Data is stored in the submission collection
def generate_submissions():
    for i in student.find():
        i['_id'] = str(i['_id'])
        for j in classes.find({'students.id':i['_id']}):
            j['_id'] = str(j['_id'])
            for k in assignment.find({'class_id':j['_id']}):
                k['_id'] = str(k['_id'])
                if k['title'] == "Assignment 1":
                    sub = {
                        'student_id': i['_id'],
                        'firstname':i['first_name'],
                        'surname':i['surname'],
                        'assignment_id':k["_id"],
                        'title':k['title'], 
                        'class_id':j['_id'],
                        'mark':'70%',
                        'feedback':"Good work!",
                        'feedback_private':'',
                        'submission_date':'2022-02-02',
                        'filename':'',
                        'filepath':'',
                        'tenant_id':i['tenant_id'],
                        'marked':True
                    }
                    submission.insert_one(sub)
                if k['title'] == "Assignment 2":
                    sub = {
                        'student_id': i['_id'],
                        'firstname':i['first_name'],
                        'surname':i['surname'],
                        'assignment_id':k["_id"],
                        'title':k['title'], 
                        'class_id':j['_id'],
                        'mark':'50%',
                        'feedback':"Focus more on the text",
                        'feedback_private':i['first_name']+' is distracted in class',
                        'submission_date':'2022-02-10',
                        'filename':'',
                        'filepath':'',
                        'tenant_id':i['tenant_id'],
                        'marked':True
                    }
                    submission.insert_one(sub)