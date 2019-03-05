from app import app, db, login_manager
from flask_login import UserMixin


class Students(db.Model):
    studId = db.Column(db.Integer, primary_key=True)
    idNum = db.Column(db.String(9), nullable=False)
    fullName = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    yearLevel = db.Column(db.Integer, default=1)
    userName = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # stud_degree = db.Column(db.String(10), nullable=False)  - foreign key sa Degree

    def __repr__(self):
        return "Students({}, {}, {}, {}, {}, {})".format(self.idNum, self.fullName, self.gender, self.yearLevel, self.userName, self.password)


class Degrees(db.Model):
    degreeId = db.Column(db.Integer, primary_key=True)
    degreeCode = db.Column(db.String(15), nullable=False)
    degreeName = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "Degrees({}, {})".format(self.degreeCode, self.degreeName)


class Departments(db.Model):
    departmentId = db.Column(db.Integer, primary_key=True)
    deptCode = db.Column(db.String(100), nullable=False)
    deptName = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return "Departments({}, {})".format(self.deptCode, self.deptName)


class CourseOfStudies(db.Model):
    courseOfStudyId = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "CourseOfStudies({})".format(self.semester)


class Courses(db.Model):
    courseId = db.Column(db.Integer, primary_key=True)
    courseCode = db.Column(db.String(10), nullable=False)
    courseTitle = db.Column(db.String(150), nullable=False)
    units = db.Column(db.Integer, nullable=False)
    preRequisite = db.Column(db.Integer, nullable=True)
    coRequisite = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return "Courses({}, {}, {}, {}, {})".format(self.courseCode, self.courseTitle, self.units, self.preRequisite, self.coRequisite)


class AcademicPerformances(db.Model):
    academicPerformanceId = db.Column(db.Integer, primary_key=True)
    gpa = db.Column(db.Float, default=None)
    cgpa = db.Column(db.Float, default=None)
    residency = db.Column(db.Integer, default=None)
    remainingSems = db.Column(db.Integer, default=None)

    def __repr__(self):
        return "AcademicPerformances({}, {}, {}, {})".format(self.gpa, self.cgpa, self.residency, self.remainingSems)

class PreviousCourses(db.Model):
    prevcourseId = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Float, default=None)
    status = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return "PreviousCourses({}, {})".format(self.grade, self.status)