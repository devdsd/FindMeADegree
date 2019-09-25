from __future__ import division
from __future__ import print_function
from app.models import *
from ortools.sat.python import cp_model
import re

            # Querying data from the database #

semstudent = SemesterStudent.query.filter_by(studid=current_user.studid).first()

subjecthistories = db.session.query(Registration.studid, Registration.sem, Registration.sy, Registration.subjcode, Registration.grade, Registration.section, Subject.subjdesc).filter(Registration.studid==current_user.studid).filter(Registration.subjcode==Subject.subjcode).all()

            ### Lists
sems = db.session.query(Registration.sem).filter_by(studid=current_user.studid).group_by(Registration.sem).all()

listgpas = db.session.query(SemesterStudent.studid, SemesterStudent.gpa, SemesterStudent.sy, SemesterStudent.sem).filter_by(studid=current_user.studid).all()

gpas = []
for gpa in listgpas:
    gpas.append(gpa.gpa)

maxsem = 12
residency = len(sems) # total number of sems nga nakuha sa studyante

cgpa = 0.0
count = 0
    
for gpa in gpas:
    if gpa is not None:
        cgpa = cgpa + float(gpa)
        count = count + 1

cgpa = cgpa/float(count)
progs = db.session.query(Program.progcode).all()
prereqs = db.session.query(Prerequisite.subjcode, Prerequisite.prereq).all()

            ### model
model = cp_model.CpModel()

            ### variables
degrees = [] # Container of the Results
passedsubjs = []
failedsubjs = []

##for pattern recognition
# ccc = re.compile("CCC*")
# csc = re.compile("CSC*")
# mat = re.compile("MAT*")

            ### the student cannot shift on their current degree
for prog in progs:
        if prog.progcode == semstudent.studmajor:
                model.Add(prog.progcode != semstudent.studmajor)
        else:

                subjectsindegree = db.session.query(CurriculumDetails.subjcode, Subject.subjdesc, Subject.subjcredit).filter(CurriculumDetails.curriculum_id==Curriculum.curriculum_id).filter(Curriculum.progcode==prog).filter(CurriculumDetails.subjcode==Subject.subjcode).all()

                for sh in subjecthistories:
                        for subject in subjectsindegree:
                                if (sh.grade != '5.00'):
                                        passedsubjs.append(sh)
                                else:
                                        failedsubjs.append(sh)

                                # for passed in passedsubjs:
                                #         model.Add(passed.subjcode != subject.subjcode)
                                #         ccclist = filter(ccc.match, passed)
                                #         csclist = filter(csc.match, passed)
                                #         matlist = filter(mat.match, passed)

                                for passed in passedsubjs:
                                        if (passed)
                                        
                                        
                                        for p in prereqs:
                                                if (p.prereq != passed.subjcode):
                                                        model.Add(subject.subjcode != p.subjcode)

ccc = re.compile("CCC*")
mat = re.compile("MAT*")
cccsubjs = list(filter(ccc.match, passedsubjs))
matsubjs = list(filter(mat.match, passedsubjs))


        ### constraints ###
#genconstraints

        #academic status #note: if regular 18+, warning 18-, probation 12- units
ac_st = {1: 'Regular', 2: 'Warning', 3: 'Probation'}


if n in ac_st[n] == 1:
    if residency >= 8 and studlevel == 4:
        model.Add(sem_units >= 3)
    else:
        model.Add(sem_units>=18)
if n in ac_st[n]==2:
    model.Add(sem_units<18)
if n in ac_st[n]==3:
    model.Add(sem_units<=12)



#gpa 
model.Add(grade<=3.0)
model.Add(residency <= maxsem)
model.Add(gpa <= 3.0)

#constraint, no more than 4 failure grade on same sem.


        #deptconstraints
#CS
model.Add(grade(degree(Comsci) <= 2.5))
model.Add(grade(degree(Math) <= 2.5))
model.Add(grade(degree(Stat) <= 2.5))

#MathStat
model.Add(grade(degree(Math) <= 2.5))
model.Add(grade(degree(Stat) <= 2.5))

#Nursing
if semstudent.gpa > 2.0:
        model.Add(prog.progcode != "BSN")

#Psych
if semstudent.gpa > 1.75:
        for sh in subjecthistories:
                if sh.subjcode != "PSY100"
                model.Add(prog.progcode != "BSPsych")

#EECE
for sh in subjecthistories:
        if sh.subjcode != "MAT060" and sem != 1
        model.Add(prog.progcode != "BSEE")
        model.Add(prog.progcode != "BSEC")


#edPysEdMat
model.Add(prog.progcode != "BSEdMath" if semstudent.gpa > 2.0)

if semstudent.studlevel >2:

        model.Add(prevcourse(degree(Ed))




#solver
solver = cp_model.CpSolver()

