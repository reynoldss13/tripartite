# AttendanceRecord
# An record of a student's attendance per academic year.
# Data includes:
#   - student_id: The student ID
#   - academic_year: The academic year
#   - tenant_id: Tenant ID
#   - attendance_list: A list of each attedance instance, recording the student's
#     student's presence or absence
#
# Note: each record in the attendance list is an instance of the
# ClassAttendance class

class AttendanceRecords:

    def __init__(self, student_id, academic_year, tenant_id):
        self.student_id = student_id
        self.academic_year = academic_year
        self.attendance_list = []
        self._tenant_id = tenant_id

    def get_attendance_list(self):
        return self.attendance_list
