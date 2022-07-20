# AssignmentResults
# An instance of results for a student, relating to a particular
# assignment. Relevant data:
#   - student_id: The student's ID
#   - assignment_id: The ID of the assignment
#   - date_submitted: Date work was submitted
#   - result: the mark or grade for the assignment
#   - feedback_student: Feedback for the student
#   - feedback_parent: An optional field, only viewable by parent
#     should the teacher wish to raise any points with the parent/guardian
#
# Methods include the ability to update the mark and feedback for students and parents

class AssignmentResults:
    def __init__(self, student_id, assignment_id, date_submitted, result, feedback_student, feedback_parent):
        self.student_id = student_id
        self.assignment_id = assignment_id
        self.date_submitted = date_submitted
        self.result = result
        self.feedback_student = feedback_student
        self.feedback_parent =  feedback_parent

    def update_result(self, result):
        self.result = result

    def update_feedback_student(self, feedback_student):
        self.feedback_student = feedback_student

    def updated_feedback_parent(self, feedback_parent):
        self.feedback_parent = feedback_parent
