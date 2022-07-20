# ClassGroup
# This represents an instance of a class. Relevant data includes:
#   - class_id: the class' ID
#   - subject: The subject
#   - teacher_id: The teacher's ID
#   - tenant_id: The tenant ID
#   - students: A list of ID's of all students in the class
#
# Methods include the ability to get & update the students in the class
# and change the teacher

class ClassGroup:
    def __init__(self, class_id, subject, teacher_id, tenant_id):
        self.class_id = class_id
        self.subject = subject
        self.students = []
        self.teacher_id = teacher_id
        self.tenant_id = tenant_id

    def get_class_students(self):
        return self.students

    def update_class_students(self, students):
        self.students = students

    def update_teacher(self, teacher_id):
        self.tenant_id = teacher_id
