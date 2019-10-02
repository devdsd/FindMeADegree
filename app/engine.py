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

<<<<<<< HEAD
maxyear = semstudent.studlevel * 1.5
residency = db.session.query(SemesterStudent.sy).filter_by(studid=current_user.studid).distinct().count()
=======
maxyear = 6
residency = len(sems) #total number of sems nga nakuha sa studyante
>>>>>>> 30dcec073da6dd2aa7d7bfa3d5654d5edbdf36a8

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

for sh in subjecthistories:
        if (sh.grade != 5.00):
                passedsubjs.append(sh)
        else:
                failedsubjs.append(sh)

### student cannot shift if MRR
if semstudent.studyear > maxyear:
        exit()

## student cannot shift when have 4 or greater failing grades in current sem

#student cannot shift when having 2 consecutive probation status


##for pattern recognition
# ccc = re.compile("CCC*")
# csc = re.compile("CSC*")
# mat = re.compile("MAT*")c

if semstudent.studlevel > maxyear:
        model.Add()


for sh in subjecthistories:
        if (sh.grade != '5.00'):
                passedsubjs.append(sh)
        else:
                failedsubjs.append(sh)

for prog in progs:
        ### the student cannot shift on their current degree
        if prog.progcode == semstudent.studmajor:
                model.Add(prog.progcode != semstudent.studmajor)

        elif semstudent.gpa > 2.0:
                model.Add(prog.progcode != 'BSN')

        for passed in passedsubjs:
                        ##Department Constraints
                        if residency == 2 :
                                if (): ##if wala sa passed subjects ang mga ED courses
                                        model.Add(prog.progcode != 'BSEdMath')
                                        model.Add(prog.progcode != 'BSEdPhysics')
                        
                        elif  (): ## if grades sa Math ug stat lapas sa 2.5
                                model.Add(prog.progcode != 'BSMath')
                                model.Add(prog.progcode != 'BSStat')
                        elif():## if grades sa math,stat, ug cs lapas sa 2.5
                                model.Add(prog.progcode != 'BSCS')
                        elif passed != 'MAT060' and sem != 1:
                                model.Add(prog.progcode != 'BSEE')
                                model.Add(prog.progcode != 'BSCpE')

                        elif passed != 'PSY100':
                                if semstudent.gpa > 1.75:
                                        model.Add(prog.progcode != 'BSPsych')  
        else:
                subjectsindegree = db.session.query(CurriculumDetails.subjcode, Subject.subjdesc, Subject.subjcredit).filter(CurriculumDetails.curriculum_id==Curriculum.curriculum_id).filter(Curriculum.progcode==prog).filter(CurriculumDetails.subjcode==Subject.subjcode).all()

                for passed in passedsubjs:
                        for prerq in prereqs:
                                if (passed.subjcode == prerq.prereq):
                                        subjectsindegree.remove(prerq)

                        for p in prereqs:
                                if (p.prereq != passed.subjcode):
                                        model.Add(subject.subjcode != p.subjcode)


                                # for passed in passedsubjs:
                                #         model.Add(passed.subjcode != subject.subjcode)
                                #         ccclist = filter(ccc.match, passed)
                                #         csclist = filter(csc.match, passed)
                                #         matlist = filter(mat.match, passed)

                                for passed in passedsubjs:
                                        for prerq in prereqs:
                                                if (passed.subjcode == prerq.prereq):
                                                        subjectsindegree.remove(passed.subjcode)

                                        
                                        
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








#solver
solver = cp_model.CpSolver()

