from app import app, db, login_manager
from flask_login import UserMixin

class Students(db.Model):
    stud_id = db.Column(db.Integer, primary_key=True)
    stud_idNum = db.Column(db.String(9), nullable=False)
    stud_fullName = db.Column(db.String(200), nullable=False)
    stud_userName = db.Column(db.String(200), nullable=False)
    stud_degree = db.Column(db.String(10), nullable=False)
    stud_year = db.Column(db.Integer, default=1)
    stud_previousGpa = db.Column(db.Float, default=None)
    stud_cgpa = db.Column(db.Float, default=None)

    def __repr__(self):
        return "Students({}, {}, {}, {}, {}, {})".format(self.stud_idNum, self.stud_fullName, self.stud_degree, self.stud_year, self.stud_previousGpa, self.stud_cgpa)

class PreviousCourses(db.Model):
    prevcourse_id = db.Column(db.Integer, primary_key=True)
    # prevcourse_courseCode = db.Column(db.String(10), nullable=False) - foreign Key
    prevcourse_grade = db.Column(db.Float, default=None)

    def __repr__(self):
        return "PreviousCourses({}, {})".format(self.prevcourse_courseCode, self.prevcourse_grade)

class Courses(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    course_courseCode = db.Column(db.String(10), nullable=False)
    course_courseName = db.Column(db.String(150), nullable=False)
    course_department = db.Column(db.String(100), nullable=False)
    course_unit = db.Column(db.Integer, nullable=False)
    # course_pre_requisite = db.Column(db.Integer, nullable=True) - foreign Key
    # course_co_requisite = db.Column(db.Integer, nullable=True) - foreign Key



    def __repr__(self):
        return "Courses({}, {}, {})".format(self.course_courseCode, self.course_courseName, self.course_department)


class Degrees(db.Model):
    degree_id = db.Column(db.Integer, primary_key=True)
    degree_degreeCode = db.Column(db.String(15), nullable=False)
    degree_degreeName = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "Degrees({}, {})".format(self.degree_degreeCode, self.degree_degreeName)

# Another Table: Department
# 