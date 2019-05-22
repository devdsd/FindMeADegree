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
prevcourse_grade = Registration.query.filter_by(subjcode=current_user.subjcode,grade=grade)
maxsem = 12
#query -> residency = count all semesters of student
#remaining semester
rem_sem = maxsem - residency
subj = Subject.query.filter_by(subjcode)
prog = Program.query.filter_by(progcode)
curri = Curriculum.query.filter_by(progcode)
dept  = Department.query.filter_by(deptcode)

num_deg = Program.query.filter_by(progcode).count()
all_deg = range(num_deg)


#query -> program, curri, subj, dept from db
#query -> num degree


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


model.Add(grade>=3)
model.Add()
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
model.Add(if studentyear>1, prevcourse(degree(Ed)))



#solver
solver = cp_model.CpSolver()

