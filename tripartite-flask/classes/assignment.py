# Assignment
# An instance of an assisgment for a class. Data includes:
#   - title: The title
#   - teacher_id: ID of teacher who created the assignment
#   - class_id: The class' ID
#   - release_date: The date the assignment was created/released
#   - deadline: The due date/deadline
#   - tenant_id: The tenant ID
#
# Methods include the ability to update the title and deadline

class Assignment:
    def __init__(self, title, teacher_id, class_id, release_date, deadline, tenant_id):
        self.title = title
        self.teacher_id = teacher_id
        self.class_id = class_id
        self.release_date = release_date
        self.deadline = deadline
        self.tenant_id = tenant_id

    def update_title(self, title):
        self.title = title
    
    def update_deadline(self, deadline):
        self.deadline = deadline