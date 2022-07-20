# Generates dummy data for user types, tenants, teachers, parents & students
# Login credentials generated here will be used for demonstration purposes
import random
import bcrypt
from bson import ObjectId
from pymongo import MongoClient
import faker
import datetime

# MongoDB client and collections
mongo_client = MongoClient(" ")
db = mongo_client.projectDB
student = db.student
teacher = db.teacher
parent = db.parent
tenant = db.tenant
user_type = db.usertype

FIRST_NAMES = ["Brian", "Stephen", "George", "Sean", "Timothy", "Francis", "Frances", "Robert","Susan", \
    "Catherine", "Pauline", "Andrew", "Seamus", "Ian", "Ellen", "Michael", "Paul", "Lina", "Oliver", "Noah", \
        "Benjamin", "Liam", "Eoin", "Emma", "Amelia", "Sophie", "Bruce", "Charlotte", "Olivia", "Katie", "Mia", \
            "Brendan", "Isaac"]
SURNAMES = ["Reynolds", "Hamill", "Simpson", "Harris", "Connery", "Smalls", "Grey", \
     "Fitzgerald", "Kennedy", "Smith", "Jones", "Williams", "Romero", "Hall", "Sullivan", "Flanagan", "Cahill", \
         "Keavy", "Taylor"]
TOWNS = ["Belfast", "Lisburn", "Derry", "Armagh", "Newry", "Antrim", "Enniskillen", "Bangor", "Newtonabbey", "Ballymena"]

# Generates the user types used in the app and inserts them
# into the usertype collection
def generate_user_types():
    roles = ["student","teacher","parent","admin"]
    index = 0
    for i in roles:
        user_type.insert_one({'u_id':index, 'usertype':i})
        index = index + 1

# Generates 2 tenants and inserts them into the tenant collection
def generate_tenants():
    tenant_1 = {
        'tenant_id':1,
        'tenant_name':'Tenant 1 Highschool',
        'phone':'02890111111',
        'address':'123 Belfast Street',
        'postcode':'BT1 111',
        'city':'Belfast',
        'country':'Northern Ireland',
        'headmaster':'Mr H. Master'
    }
    tenant_2 = {
        'tenant_id':2,
        'tenant_name':'Tenant 2 College',
        'phone':'02890222222',
        'address':'321 Fake Avenue',
        'postcode':'BT2 222',
        'city':'Belfast',
        'country':'Northern Ireland',
        'headmaster':'Mrs H. Teacher'
    }
    tenants = [tenant_1, tenant_2]
    tenant.insert_many(tenants)

# Generates 2 teachers, 1 for each tenant, and inserts them into the
# teacher collection
def generate_teachers():

    password = 'password'.encode('utf-8')        

    teacher_1_1 = {
        'first_name':'Hank',
        'surname':'Pym',
        'DOB':'1980-01-06',
        'email':'hankpym@gmail.com',
        'password': bcrypt.hashpw(password, bcrypt.gensalt()),
        'user_type':1,
        'phone':'02890123456',
        'address':'22 Acacia Avenue',
        'postcode':'BT1 A1A',
        'city':'Lisburn',
        'country':'Northern Ireland',
        'verified': True,
        'tenant_id':1
    }
    teacher_1_2 = {
        'first_name':'Bruce',
        'surname':'Banner',
        'DOB':'1980-01-06',
        'email':'brucebanner@gmail.com',
        'password': bcrypt.hashpw(password, bcrypt.gensalt()),
        'user_type':1,
        'phone':'02890123456',
        'address':'27 Jocelyn Avenue',
        'postcode':'BT3 C1A',
        'city':'Portadown',
        'country':'Northern Ireland',
        'verified': True,
        'tenant_id':1
    }
    teacher_2_1 = {
        'first_name':'Peter',
        'surname':'Parker',
        'DOB':'1994-05-07',
        'email':'peterparker@gmail.com',
        'password': bcrypt.hashpw(password, bcrypt.gensalt()),
        'user_type':1,
        'phone':'02890654321',
        'address':'461 Ocean Boulevard',
        'postcode':'BT2 B2B',
        'city':'Derry',
        'country':'Northern Ireland',
        'verified': True,
        'tenant_id':2
    }
    teacher_2_2 = {
        'first_name':'Susan',
        'surname':'Storm',
        'DOB':'1990-05-07',
        'email':'suestorm@gmail.com',
        'password': bcrypt.hashpw(password, bcrypt.gensalt()),
        'user_type':1,
        'phone':'02890654321',
        'address':'45 Manse Road',
        'postcode':'BT8 829',
        'city':'Belfast',
        'country':'Northern Ireland',
        'verified': True,
        'tenant_id':2
    }
    teachers = [teacher_1_1,teacher_1_2,teacher_2_1,teacher_2_2]
    teacher.insert_many(teachers)

# Generate Students & Parents, 1 for each tenant, related to each other
# which are inserted into the parent and student collections.
def generate_parent_student():
    password = 'password'.encode('utf-8') 

    student_1_1 = {
        'first_name':'Christopher',
        'surname':'Griffin',
        'middle_name':'James',
        'DOB':'2007-03-03',
        'email':'cgriffin@tenantone.ac.uk',
        'password':bcrypt.hashpw(password, bcrypt.gensalt()),
        'user_type':0,
        'address':'15 Spooner Street',
        'postcode':'BT7 616',
        'city':'Belfast',
        'country':'Northern Ireland',
        'guardians': [],
        'enrolled_date':'2018-09-01',
        'year_group': 4,
        'tenant_id':1
    }
    student_1_2 = {
        'first_name':'Meg',
        'surname':'Griffin',
        'middle_name':'Lois',
        'DOB':'2009-03-03',
        'email':'mlgriffin@tenantone.ac.uk',
        'password':bcrypt.hashpw(password, bcrypt.gensalt()),
        'user_type':0,
        'address':'15 Spooner Street',
        'postcode':'BT7 616',
        'city':'Belfast',
        'country':'Northern Ireland',
        'guardians': [],
        'enrolled_date':'2018-09-01',
        'year_group': 4,
        'tenant_id':1
    }
    parent_1_1 = {
        'first_name':'Peter',
        'surname':'Griffin',
        'DOB':'1982-05-01',
        'registered_students':[],
        'email':'pgriffin@gmail.com',
        'password':bcrypt.hashpw(password, bcrypt.gensalt()),
        'user_type':2,
        'phone':'02890545454',
        'address':'15 Spooner Street',
        'postcode':'BT7 616',
        'city':'Belfast',
        'country':'Northern Ireland',
        'verified':True,
        'tenant_id':1
    }
    student_2_1 = {
        'first_name':'Lucy',
        'surname':'Jones',
        'middle_name':'Amy',
        'DOB':'2007-04-01',
        'email':'ljones@tenanttwo.ac.uk',
        'password':bcrypt.hashpw(password, bcrypt.gensalt()),
        'user_type':0,
        'address':'66 Street Road',
        'postcode':'BT2 1FF',
        'city':'Belfast',
        'country':'Northern Ireland',
        'guardians': [],
        'enrolled_date':'2018-09-01',
        'year_group': 4,
        'tenant_id':2
    }
    parent_2_1 = {
        'first_name':'Mary',
        'surname':'Jones',
        'DOB':'1982-05-01',
        'registered_students':[],
        'email':'mjones@gmail.com',
        'password':bcrypt.hashpw(password, bcrypt.gensalt()),
        'user_type':2,
        'phone':'02890666666',
        'address':'66 Street Road',
        'postcode':'BT2 1FF',
        'city':'Belfast',
        'country':'Northern Ireland',
        'verified':True,
        'tenant_id':2
    }
    student_list = [student_1_1, student_1_2, student_2_1]
    parent_list = [parent_1_1, parent_2_1]
    student.insert_many(student_list)
    parent.insert_many(parent_list)

    P1_children = []
    P2_children = []
    P1 = parent.find_one({'surname':'Griffin'})
    P1['_id'] = str(P1['_id'])
    P2 = parent.find_one({'surname':'Jones'})
    P2['_id'] = str(P2['_id'])
    for i in student.find():
        s_id = str(i['_id'])
        if i['surname'] == 'Griffin':
            student.update_one({'_id':ObjectId(s_id)},{'$set':{
                'guardians': [P1['_id']]
            }})
            P1_children.append(s_id)
        else:
            student.update_one({'_id':ObjectId(s_id)},{'$set':{
                'guardians': [P2['_id']]
            }})
            P2_children.append(s_id)
    parent.update_one({'_id':ObjectId(P1['_id'])},{'$set':{
        'registered_students':P1_children
    }})
    parent.update_one({'_id':ObjectId(P2['_id'])},{'$set':{
        'registered_students':P2_children
    }})

def generate_random_students():
    streets = ['Avenue', "Street", "Close", "Way", "Drive", "Gardens", "Manse"]
    for i in tenant.find():
        email_tail = ""
        if i['tenant_id'] == 1:
            email_tail = '@tenantone.ac.uk'
        else:
            email_tail = '@tenanttwo.ac.uk'

        for j in range(100):
            password = 'password'.encode('utf-8')
            birth_year = random.randint(2005,2012) 
            enrolled_year = random.randint(2015, 2021)
            current_year = int(datetime.datetime.now().year)
            year_group = current_year - enrolled_year
            firstname = random.choice(FIRST_NAMES)
            surname = random.choice(SURNAMES)
            email = firstname[0].lower() + surname.lower() + email_tail

            stdnt = {
                'first_name':firstname,
                'surname':surname,
                'middle_name':random.choice(FIRST_NAMES),
                'DOB': str(birth_year)+'-03-03',
                'email':email,
                'password':bcrypt.hashpw(password, bcrypt.gensalt()),
                'user_type':0,
                'address':str(random.randint(1,10)) + " " + random.choice(SURNAMES) + " " + random.choice(streets),
                'postcode':'BT' + str(random.randint(1,10)) +" "+ str(random.randint(100,999)),
                'city':random.choice(TOWNS),
                'country':'Northern Ireland',
                'guardians': [],
                'enrolled_date':str(enrolled_year) + '-09-01',
                'year_group': int(year_group),
                'tenant_id':i['tenant_id']
            }
            student.insert_one(stdnt)