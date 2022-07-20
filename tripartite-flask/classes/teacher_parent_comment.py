# TeacherParentComment
# A instance of a comment that teachers can create
# which is only viewable by the parent/guardian of the 
# associated student ID. Relevant data includes:
#   - teacher_id: the ID of the teacher creating the comment
#   - student_id: the ID of the student to whom the comment relates
#   - date: the date of the comment's creation
#   - comment_body: the text that makes up the body of the comment
#   - tenant_id: the tenant's ID
#
# Methods include the ability to update the comment's body and
# student ID


from datetime import date

class TeacherParentComment:

    def __init__(self, teacher_id, student_id, comment_body, tenant_id):
        self.teacher_id = teacher_id
        self.student_id = student_id
        self.date = date.today()
        self.comment_body = comment_body
        self.tenant_id = tenant_id

    def update_comment(self, comment_body):
        self.comment_body = comment_body

    def update_student_id(self, student_id):
        self.student_id = student_id