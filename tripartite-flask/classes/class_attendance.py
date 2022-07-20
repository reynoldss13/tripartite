# ClassAttendance
# An instance of attendace which is stored in each student's
# Attendance record.  Data includes:
#   - class_id: The class ID
#   - date: The date
#   - teacher_id: The teacher ID
#   - presence: Whether the student was present/absent (0 = absent, 1 = present)
#
# Class method to update whether the student was absent/present

from datetime import date

class ClassAttendance:
    def __init__(self, class_id, teacher_id, presence):
        self.class_id = class_id
        self.date = date.today()
        self.teacher_id = teacher_id
        presence = presence

    def update_presence(self, presence):
        self.presence = presence