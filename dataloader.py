""" static.py
	- this module contains auto database populate funcitons
	- which will put synthetic datas to the database
"""

import json
from app.models import *


def openJSON(filename):
    with open(filename) as data:
        res = json.load(data)
    return res['data']


def addStudent():
	for x in openJSON('app/resources/datas/studentdatas.json'):
		reg = Student.query.filter_by(studid=x[0]).first()
		if reg is None:
			reg = Student(
				studid=x[0],
				studfirstname = x[1],
				studmidname = x[2],
				studlastname = x[3],
				emailadd=x[4],
				password=x[5],
				image_file=x[6]
				)
			db.session.add(reg)
		db.session.commit()


def addCollege():
	for x in openJSON('app/resources/datas/collegedatas.json'):
		acct = College.query.filter_by(collcode=x[1]).first()
		if acct is None:
			acct = College(
				collname=x[0], 
				collcode=x[1]
				)
			db.session.add(acct)
		db.session.commit()

def addDept():
	for x in openJSON('app/resources/datas/departmentdatas.json'):
		acct = Department.query.filter_by(deptname=x[1]).first()
		if acct is None:
			acct = Department(
				deptcode=x[0],
				deptname=x[1], 
				deptcoll=x[2],
				)
			db.session.add(acct)
		db.session.commit()

def addCurriculum():
	for a in openJSON('app/resources/datas/curriculumdatas.json'):
		acct = Curriculum.query.filter_by(progcode=a[1]).first()
		if acct is None:
			acct = Curriculum(
				curriculum_id=a[0],
				progcode=a[1],
				total_units=a[2],
				)
			db.session.add(acct)
		db.session.commit()

def addCurriculumDetails():
	for a in openJSON('app/resources/datas/curriculumdetailsdatas.json'):
		acct = CurriculumDetails.query.filter_by(subjcode=a[3]).first()
		if acct is None:
			acct = CurriculumDetails(
				curriculum_id=a[0],
				curriculum_year=a[1],
				curriculum_sem=a[2],
				subjcode=a[3]
				)
			db.session.add(acct)
		db.session.commit()


def addSubject():
	for a in openJSON('app/resources/datas/subjectdatas.json'):
		acct = Subject.query.filter_by(subjcode=a[0]).first()
		if acct is None:
			acct = Subject(
				subjcode=a[0], 
				subjdesc=a[1], 
				subjcredit=a[2],
				subjdept=a[3]
				)
			db.session.add(acct)
		db.session.commit()


def addSemStud():
	for i in openJSON('app/resources/datas/semstudentdatas.json'):
		acct = SemesterStudent.query.filter_by(studid=i[0], sy=i[2], sem=str(i[1])).first()
		if acct is None:
			acct = SemesterStudent(
					studid=i[0], 
					sem=i[1], 
					sy=i[2], 
					studmajor=i[6], 
					studlevel=i[3], 
					scholasticstatus=i[4], 
					scholarstatus=i[5],
					gpa=i[7],
					cgpa=i[8]
					)
			db.session.add(acct)
		db.session.commit()


def addRegistration():
	for i in openJSON('app/resources/datas/registrationdatas_new.json'):
		acct = Registration.query.filter_by(studid=i[0], sem=i[1], sy=i[2], subjcode=i[3], grade=str(i[4]), section=i[5]).first()
		if acct is None:
			acct = Registration(
				sem=i[1], 
				sy=i[2], 
				subjcode=i[3], 
				grade=str(i[4]), 
				section=i[5], 
				studid=i[0]
					)
			db.session.add(acct)
		db.session.commit()


def addSemesterSubject():
	for i in openJSON('app/resources/datas/semsubjectdatas_new.json'):
		acct = SemesterSubject.query.filter_by(section=i[3], sy=i[0], sem=i[1],subjcode=i[2]).first()
		if acct is None:
			acct = SemesterSubject(
				sy=i[0],
				sem=i[1],
				subjcode=i[2],
				section=i[3],
				semsubject_id=i[4]
					)
			db.session.add(acct)
		db.session.commit()


def addPrerequisites():
	for i in openJSON('app/resources/datas/prerequisitedatas.json'):
		acct = Prerequisite.query.filter_by(subjcode=i[0]).first()
		if acct is None:
			acct = Prerequisite( 
				subjcode=i[0], 
				prereq=i[1]
				)
			db.session.add(acct)
		db.session.commit()


def addProgram():
	for i in openJSON('app/resources/datas/programdatas.json'):
		acct = Program.query.filter_by(progcode=i[0]).first()
		if acct is None:
			acct = Program( 
				progcode=i[0], 
				progdesc=i[1],
				progdept=i[2]
				)
			db.session.add(acct)
		db.session.commit()