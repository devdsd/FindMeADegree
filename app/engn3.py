from __future__ import division
from __future__ import print_function
from ortools.sat.python import cp_model
from app import app, db
from app.models import *
from flask_login import login_user, current_user, logout_user, login_required
import re


# class FindMeADegreeSolutionPrinter(cp_model.CpSolverSolutionCallback):
#     """Print intermediate solutions."""

#     def __init__(self, progs, subjectsindegree, remaining nga subjects (including ang lain nga information), num_shifts, sols):
#         cp_model.CpSolverSolutionCallback.__init__(self)
#         self._shifts = shifts
#         self._num_nurses = num_nurses
#         self._num_days = num_days
#         self._num_shifts = num_shifts
#         self._solutions = set(sols)
#         self._solution_count = 0

#     def on_solution_callback(self):
#         if self._solution_count in self._solutions:
#             print('Solution %i' % self._solution_count)
#             for d in range(self._num_days):
#                 print('Day %i' % d)
#                 for n in range(self._num_nurses):
#                     is_working = False
#                     for s in range(self._num_shifts):
#                         if self.Value(self._shifts[(n, d, s)]):
#                             is_working = True
#                             print('  Nurse %i works shift %i' % (n, s))
#                     if not is_working:
#                         print('  Nurse {} does not work'.format(n))
#             print()
#         self._solution_count += 1

#     def solution_count(self):
#         return self._solution_count


def datas():
                # Querying data from the database #
    semstudent = SemesterStudent.query.filter_by(studid=current_user.studid).first()
    semstudent2 = db.session.query(SemesterStudent.studid, SemesterStudent.sy, SemesterStudent.studlevel, SemesterStudent.sem, SemesterStudent.scholasticstatus).filter_by(studid=current_user.studid).all()
    sems = db.session.query(Registration.sem).filter_by(studid=current_user.studid).group_by(Registration.sem).all()
    listgpas = db.session.query(SemesterStudent.studid, SemesterStudent.gpa, SemesterStudent.sy, SemesterStudent.sem).filter_by(studid=current_user.studid).all()
    residency = db.session.query(SemesterStudent.sy).filter_by(studid=current_user.studid).distinct().count()
    progs = db.session.query(Program.progcode).all()
    subjects = db.session.query(Subject.subjcode, Subject.subjdesc, Subject.subjcredit, Subject.subjdept).all()
    studlevel = semstudent2[-1].studlevel
    student_program = Program.query.filter_by(progcode=semstudent.studmajor).first()
    lateststudent_record = semstudent2[-1]
    current_sem = db.session.query(Semester.sy, Semester.sem).filter(Semester.is_online_enrollment_up==True).first()

    
    # degrees = []
  
    passedsubjslist = []
    passedsubjcodes = []
    failedsubjslist = []
    failedsubjcodes = []
    subjectsinformations = []
    gpas = []
   

    
    for gpa in listgpas:
        gpas.append(gpa.gpa)

    cgpa = 0.0
    count = 0
    
    for gpa in gpas:
        if gpa is not None:
            cgpa = cgpa + float(gpa)
            count = count + 1

    cgpa = cgpa/float(count)


    for s in subjects:
        entry = {
            'subjcode': s.subjcode,
            'subjdesc': s.subjdesc,
            'unit': s.subjcredit
        } 

        subjectsinformations.append(entry)


    for subj in subjectsinformations:
        q = Registration.query.filter(Registration.subjcode==subj['subjcode']).filter(Registration.studid==current_user.studid).first()
        
        if q is not None:
            if q.grade != '5.0':
                passedsubjslist.append(q)
                passedsubjcodes.append(q.subjcode)
            else:
                failedsubjslist.append(q)
                failedsubjcodes.append(q.subjcode)

    return semstudent2, sems, listgpas, residency, progs, subjects, studlevel, student_program, lateststudent_record, current_sem, passedsubjslist, passedsubjcodes, failedsubjslist, failedsubjcodes, subjectsinformations

# def variables(datas):
            ### variables
    
def constraints(semstudent2, sems, listgpas, residency, progs, subjects, studlevel, student_program, lateststudent_record, current_sem, passedsubjslist, passedsubjcodes, failedsubjslist, failedsubjcodes, subjectsinformations):
    maxyear = 6
    unit = 0
    countfail = 0
    output = {}
            ### model
    model = cp_model.CpModel()
        
            ### student cannot shift if MRR
    if residency > maxyear:
        print ("No recommendation!")
    # model.Add(datas[3] < maxyear)

    ## student cannot shift when have 4 or greater failing grades in current sem
    for fail in failedsubjslist:
        if (fail.sy == lateststudent_record.sy and fail.sem == lateststudent_record.sem):
            countfail += 1
                    
    if (countfail > 4):
        print ("No recommendation!")


    # return semstudent, sems, listgpas, residency, progs, subjects, progs, studlevel, student_program, lateststudent_record, current_sem

    for prog in progs:

        if prog == student_program:
            pass

        else:
            curr = db.session.query(CurriculumDetails.subjcode).filter(CurriculumDetails.curriculum_id==Curriculum.curriculum_id).filter(Curriculum.progcode==prog).all()

            subjectsindegree = []
            passedsubjs = []
            failedsubjs = []
            
            for s in subjectsinformations:
                q = db.session.query(CurriculumDetails.subjcode, Curriculum.progcode, CurriculumDetails.curriculum_year, CurriculumDetails.curriculum_sem).filter(Curriculum.curriculum_id==CurriculumDetails.curriculum_id).filter(CurriculumDetails.subjcode==s['subjcode']).filter(Curriculum.progcode==prog).first()

                if q is not None:
                    q2 = db.session.query(Prerequisite.prereq).filter(Prerequisite.subjcode==q[0]).first()
                    if q2 is not None:
                        if q2 in curr:
                            s['prereq'] = q2[0]
                        else:
                            s['prereq'] = "None"
                    else:
                        s['prereq'] = "None"
                    subjectsindegree.append(s)

            
            for subj in subjectsindegree:
                q = Registration.query.filter(Registration.subjcode==subj['subjcode']).filter(Registration.studid==current_user.studid).first()
            
                if q is not None:
                    if q.grade != '5.0':
                        subj.update({'grade': q.grade})
                        passedsubjs.append(subj)
                    else:
                        subj.update({'grade': q.grade})
                        failedsubjs.append(subj)
                else:
                    subj.update({'grade': None})


                        ##------------ Department Constraints --------------------##
                        ##========================================================##

            if prog == 'BSN':
                if lateststudent_record.gpa > 2.0:
                    model.Add(prog != 'BSN')


            if prog == 'BSEdMath' or prog == 'BSEdPhysics':
                if residency == 2:
                    patterned = re.compile(r'(ELC|SED|EDM|CPE)(\d{3}|\d{3}.\d{1})')
                    edsubjs = list(filter(patterned.match, passedsubjcodes))
                    if not edsubjs:
                        model.Add(prog != 'BSEdMath')
                        model.Add(prog != 'BSEdPhysics')

            for passed in passedsubjs:
                if prog == 'BSMath' or prog == 'BSStat':
                    patternms = re.compile(r'(MAT|STT)(\d{3}|\d{3}.\d{1})')
                    mssubjs = list(filter(patternms.match, passedsubjcodes))
                    mssubjsinfo = []
                    for ms in mssubjs:
                        if passed['subjcode'] == ms:
                            mssubjsinfo.append(passed)
                    for msinfo in mssubjsinfo:
                        if (msinfo['grade'] > '2.5'): ## if grades sa Math ug stat lapas sa 2.5
                            model.Add(prog != 'BSMath')
                            model.Add(prog != 'BSStat')
            

                if prog == 'BSCS':
                    patterncs = re.compile(r'(MAT|STT|CSC|CCC)(\d{3}|\d{3}.\d{1})')
                    csubjs = list(filter(patterncs.match, passedsubjcodes))
                    cssubjsinfo = []
                    for cs in csubjs:
                        if passed['subjcode'] == cs:
                            cssubjsinfo.append(passed)
                    for csinfo in cssubjsinfo:
                        if(csinfo['grade'] > '2.5'):## if grades sa math,stat, ug cs lapas sa 2.5
                            model.Add(prog != 'BSCS')


                if prog == 'BSEE' or prog == 'BSCpE':
                    if passed['subjcode'] != 'MAT060' and current_sem.sem != 1: #note: mkashift ra ani every 1st sem sa school year
                        model.Add(prog != 'BSEE')
                        model.Add(prog != 'BSCpE')


                if prog == 'BSPsych':
                    if passed['subjcode'] != 'PSY100':
                        if lateststudent_record.gpa > 1.75:
                            model.Add(prog != 'BSPsych')

                    ### General Constraints

            sub = []
            for s in subjectsindegree:
                sub.append(s['subjcode'])

            psubjs = []
            for p in passedsubjs:
                psubjs.append(p['subjcode'])

            
            for s in subjectsindegree:
                preqs = db.session.query(Prerequisite.subjcode).filter(Prerequisite.subjcode == s['subjcode']).all()
                position, subjectWeight = 0, 0
                queriedSubjects = []
                queriedSubjects.append([s['subjcode']])
                
                while position < len(queriedSubjects):
                    subjectPerDegree = []
                    for i in queriedSubjects[position]:
                        temp = db.session.query(Prerequisite.subjcode).filter(Prerequisite.prereq==i).all()
                        if temp:
                            for item in temp:
                                if item[0] in sub:
                                    subjectPerDegree.append(item)
                    if len(subjectPerDegree)>0:
                        queriedSubjects.append(subjectPerDegree)
                        subjectWeight = subjectWeight + 1
                    position=position+1
                s.update({'weight': subjectWeight})

            courses = []

            for subject in subjectsindegree:
                semsy = db.session.query(CurriculumDetails.curriculum_year,CurriculumDetails.curriculum_sem).filter(CurriculumDetails.subjcode == subject['subjcode']).filter(CurriculumDetails.curriculum_id == Curriculum.curriculum_id).filter(Curriculum.progcode == 
                prog).first()

                if semsy is not None and semsy.curriculum_year <= studlevel and semsy.curriculum_sem == current_sem.sem:
                    if subject['subjcode'] not in psubjs:
                            courses.append(subject)
                            courses.sort(key = lambda i:i['weight'], reverse = True)

            specific_courses = []

            for  c in courses:
                if lateststudent_record.scholasticstatus == 'Warning':
                    unit += c['unit']
                    if unit <= 17:
                        specific_courses.append(c)
                        
<<<<<<< HEAD
                        if semsy is not None and semsy.curriculum_sem == current_sem.sem:
                            if subject['prereq'] in psubjs or subject['prereq'] == 'None':
                                # print("Prereq:" + subject['prereq'] + "Subject:" + subject['subjcode'])
                                if subject['subjcode'] not in psubjs:
                                    # print ("subject['subjcode']" + "not in psubjs -> ", subject['subjcode'], subject['subjcode'] not in psubjs)
                                    courses.append(subject)
                                    # courses.sort(key = lambda i:i['weight'], reverse = True)/ayaw sa ni idelete
                                    courses.sort(key = lambda i:(i['unit'], i['weight']), reverse = True)


                    specific_courses = []

                    for c in courses:

                        if lateststudent_record.scholasticstatus == 'Regular':
                            unit += c['unit']
                            specific_courses.append(c)

                        if lateststudent_record.scholasticstatus == 'Warning':
                            unit += c['unit']
                            if unit <= 17:
                                specific_courses.append(c)
                            else:
                                unit -= c['unit']
                                
                        if lateststudent_record.scholasticstatus == 'Probation':
                            unit += c['unit']
                            if unit <= 12:
                                specific_courses.append(c)
                            else:
                                unit -= c['unit']


                    remaincourses = []
                    for s in deg["subjects"]:
                        if s not in passedsubjs :
                            remaincourses.append(s)

                    #### Diether: Edited Code Starts Here! ####
                    # for passed in passedsubjs:
                    if degreeparsed == 'BSN':
                        if lateststudent_record.gpa > float(2.0):
                            # model.Add(prog != 'BSN')
                            print("BSN ni siya!")
                            deg['status'] = 0
                        else:
                            print(specific_courses)

                    if degreeparsed == 'BSEdMath' or degreeparsed == 'BSEdPhysics':

                        if residency >= 2:
                            patterned = re.compile(r'(ELC|SED|EDM|CPE)(\d{3}|\d{3}.\d{1})')
                            edsubjs = list(filter(patterned.match, psubjs))
                            print('BSEdMath and BSEdPhysics')
                            if edsubjs == []:
                                # model.Add(prog != 'BSEdMath')
                                # model.Add(prog != 'BSEdPhysics')
                                print('BSEdMath and BSEdPhysics')
                                deg['status'] = 0


                    if degreeparsed == 'BSMath' or degreeparsed == 'BSStat':
                        for passed in passedsubjs:
                            patternms = re.compile(r'(MAT|STT)(\d{3}|\d{3}.\d{1})')
                            mssubjs = list(filter(patternms.match, passedsubjcodes))
                            mssubjsinfo = []
                            for ms in mssubjs:
                                if passed['subjcode'] == ms:
                                    mssubjsinfo.append(passed)
                            for msinfo in mssubjsinfo:
                                if (msinfo['grade'] > '2.5'): 
                                    print ("MathStat")
                                    deg['status'] = 0
                        
                    if degreeparsed == 'BSCS':
                        for passed in passedsubjs:
                            patterncs = re.compile(r'(MAT|STT|CSC|CCC)(\d{3}|\d{3}.\d{1})')
                            csubjs = list(filter(patterncs.match, psubjs))
                            cssubjsinfo = []
                            
                            for cs in csubjs:
                                if passed['subjcode'] == cs:
                                    cssubjsinfo.append(passed)
                            for csinfo in cssubjsinfo:
                                if(csinfo['grade'] > '2.5'):## if grades sa math,stat, ug cs lapas sa 2.5
                                        # model.Add(prog != 'BSCS')
                                        print("BSCS ni Siya!!")
                                        deg['status'] = 0


                    if degreeparsed == 'BSEE' or degreeparsed == 'BSCpE':
                        for passed in passedsubjs:
                            if passed['subjcode'] != 'MAT060' and current_sem.sem != 1: #note: mkashift ra ani every 1st sem sa school year
                                # model.Add(prog != 'BSEE')
                                # model.Add(prog != 'BSCpE')
                                print("BSEE and BSCpE")
                                deg['status'] = 0
                                


                    if degreeparsed == 'BSPsych':
                        if lateststudent_record.gpa > float(1.75):
                        # if passed.subjcode != 'PSY100':
                            # model.Add(prog != 'BSPsych')
                            print("Psych ni siya")
                            deg['status'] = 0

                        #### Edited Code Ends Here ######
                    
=======
                if lateststudent_record.scholasticstatus == 'Probation':
                    unit += c['unit']
                    if unit <= 12:
                        specific_courses.append(c)
                        
                if lateststudent_record.scholasticstatus == 'Regular':
                    unit += c['unit']
                    specific_courses.append(c)
>>>>>>> 8c72f042fdff59c450be0aa5646f655b19829ac9

            coursestaken = passedsubjs + specific_courses
        

            remaincourses = []
            for s in subjectsindegree:
                if s in coursestaken:
                    pass
                else:
                    remaincourses.append(s)

        # dictoutput.update({'prog': prog})
        # dictoutput['remaining'] = remaincourses

    return output
    

def main():
    var_datas = datas()
    # var_variables = variables(var_datas)
    # var_constraints = constraints(var_variables[0], var_variables[1], var_variables[2], var_variables[3], var_variables[4], var_variables[5], var_variables[6], var_variables[7], var_variables[8], var_variables[9], var_variables[10], var_datas, var_variables[11])
    # var_constraints = constraints(semstudent2, sems, listgpas, residency, progs, subjects, studlevel, student_program, lateststudent_record, current_sem, passedsubjslist, passedsubjcodes, failedsubjslist, failedsubjcodes, subjectsinformations)
    
    for vc in var_constraints:
        if vc is not None:
            print("String: {}".format(vc))

    #solver
    solver = cp_model.CpSolver()

    # solution_printer = FindMeADegreeSolutionPrinter()

    # solver.SearchForAllSolutions(model, solution_printer)


