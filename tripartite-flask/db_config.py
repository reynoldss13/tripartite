from pymongo import MongoClient
import os

# MongoDB - establishing client and document connections
# Was set to private mongoDB
mongo_client = MongoClient(" ")
db = mongo_client.projectDB
student = db.student
teacher = db.teacher
parent = db.parent
tenant = db.tenant
user_type = db.usertype
tutorialgroup = db.tutorgroup
classes = db.classes
subject = db.subject
assignment = db.assignment
submission = db.submission
attendance_record = db.attendancerecord
attendance_instance = db.attendanceinstance
tpcomment = db.teacherparentcomment

# Establishing the connection to the backup database
db_backup = mongo_client.projectDB_backup
student_backup = db.student
teacher_backup = db.teacher
parent_backup = db.parent
tenant_backup = db.tenant
user_type_backup = db.usertype
tutorialgroup_backup = db.tutorgroup
classes_backup = db.classes
subject_backup = db.subject
assignment_backup = db.assignment
submission_backup = db.submission
attendance_record_backup = db.attendancerecord
attendance_instance_backup = db.attendanceinstance
tpcomment_backup = db.teacherparentcomment


# Function to perform a back up of the DB.  Because the DB
# is currently stored locally, this is achieved using os.system
# to run mongoexport, which stores JSON files of the collections
# in a backup file found in the current directory. 
#  
# This copy is then imported to the current backup 'db_backup'
def db_backup():
    # Creation of the JSON files
    os.system('mongoexport -d projectDB -c student -o backup/Student.json --jsonArray')
    os.system('mongoexport -d projectDB -c teacher -o backup/Teacher.json --jsonArray')
    os.system('mongoexport -d projectDB -c parent -o backup/Parent.json --jsonArray')
    os.system('mongoexport -d projectDB -c tenant -o backup/Tenant.json --jsonArray')
    os.system('mongoexport -d projectDB -c usertype -o backup/UserType.json --jsonArray')
    os.system('mongoexport -d projectDB -c tutorgroup -o backup/TutorGroup.json --jsonArray')
    os.system('mongoexport -d projectDB -c classes -o backup/Classes.json --jsonArray')
    os.system('mongoexport -d projectDB -c subject -o backup/Subject.json --jsonArray')
    os.system('mongoexport -d projectDB -c assignment -o backup/Assignment.json --jsonArray')
    os.system('mongoexport -d projectDB -c submission -o backup/Submission.json --jsonArray')
    os.system('mongoexport -d projectDB -c attendancerecords -o backup/AttendanceRecords.json --jsonArray')
    os.system('mongoexport -d projectDB -c attendanceinstance -o backup/AttendanceInstance.json --jsonArray')
    os.system('mongoexport -d projectDB -c teacherparentcomment -o backup/TeacherParentComment.json --jsonArray')

    # Importing the JSON files into the projectDB_backup document
    os.system('mongoimport --db projectDB_backup --collection student --file backup/Student.json --jsonArray')
    os.system('mongoimport --db projectDB_backup --collection teacher --file backup/Teacher.json --jsonArray')
    os.system('mongoimport --db projectDB_backup --collection parent --file backup/Parent.json --jsonArray')
    os.system('mongoimport --db projectDB_backup --collection tenant --file backup/Tenant.json --jsonArray')
    os.system('mongoimport --db projectDB_backup --collection usertype --file backup/UserType.json --jsonArray')
    os.system('mongoimport --db projectDB_backup --collection tutorgroup --file backup/TutorGroup.json --jsonArray')
    os.system('mongoimport --db projectDB_backup --collection classes --file backup/Classes.json --jsonArray')
    os.system('mongoimport --db projectDB_backup --collection subject --file backup/Subject.json --jsonArray')
    os.system('mongoimport --db projectDB_backup --collection assignment --file backup/Assignment.json --jsonArray')
    os.system('mongoimport --db projectDB_backup --collection submission --file backup/Submission.json --jsonArray')
    os.system('mongoimport --db projectDB_backup --collection attendancerecords --file backup/AttendanceRecords.json --jsonArray')
    os.system('mongoimport --db projectDB_backup --collection attendanceinstance --file backup/AttendanceInstance.json --jsonArray')
    os.system('mongoimport --db projectDB_backup --collection teacherparentcomment --file backup/TeacherParentComment.json --jsonArray')



