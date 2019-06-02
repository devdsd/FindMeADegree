from __future__ import division
from __future__ import print_function
from app.models import *
from ortools.sat.python import cp_model

#data

# query -> student currently on session
student = Student.query.filter_by(studid=current_user.studid).first()
#query -> student info
studinfo = SemesterStudent.query.filter_by(studid=current_user.studid).first()
#query -> previous courses and grades
prevcourse_grade = Registration.query.filter_by(subjcode=current_user.subjcode,grade=current_user.grade).all()
maxsem = 12
#query -> residency = count all semesters of student
subj = Subject.query.filter_by(subjcode).all()
prog = Program.query.filter_by(progcode).all()

num_deg = Program.query.filter_by(progcode).count()
all_deg = range(num_deg)
num_sub = Subject.query.filter_by(subjcode).count()
all_sub = range(num_sub)


#model
model = cp_model.CpModel()

#note: student, semstudent, registration, 

#variables
s = model.#student
pc = model.#prev.courses
sbj = model.#allsubjects
#constraints
#genconstraints

#academic status #note: if regular 18+, warning 18-, probation 12- units
ac_st = [1,2,3]
ac_st[1]='Regular'
ac_st[2]='Warning'
ac_st[3]='Probation'


if n in ac_st[n] ==1:
    if residency >= 8 and studlevel == 4:
        model.Add(sem_units >= 3)
    else:
        model.Add(sem_units>=18)
if n in ac_st[n]==2:
    model.Add(sem_units<18)
if n in ac_st[n]==3:
    model.Add(sem_units<=12)

#gpa 
model.Add(grade<=3)
model.Add(residency <= maxsem)
model.Add(gpa <= 3)
#constraint, no more than 4 failure grade on same sem.

#deptconstraints
#CS
model.Add(grade(degree(Comsci) <= 2.5))
model.Add(grade(degree(Math) <= 2.5))
model.Add(grade(degree(Stat)<= 2.5))
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
model.Add(if residency >2: prevcourse(degree(Ed))




#solver
solver = cp_model.CpSolver()

