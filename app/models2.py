from app import db2, app2, login_manager2
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import JSONWebSignatureSerializer as Serializer
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column, and_, DateTime
from flask_login import UserMixin


@login_manager2.user_loader
def load_student(student_id):
    return Student.query.get(student_id)


class Student(db2.Model, UserMixin):
    __tablename__ = 'student'
    __table_args__ = (db2.PrimaryKeyConstraint('studid', name='student_pkey'),)
    studid = db2.Column(db2.CHAR(9), primary_key=True, nullable=False)
    studfirstname = db2.Column(db2.String(40), nullable=False)
    studmidname = db2.Column(db2.String(20))
    studlastname = db2.Column(db2.String(20), nullable=False)
    emailadd = db2.Column(db2.String(60))
    password = db2.Column(db2.String(60), nullable=False)
    image_file = db2.Column(db2.String(50), nullable=False,
                           default='default.jpg')

    def __init__(self, studid, studfirstname, studmidname, studlastname, emailadd, password, image_file):
        self.studid = studid
        self.studfirstname = studfirstname
        self.studmidname = studmidname
        self.studlastname = studlastname
        self.emailadd = emailadd
        self.password = password
        self.image_file = image_file

    def get_id(self):
        return self.studid

    def __repr__(self):
        return '<id {}>'.format(self.studid)


class College(db2.Model):
    __tablename__ = 'college'
    __table_args__ = (db2.PrimaryKeyConstraint('collcode', name='coll_pkey'),)
    collname = db2.Column(db2.String(70), nullable=False)
    collcode = db2.Column(db2.CHAR(4), nullable=False)

    def __init__(self, collname, collcode):
        self.collname = collname
        self.collcode = collcode

    def __repr__(self):
        return '<id {}>'.format(self.collcode)


class Department(db2.Model):
    __tablename__ = 'department'
    __table_args__ = (db2.PrimaryKeyConstraint('deptcode', name='dept_pkey'),
                      db2.ForeignKeyConstraint(['deptcoll'], ['college.collcode'], name='college_dept_fkey', onupdate="CASCADE", ondelete="RESTRICT"))
    deptcode = db2.Column(db2.CHAR(10), nullable=False, unique=True)
    deptname = db2.Column(db2.String(100), nullable=False)
    deptcoll = db2.Column(db2.CHAR(4), nullable=False)

    def __init__(self, deptcode, deptcoll, deptname):
        self.deptname = deptname
        self.deptcode = deptcode
        self.deptcoll = deptcoll

    def __repr__(self):
        return '<id {}>'.format(self.deptcode)


class Curriculum(db2.Model):
    __tablename__ = 'curriculum'
    __table_args__ = (db2.PrimaryKeyConstraint(
        'curriculum_id', name='curriculum_pk'),)

    curriculum_id = db2.Column(db2.CHAR(15), nullable=False)
    progcode = db2.Column(db2.CHAR(12), nullable=False)
    total_units = db2.Column(db2.Numeric(6, 2))

    def __init__(self, curriculum_id, progcode, total_units):
        self.progcode = progcode
        self.total_units = total_units
        self.curriculum_id = curriculum_id

    def __repr__(self):
        return '<id {}>'.format(self.curriculum_id)


class Program(db2.Model):
    __tablename__ = 'program'
    __table_args__ = (db2.PrimaryKeyConstraint('progcode', name='program_pk'),
                      db2.ForeignKeyConstraint(['progdept'], ['department.deptcode'], name='program_progdept_fkey', onupdate="CASCADE", ondelete="RESTRICT"),)
    progcode = db2.Column(db2.CHAR(12), nullable=False)
    progdesc = db2.Column(db2.String(100), nullable=False)
    progdept = db2.Column(db2.CHAR(10), nullable=False)

    def __init__(self, progdesc, progcode, progdept):
        self.progcode = progcode
        self.progdept = progdept
        self.progdesc = progdesc

    def __repr__(self):
        return '<id {}>'.format(self.progcode)


class CurriculumDetails(db2.Model):
    __tablename__ = 'curriculum_semsubject'
    __table_args__ = (db2.PrimaryKeyConstraint('curriculum_id', 'curriculum_year',
                                              'curriculum_sem', 'subjcode', name='curriculum_semsubject_pk'),)

    curriculum_id = db2.Column(db2.CHAR(15), nullable=False)
    curriculum_year = db2.Column(db2.Integer, nullable=False)
    curriculum_sem = db2.Column(db2.CHAR(1), nullable=False)
    subjcode = db2.Column(db2.CHAR(12), nullable=False)

    def __init__(self, curriculum_id, curriculum_year, curriculum_sem, subjcode):
        self.curriculum_id = curriculum_id
        self.curriculum_year = curriculum_year
        self.curriculum_sem = curriculum_sem
        self.subjcode = subjcode

    def __repr__(self):
        return '<id {}>'.format(self.curriculum_id)


class Subject(db2.Model):
    __tablename__ = 'subject'
    __table_args__ = (db2.PrimaryKeyConstraint(
        'subjcode', name='subject_pkey'),)
    subjcode = db2.Column(db2.CHAR(12), primary_key=True, nullable=False)
    subjdesc = db2.Column(db2.String(250), nullable=False)
    subjcredit = db2.Column(db2.Numeric(4, 2))

    # added
    subjdept = db2.Column(db2.CHAR(10), nullable=False)

    def __init__(self, subjcode, subjdesc, subjcredit, subjdept):
        self.subjcode = subjcode
        self.subjdesc = subjdesc
        self.subjcredit = subjcredit
        self.subjdept = subjdept

    def __repr__(self):
        return '<id {}>'.format(self.subjcode)


class Prerequisite(db2.Model):
    __tablename__ = 'prerequisite'
    __table_args__ = (db2.PrimaryKeyConstraint('subjcode', 'prereq', name='subjcode_prereq_pk'),)
    subjcode = db2.Column(db2.CHAR(12), nullable=False)
    prereq = db2.Column(db2.CHAR(12), nullable=False)

    def __init__(self, subjcode, prereq):
        self.subjcode = subjcode
        self.prereq = prereq

    def __repr__(self):
        return '<id {}>'.format(self.subjcode)


class SemesterStudent(db2.Model):
    __tablename__ = 'semstudent'
    __table_args__ = (db2.PrimaryKeyConstraint('sy', 'sem', 'studid', name='semstudent_pkey'),
                      db2.ForeignKeyConstraint(['studid'], ['student.studid'], name='semstudent_studid_fkey', onupdate="CASCADE", ondelete="RESTRICT"),)
    studid = db2.Column(db2.CHAR(9), nullable=False)
    sem = db2.Column(db2.CHAR(1), nullable=False)
    sy = db2.Column(db2.CHAR(9), nullable=False)
    studlevel = db2.Column(db2.SmallInteger)
    scholasticstatus = db2.Column(db2.String(20))
    scholarstatus = db2.Column(db2.String(12))
    studmajor = db2.Column(db2.CHAR(12))
    gpa = db2.Column(db2.Numeric(6, 5))
    cgpa = db2.Column(db2.Numeric(6, 5))

    def __init__(self, studid, sem, sy, studmajor, studlevel, scholasticstatus, scholarstatus, gpa, cgpa):
        self.studid = studid
        self.sem = sem
        self.sy = sy
        self.studmajor = studmajor
        self.studlevel = studlevel
        self.scholasticstatus = scholasticstatus
        self.scholarstatus = scholarstatus
        self.gpa = gpa
        self.cgpa = cgpa

    def __repr__(self):
        return '<id {}>'.format(self.studid)


class SemesterSubject(db2.Model):
    __tablename__ = 'semsubject'
    __table_args__ = (db2.PrimaryKeyConstraint('sy', 'sem', 'subjcode', 'section', name='semsubject_pkey'),
                      db2.ForeignKeyConstraint(['subjcode'], ['subject.subjcode'], name='semsubject_subject', onupdate="CASCADE", ondelete="RESTRICT"))

    sy = db2.Column(db2.CHAR(9), nullable=False)
    sem = db2.Column(db2.CHAR(1), nullable=False)
    subjcode = db2.Column(db2.CHAR(12), nullable=False)
    section = db2.Column(db2.CHAR(10), nullable=False)
    semsubject_id = db2.Column(db2.Integer, unique=True)

    def __init__(self, sy, sem, subjcode, section, semsubject_id):
        self.sy = sy
        self.sem = sem
        self.subjcode = subjcode
        self.section = section
        self.semsubject_id = semsubject_id

    def __repr__(self):
        return '<section {}>'.format(self.subjcode)


class Registration(db2.Model):
    __tablename__ = 'registration'
    __table_args__ = (db2.PrimaryKeyConstraint('sy', 'sem', 'studid', 'subjcode', name='registration_pkey'),
                      db2.ForeignKeyConstraint(['sy', 'sem', 'section', 'subjcode'], ['semsubject.sy', 'semsubject.sem', 'semsubject.section',
                                                                                     'semsubject.subjcode'], name='registration_semsubject', onupdate="CASCADE", ondelete="RESTRICT"),
                      db2.ForeignKeyConstraint(['studid', 'sem', 'sy'], ['semstudent.studid', 'semstudent.sem', 'semstudent.sy'], name='registration_semstudent', onupdate="CASCADE", ondelete="RESTRICT"),)

    studid = db2.Column(db2.CHAR(9), nullable=False)
    sem = db2.Column(db2.CHAR(1), nullable=False)
    sy = db2.Column(db2.CHAR(9), nullable=False)
    subjcode = db2.Column(db2.CHAR(12), nullable=False)
    grade = db2.Column(db2.String(8))
    section = db2.Column(db2.CHAR(10))

    def __init__(self, sem, sy, subjcode, grade, section, studid):
        self.sem = sem
        self.sy = sy
        self.subjcode = subjcode
        self.studid = studid
        self.grade = grade
        self.section = section

    def __repr__(self):
        return '<id {}>'.format(self.studid)

    @staticmethod
    def addConst():
        return db2.ForeignKeyConstraint(['studid', 'sem', 'sy'], ['semstudent.studid', 'semstudent.sem', 'semstudent.sy'], name='registration_semstudent', onupdate="CASCADE", ondelete="RESTRICT")


class Semester(db2.Model):
    __tablename__ = 'semester'
    __table_args__ = (db2.PrimaryKeyConstraint('sy', 'sem', name='sem_pkey'),)
    sy = db2.Column(db2.CHAR(9), nullable=False)
    sem = db2.Column(db2.CHAR(1), nullable=False)
    is_online_enrollment_up = db2.Column(db2.Boolean)

    def __init__(self, sy, sem, is_online_enrollment_up):
        self.sy = sy
        self.sem = sem
        self.is_online_enrollment_up = is_online_enrollment_up

    def __repr__(self):
        return '<up {}'.format(self.is_online_enrollment_up)
