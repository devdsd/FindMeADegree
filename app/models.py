from app import app, db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_student(student_id):
    return Students.query.get(int(student_id))

student_to_degree_rel_table = db.Table('student_to_degree_rel_table',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('degree_id', db.Integer, db.ForeignKey('degrees.id'))
)

class Students(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    idNum = db.Column(db.String(9), nullable=False, unique=True)
    firstName = db.Column(db.String(100), nullable=False)
    middleName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    userName = db.Column(db.String(200), unique=True, nullable=False)   
    emailAddress = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(30), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    academic_performance = db.relationship('AcademicPerformances', backref='acadhistory', lazy=True)
    can_shift = db.relationship('Degrees', secondary=student_to_degree_rel_table, backref=db.backref('degreeforshifters', lazy=True))


    def __repr__(self):
        return "Students({}, {}, {}, {}, {}, {}, {}, {})".format(self.idNum, self.firstName, self.middleName, self.lastName, self.gender, self.userName, self.emailAddress)


class AcademicPerformances(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentMajor = db.Column(db.String(100), nullable=False)
    studentYearLevel = db.Column(db.String(100), nullable=False)
    scholasticStatus = db.Column(db.String(100), nullable=False)
    schoolYear = db.Column(db.String(50), nullable=False)
    gpa = db.Column(db.Float, default=None)
    cgpa = db.Column(db.Float, default=None)
    residency = db.Column(db.Integer, default=None)
    remainingSems = db.Column(db.Integer, default=None)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    previous_course = db.relationship('PreviousCourses', backref='prevsubject', lazy=True)

    def __repr__(self):
        return "AcademicPerformances({}, {}, {}, {}, {}, {}, {}, {})".format(self.studentMajor, self.studentYearLevel, self.scholasticStatus, self.schoolYear, self.gpa, self.cgpa, self.residency, self.remainingSems)


class PreviousCourses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Float, default=None)
    status = db.Column(db.String(10), nullable=False)
    acadperformance_id = db.Column(db.Integer, db.ForeignKey('academic_performances.id'), nullable=False)
    courseofstudy_id = db.Column(db.Integer, db.ForeignKey('course_of_studies.id'), nullable=False)

    def __repr__(self):
        return "PreviousCourses({}, {})".format(self.grade, self.status)


class CourseOfStudies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.String(100), nullable=False)
    courses = db.relationship('Courses', backref='listofcourses', lazy=True)
    degree = db.relationship('Degrees', backref='degreeprogram', lazy=True, uselist=False)
    prev_courses = db.relationship('PreviousCourses', backref='listofpreviouscourses', lazy=True)
    

    def __repr__(self):
        return "CourseOfStudies({})".format(self.semester)


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courseCode = db.Column(db.String(10), nullable=False)
    courseTitle = db.Column(db.String(150), nullable=False)
    deptName = db.Column(db.String(300), nullable=False)
    units = db.Column(db.Integer, nullable=False)
    preRequisite = db.Column(db.Integer, nullable=True)
    coRequisite = db.Column(db.Integer, nullable=True)
    courseofstudy_id = db.Column(db.Integer, db.ForeignKey('course_of_studies.id'), nullable=False)

    def __repr__(self):
        return "Courses({}, {}, {}, {}, {})".format(self.courseCode, self.courseTitle, self.units, self.preRequisite, self.coRequisite)


class Colleges(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    collegeCode = db.Column(db.String(20), nullable=False)
    collegeName = db.Column(db.String(100), nullable=False)
    department = db.relationship('Departments', backref='department', lazy=True)

    def __repr__(self):
        return "College({}, {})".format(self.collegeCode, self.collegeName)


class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deptCode = db.Column(db.String(100), nullable=False)
    deptName = db.Column(db.String(300), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    degree_relationship = db.relationship('Degrees', backref='degree', lazy=True)

    def __repr__(self):
        return "Departments({}, {})".format(self.deptCode, self.deptName)


class Degrees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degreeCode = db.Column(db.String(15), nullable=False)
    degreeName = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), unique=True, nullable=False)
    courseofstudy_id = db.Column(db.Integer, db.ForeignKey('course_of_studies.id'), nullable=False)

    def __repr__(self):
        return "Degrees({}, {})".format(self.degreeCode, self.degreeName)