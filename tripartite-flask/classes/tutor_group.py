# TutorGroup
# This represents an instance of a tutorial class. Relevant data includes:
#   - class_id: The tutor group's ID
#   - tutor_id : The tutor's ID
#   - tenant_id: The tenant ID
#   - students: A list of ID's of all students in the group
#
# Methods include the ability to get & update the students in the group
# and change the teacher

class TutorGroup:
    def __init__(self, class_id, tutor_id, tenant_id):
        self.class_id = class_id
        self.students = []
        self.tutor_id = tutor_id
        self.tenant_id = tenant_id

    def get_class_students(self):
        return self.students

    def update_class_students(self, students):
        self.students = students

    def update_teacher(self, tutor_id):
        self.tutor_id = tutor_id
