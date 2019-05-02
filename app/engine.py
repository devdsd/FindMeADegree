#from app import *
from ortools.sat.python import cp_model

#model
enmodel = cp_model.CpModel()

#variables
s = enmodel.#student
pc = enmodel.#prev.courses
sbj = enmodel.#allsubjects
#constraints
#genconstraints
enmodel.Add(grade>=3)
enmodel.Add()
#deptconstraints
#CS
enmodel.Add(grade(degree(Comsci) <= 2.5))
enmodel.Add(grade(degree(Math) <= 2.5))
enmodel.Add(grade('

degree(Stat) <= 2.5))
enmodel.Add(grade(degree(Physics) <= 2.5))
#MathStat
enmodel.Add(grade(degree(Math) <= 2.5))
enmodel.Add(grade(degree(Stat) <= 2.5))
#Nursing
enmodel.Add(student gpa <= 2.0)
#Psych
enmodel.Add(student gpa <= 1.75)
enmodel.Add(prevcourse = Pshych 1 or Psych 100)
#EECE
enmodel.Add(prevcourse = Math 60)
enmodel.Add(sem = 1)
#edPysEdMat
enmodel.Add(student gpa <= 2.0)
enmodel.Add(if studentyear>1, prevcourse(degree(Ed)))



#solver
solver = cp_model.CpSolver()

