from __future__ import division
from __future__ import print_function
from app.models import *
from ortools.sat.python import cp_model

            # Querying data from the database #

semstudent = SemesterStudent.query.filter_by(studid=current_user.studid).first()
            
            ### subjecthistories - previously taken na courses (description and code),grades, sems (Residency sa Student), 
subjecthistories = db.session.query(Registration.studid, Registration.sem, Registration.sy, Registration.subjcode, Registration.grade, Registration.section, Subject.subjdesc).filter(Registration.studid==current_user.studid).filter(Registration.subjcode==Subject.subjcode).all()

            ### Lists
sems = db.session.query(Registration.sem).filter_by(studid=current_user.studid).group_by(Registration.sem).all()

listgpas = db.session.query(SemesterStudent.studid, SemesterStudent.gpa, SemesterStudent.sy, SemesterStudent.sem).filter_by(studid=current_user.studid).all()

gpas = []
for gpa in listgpas:
    gpas.append(gpa.gpa)


# prevcourses = []
# for prevcourse in subjecthistories:
#     prevcourses.append(prevcourse.subjcode, prevcourse.grade)


# grades = []
# for grade in subjecthistories:
#     grades.append(grade.grade)


maxsem = 12
            ### query -> residency = count all semesters of student
residency = len(sems) #total number of sems nga nakuha sa studyante

cgpa = 0.0
count = 0
    
for gpa in gpas:
    if gpa is not None:
        cgpa = cgpa + float(gpa)
        count = count + 1

cgpa = cgpa/float(count)

            ### Comparison Purposes
progs = Program.query.filter_by(progcode).all()
prereqs = db.session.query(Prerequisite.subjcode, Prerequisite.prereq).all()

            ### model
model = cp_model.CpModel()

            ### variables
degrees = [] # Container of the Results
passedsubjs = []
failedsubjs = []

            ### the student cannot shift on their current degree
for prog in progs:
        if prog.progcode == semstudent.studmajor:
                model.Add(prog.progcode != semstudent.studmajor)
        else:
                # degrees.append(prog.progcode)
                subjectsindegree = db.session.query(CurriculumDetails.subjcode, Subject.subjdesc, Subject.subjcredit).filter(CurriculumDetails.curriculum_id==Curriculum.curriculum_id).filter(Curriculum.progcode==prog).filter(CurriculumDetails.subjcode==Subject.subjcode).all()

                for sh in subjecthistories:
                        if (sh.grade != 5.00):
                                passedsubjs.append(sh)
                        else:
                                failedsubjs.append(sh)
                

# QUEUE
for i in subjecthistories:
        if i.grade != 5.00:
                model.Add(subjecthistories != subjectsindegree)
        else:
                subjectsindegrees.append(subjectsindegree)

for i in subjecthistories:
        if i.grade != 5.00:
                napasarnasubjs.append(i)
        else:
                failedsubj.append(i)

for x in napasarnasubjs:
        model.Add(x != subjectsindegree)

        
# for subject in semsubje
# model.Add()

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
model.Add(student gpa <= 2.0)

#Psych
model.Add(student gpa <= 1.75)
model.Add(prevcourse = Pshych 1 or Psych 100)

#EECE
model.Add(prevcourse = Math 60)
model.Add(sem = 1)

#edPysEdMat
model.Add(student gpa <= 2.0)
model.Add(if residency > 2: prevcourse(degree(Ed))




#solver
solver = cp_model.CpSolver()

