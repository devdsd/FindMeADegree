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

maxyear = 6
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
                # degrees.append(prog.progcode)
                subjectsindegree = db.session.query(CurriculumDetails.subjcode, Subject.subjdesc, Subject.subjcredit).filter(CurriculumDetails.curriculum_id==Curriculum.curriculum_id).filter(Curriculum.progcode==prog).filter(CurriculumDetails.subjcode==Subject.subjcode).all()

        ### constraints ###
#genconstraints

        #academic status #note: if regular 18+, warning 18-, probation 12- units






#solver
solver = cp_model.CpSolver()

