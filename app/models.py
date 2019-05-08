from app import db, app, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import JSONWebSignatureSerializer as Serializer
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column, and_, DateTime
from flask_login import UserMixin
# from flask_login import AnonymousUserMixin


# class Anonymous(AnonymousUserMixin):
# 	def __init__(self):
# 		self.username = 'Guest'

# 	def isAuthenticated(Self):
# 		return False

# 	def is_active(self):
# 		return False

# 	def is_anonymous(self):
# 		return True

@login_manager.user_loader	
def load_student(student_id):
	return Student.query.get(student_id)


class Student(db.Model, UserMixin):
	__tablename__ = 'student'
	__table_args__ = (db.PrimaryKeyConstraint('studid', name='student_pkey'),)
	studid = db.Column(db.CHAR(9), primary_key=True, nullable=False)
	studfirstname = db.Column(db.String(40), nullable=False)
	studmidname = db.Column(db.String(20))
	studlastname = db.Column(db.String(20), nullable=False)
	emailadd = db.Column(db.String(60))
	password = db.Column(db.String(60), nullable=False)
	image_file = db.Column(db.String(50), nullable=False, default='default.jpg')

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


class College(db.Model):
	__tablename__ = 'college'
	__table_args__ = (db.PrimaryKeyConstraint('collcode', name='coll_pkey'),)
	collname = db.Column(db.String(70), nullable=False)
	collcode = db.Column(db.CHAR(4), nullable=False)

	def __init__(self, collname, collcode):
		self.collname = collname
		self.collcode = collcode

	def __repr__(self):
		return '<id {}>'.format(self.collcode)


class Department(db.Model):
	__tablename__ = 'department'
	__table_args__ = (db.PrimaryKeyConstraint('deptcode', name='dept_pkey'),
		db.ForeignKeyConstraint(['deptcoll'], ['college.collcode'], name='college_dept_fkey', onupdate="CASCADE", ondelete="RESTRICT"))
	deptcode = db.Column(db.CHAR(10), nullable=False, unique=True)
	deptname = db.Column(db.String(100), nullable=False)
	deptcoll = db.Column(db.CHAR(4), nullable=False)

	def __init__(self, deptcode, deptcoll, deptname):
		self.deptname = deptname
		self.deptcode = deptcode
		self.deptcoll = deptcoll

	def __repr__(self):
		return '<id {}>'.format(self.deptcode)


class Curriculum(db.Model):
	__tablename__ = 'curriculum'
	__table_args__ = (db.PrimaryKeyConstraint('curriculum_id', name='curriculum_pk'),)

	curriculum_id = db.Column(db.CHAR(15), nullable=False)
	progcode = db.Column(db.CHAR(12), nullable=False)
	total_units = db.Column(db.Numeric(6,2))

	def __init__(self, curriculum_id, progcode, total_units):
		self.progcode = progcode
		self.total_units = total_units
		self.curriculum_id = curriculum_id

	def __repr__(self):
		return '<id {}>'.format(self.curriculum_id)

class Program(db.Model):
	__tablename__ = 'program'
	__table_args__ = (db.PrimaryKeyConstraint('progcode', name='program_pk'),
		db.ForeignKeyConstraint(['progdept'], ['department.deptcode'], name='program_progdept_fkey', onupdate="CASCADE", ondelete="RESTRICT"),)
	progcode = db.Column (db.CHAR(12), nullable=False)
  	progdesc = db.Column(db.String(100), nullable=False)
  	progdept = db.Column (db.CHAR(10), nullable=False)

  	def __init__(self, progdesc, progcode, progdept):
		self.progcode = progcode
		self.progdept = progdept
		self.progdesc = progdesc

	def __repr__(self):
		return '<id {}>'.format(self.progcode)

class CurriculumDetails(db.Model):
	__tablename__ = 'curriculum_semsubject'
	__table_args__ = (db.PrimaryKeyConstraint('curriculum_id','curriculum_year','curriculum_sem','subjcode', name='curriculum_semsubject_pk'),)

	curriculum_id = db.Column(db.CHAR(15), nullable=False)
	curriculum_year = db.Column(db.Integer, nullable=False)
	curriculum_sem = db.Column(db.CHAR(1), nullable=False)
	subjcode = db.Column(db.CHAR(12), nullable=False)

	def __init__(self, curriculum_id, curriculum_year, curriculum_sem, subjcode):
		self.curriculum_id = curriculum_id
		self.curriculum_year = curriculum_year
		self.curriculum_sem = curriculum_sem
		self.subjcode = subjcode

	def __repr__(self):
		return '<id {}>'.format(self.curriculum_id)
 

class Subject(db.Model):
	__tablename__ = 'subject'
	__table_args__ = (db.PrimaryKeyConstraint('subjcode', name='subject_pkey'),)
	subjcode = db.Column(db.CHAR(12), primary_key=True, nullable=False)
	subjdesc = db.Column(db.String(250), nullable=False)
	subjcredit = db.Column(db.Numeric(4,2))

	#added
	subjdept = db.Column(db.CHAR(10), nullable=False)

	def __init__(self, subjcode, subjdesc, subjcredit, subjdept):
		self.subjcode = subjcode
		self.subjdesc = subjdesc
		self.subjcredit = subjcredit
		self.subjdept = subjdept

	def __repr__(self):
		return '<id {}>'.format(self.subjcode)

class Prerequisite(db.Model):
	__tablename__ = 'prerequisite'
	__table_args__ = (db.PrimaryKeyConstraint('subjcode', name='subjcode_pk'),)
	subjcode = db.Column(db.CHAR(12), nullable=False)
	prereq = db.Column(db.CHAR(12), nullable=False)

	def __init__(self, subjcode, prereq):
		self.subjcode = subjcode
		self.prereq = prereq

	def __repr__(self):
		return '<id {}>'.format(self.subjcode)


class SemesterStudent(db.Model):
	__tablename__ = 'semstudent'
	__table_args__ = (db.PrimaryKeyConstraint('sy','sem','studid', name='semstudent_pkey'),
						db.ForeignKeyConstraint(['studid'], ['student.studid'], name='semstudent_studid_fkey', onupdate="CASCADE", ondelete="RESTRICT"),)
	studid = db.Column(db.CHAR(9), nullable=False)
	sem = db.Column(db.CHAR(1), nullable=False)
	sy = db.Column(db.CHAR(9), nullable=False)
	studlevel = db.Column(db.SmallInteger)
	scholasticstatus = db.Column(db.String(20))
	scholarstatus = db.Column(db.String(12))
	studmajor = db.Column(db.CHAR(12))
	gpa = db.Column(db.Numeric(6,5))
	cgpa = db.Column(db.Numeric(6,5))

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


class SemesterSubject(db.Model):
	__tablename__ = 'semsubject'
	__table_args__ = (db.PrimaryKeyConstraint('sy','sem','subjcode', name='semsubject_pkey'),
						db.ForeignKeyConstraint(['subjcode'],['subject.subjcode'], name='semsubject_subject', onupdate="CASCADE", ondelete="RESTRICT"))

	sy = db.Column(db.CHAR(9), nullable=False)	
	sem = db.Column(db.CHAR(1), nullable=False)
	subjcode = db.Column(db.CHAR(12), nullable=False)
	semsubject_id = db.Column(db.Integer, unique=True)
	# forcoll = db.Column(db.String(12))
	# fordept = db.Column(db.String(20))
	# subjsecno = db.Column(db.SMALLINT)
	#added
	# maxstud = db.Column(db.Integer)
	# section = db.Column(db.CHAR(10), nullable=False)

	def __init__(self, sy, sem, subjcode, semsubject_id):
		self.sy = sy
		self.sem = sem
		self.subjcode = subjcode
		self.semsubject_id = semsubject_id
		# self.maxstud = maxstud		
		# self.forcoll = forcoll
		# self.fordept = fordept
		# self.subjsecno = subjsecno
		# self.section = section


	def __repr__(self):
		return '<section {}>'.format(self.subjcode)


class Registration(db.Model):
	__tablename__ = 'registration'
	__table_args__ = (db.PrimaryKeyConstraint('sy','sem','studid', 'subjcode', name='registration_pkey'),
					  db.ForeignKeyConstraint(['sy','sem', 'subjcode'], ['semsubject.sy','semsubject.sem','semsubject.subjcode'], name='registration_semsubject', onupdate="CASCADE", ondelete="RESTRICT"),
					  db.ForeignKeyConstraint(['studid','sem','sy'], ['semstudent.studid', 'semstudent.sem', 'semstudent.sy'], name='registration_semstudent', onupdate="CASCADE", ondelete="RESTRICT"),)

	studid = db.Column(db.CHAR(9), nullable=False)
	sem = db.Column(db.CHAR(1), nullable=False)
	sy = db.Column(db.CHAR(9), nullable=False)
	subjcode = db.Column(db.CHAR(12), nullable=False)
	grade = db.Column(db.String(8))
	section = db.Column(db.CHAR(10))
	gcompl = db.Column(db.String(8))

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
		return db.ForeignKeyConstraint(['studid','sem','sy'], ['semstudent.studid','semstudent.sem','semstudent.sy'], name='registration_semstudent', onupdate="CASCADE", ondelete="RESTRICT")


class Semester(db.Model):
	__tablename__ = 'semester'
	__table_args__ = (db.PrimaryKeyConstraint('sy','sem', name='sem_pkey'),)
	sy = db.Column(db.CHAR(9), nullable=False)
	sem = db.Column(db.CHAR(1), nullable=False)
	is_online_enrollment_up = db.Column(db.Boolean)

	def __init__(self, sy, sem, is_online_enrollment_up):
		self.sy = sy
		self.sem = sem
		self.is_online_enrollment_up = is_online_enrollment_up

	def __repr__(self):
		return '<up {}'.format(self.is_online_enrollment_up)




# class SemesterSubjectSchedule(db.Model):
# 	__tablename__ = 'semsubject_schedule'
# 	__table_args__ = (db.PrimaryKeyConstraint('schedule_id', name='semsubject_schedule_pk'),
# 						db.ForeignKeyConstraint(['semsubject_id'],['semsubject.semsubject_id'], name='semsubject_schedule_semsubject_fk', onupdate="CASCADE", ondelete="CASCADE"))
# 	schedule_id = db.Column(db.Integer, nullable=False)
# 	semsubject_id = db.Column(db.BigInteger, nullable=False)
# 	days = db.Column(db.CHAR(7))
# 	starttime = db.Column(db.Time)
# 	endtime = db.Column(db.Time)
# 	roomno  = db.Column(db.CHAR(12))

# 	def __init__(self, semsubject_id, schedule_id, days, starttime, endtime, roomno):
# 		self.schedule_id = schedule_id
# 		self.days = days
# 		self.starttime = starttime
# 		self.endtime = endtime
# 		self.roomno = roomno		
# 		self.semsubject_id = semsubject_id


# 	def __repr__(self):
# 		return '<id {}>'.format(self.semsubject_id)