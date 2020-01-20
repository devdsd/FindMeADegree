from __future__ import division
from __future__ import print_function
from ortools.sat.python import cp_model
from app import app, db
from app.models import *
from flask_login import login_user, current_user, logout_user, login_required
import re


def datas():
                # Querying data from the database #
    semstudent = SemesterStudent.query.filter_by(studid=current_user.studid).first()
    semstudent2 = db.session.query(SemesterStudent.studid, SemesterStudent.sy, SemesterStudent.studlevel, SemesterStudent.sem, SemesterStudent.scholasticstatus, SemesterStudent.gpa).filter_by(studid=current_user.studid).all()
    sems = db.session.query(Registration.sem).filter_by(studid=current_user.studid).group_by(Registration.sem).all()
    listgpas = db.session.query(SemesterStudent.studid, SemesterStudent.gpa, SemesterStudent.sy, SemesterStudent.sem).filter_by(studid=current_user.studid).all()
    residency = db.session.query(SemesterStudent.sy).filter_by(studid=current_user.studid).distinct().count()
    progs = db.session.query(Program.progcode).all()
    subjects = db.session.query(Subject.subjcode, Subject.subjdesc, Subject.subjcredit, Subject.subjdept).all()
    studlevel = semstudent2[-1].studlevel
    student_program = db.session.query(Program.progcode).filter_by(progcode=semstudent.studmajor).first()
    lateststudent_record = semstudent2[-1]
    current_sem = db.session.query(Semester.sy, Semester.sem).filter(Semester.is_online_enrollment_up==True).first()


                # Local Lists
    passedsubjslist = []
    passedsubjcodes = []
    failedsubjslist = []
    failedsubjcodes = []
    subjectsinformations = []
    subjectsindegree = []
    gpas = []


    for s in subjects:
        entry = {
            'subjcode': s.subjcode,
            'subjdesc': s.subjdesc,
            'unit': s.subjcredit
        } 

        subjectsinformations.append(entry)


    ## Para asa gane ni ? Nganong sa Subjects information siya mag loop (Dili ni madala sa subjectindegree mag loop)
    for subj in subjectsinformations:
        q = Registration.query.filter(Registration.subjcode==subj['subjcode']).filter(Registration.studid==current_user.studid).first()
        
        if q is not None:
            if q.grade != '5.0':
                passedsubjslist.append(q)
                passedsubjcodes.append(q.subjcode)
            else:
                failedsubjslist.append(q)
                failedsubjcodes.append(q.subjcode)

    degreeinfo = {}
    degrees = []
    
    for prog in progs:
        
        curr = db.session.query(CurriculumDetails.subjcode).filter(CurriculumDetails.curriculum_id==Curriculum.curriculum_id).filter(Curriculum.progcode==prog).all()

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

        degreeinfo['DegreeName'] = prog
        degreeinfo['subjects'] = subjectsindegree
        subjectsindegree = []
        degrees.append(degreeinfo)
        degreeinfo = {}


    return residency, passedsubjslist, passedsubjcodes, failedsubjslist, failedsubjcodes, subjectsinformations, lateststudent_record, degrees, progs, studlevel, current_sem, student_program, semstudent
    

def gen_constraints(residency, passedsubjslist, passedsubjcodes, failedsubjslist, failedsubjcodes, subjectsinformations, lateststudent_record, degrees, progs, studlevel, current_sem, student_program, semstudent):
    
            ### model
    model = cp_model.CpModel()
    
    prog_bool = {}
    bool_res = {}

    output = {}
    unit = 0
    maxyear = 6
    countfail = 0
            ### student cannot shift if MRR ###

    if residency > maxyear:
        print("Cannot shift!")

    ## student cannot shift when have 4 or greater failing grades in current sem
    
    for fail in failedsubjslist:
        if fail.sy == lateststudent_record.sy and fail.sem == lateststudent_record.sem:
            countfail += 1
                
    if countfail > 4:
        print("Cannot shift!")
    
    ### General Constraints
    

    sub = []
    for deg in degrees:
        deg['status'] = 1
        if deg['DegreeName'] == student_program:
            deg.update({'status': 0})
            pass

        else:
            for prog in progs:
                if deg['DegreeName'] == prog:
                    print()
                    print(prog)

                    degree = str(prog[0])
                    degreeparsed = degree.rstrip()
                    

                    passedsubjs = []
                    failedsubjs = []

                    for subj in deg['subjects']:
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

                    psubjs = []
                    for p in passedsubjs:
                        psubjs.append(p['subjcode'])
                    
                    for s in deg['subjects']:
                        sub.append(s['subjcode'])

                    for s in deg['subjects']:
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
                    for subject in deg['subjects']:
                        semsy = db.session.query(CurriculumDetails.curriculum_year,CurriculumDetails.curriculum_sem).filter(CurriculumDetails.subjcode == subject['subjcode']).filter(CurriculumDetails.curriculum_id == Curriculum.curriculum_id).filter(Curriculum.progcode == 
                        prog).first()

                        
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
                    
                    if degreeparsed == 'BSN':
                        if lateststudent_record.gpa > float(2.0):
                            # model.Add(prog != 'BSN')
                            deg.update({'status': 0})
                        


                    if degreeparsed == 'BSEdMath' or degreeparsed == 'BSEdPhysics':
                        if residency >= 2:
                            patterned = re.compile(r'(ELC|SED|EDM|CPE)(\d{3}|\d{3}.\d{1})')
                            edsubjs = list(filter(patterned.match, psubjs))
                            print('BSEdMath and BSEdPhysics')
                            if edsubjs == []:
                                # model.Add(prog != 'BSEdMath')
                                # model.Add(prog != 'BSEdPhysics')
                                deg.update({'status': 0})
                            



                    if degreeparsed == 'BSMath' or degreeparsed == 'BSStat':
                        for passed in passedsubjs:
                            patternms = re.compile(r'(MAT|STT)(\d{3}|\d{3}.\d{1})')
                            mssubjs = list(filter(patternms.match, passedsubjcodes))
                            mssubjsinfo = []
                            for ms in mssubjs:
                                if passed['subjcode'] == ms:
                                    mssubjsinfo.append(passed)
                            counter = 0
                            for msinfo in mssubjsinfo:
                                if (msinfo['grade'] > '2.5'):
                                    counter += 1
                            if counter != 0:
                                print(counter) 
                                print ("MathStat")
                                deg.update({'status': 0})
                            
                        
                    if degreeparsed == 'BSCS':
                        for passed in passedsubjs:
                            patterncs = re.compile(r'(MAT|STT|CSC|CCC)(\d{3}|\d{3}.\d{1})')
                            csubjs = list(filter(patterncs.match, psubjs))
                            cssubjsinfo = []
                            for cs in csubjs:
                                if passed['subjcode'] == cs:
                                    cssubjsinfo.append(passed)
                            counter = 0
                            for csinfo in cssubjsinfo:
                                if(csinfo['grade'] > '2.5'):## if grades sa math,stat, ug cs lapas sa 2.5
                                        counter += 1
                            if counter != 0:
                                    print("BSCS ni Siya!!")
                                    deg.update({'status': 0})
                            

                    if degreeparsed == 'BSEE' or degreeparsed == 'BSCpE':
                        for passed in passedsubjs:
                            if passed['subjcode'] != 'MAT060' and current_sem.sem != 1: #note: mkashift ra ani every 1st sem sa school year
                                deg.update({'status': 0})
                            


                    if degreeparsed == 'BSPsych':
                        if lateststudent_record.gpa > float(1.75):
                            for passed in psubjs:
                                if passed != 'PSY100':
                                    print("Psych ni siya")
                                    deg.update({'status': 0})
                                

                    
                        #### Edited Code Ends Here ######
                
                    # print(remaincourses)
                    # for r in specific_courses:
                    #     print(r['subjcode'])
                    # print ("units:  ", unit)
        



                    unit = 0
                    specific_courses = []
    

    for p in progs:
        bool_res[(p)] = model.NewBoolVar('%s' % (p))
    
    for deg in degrees:
        if deg['status'] == 1:
            model.Add(deg['status'] == 1)

        

 

    # return bool_res, degrees

    
# class PartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
#      def __init__(self, shifts, num_nurses, num_days, num_shifts, bool_res, progs, prog_and_gpa, gpa, sols):
#         cp_model.CpSolverSolutionCallback.__init__(self)
#         self._shifts = shifts
#         self._num_nurses = num_nurses
#         self._num_days = num_days
#         self._num_shifts = num_shifts
#         self._bool_res = bool_res
#         self._progs = progs
#         self._prog_and_gpa = prog_and_gpa
#         self._gpas = gpa
#         self._solutions = set(sols)
#         self._solution_count = 0

#     def on_solution_callback(self):
#         if self._solution_count in self._solutions:
#             for p in self._progs:
#                 # for g in self._gpas:
#                 if self.Value(self.bool_res[(p)]):
#                     is_working = True
#                     print('{} is recommended'.format(p))
#                 else:
#                     pass
#         self._solution_count += 1

#     def solution_count(self):
#         return self._solution_count

def main():
    var_datas = datas()
    var_constraints = gen_constraints(var_datas[0], var_datas[1], var_datas[2], var_datas[3], var_datas[4], var_datas[5], var_datas[6], var_datas[7], var_datas[8], var_datas[9], var_datas[10], var_datas[11], var_datas[12])
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    # a_few_solutions = range(1)
    # var_res = PartialSolutionPrinter(var_datas, var_constraints)
    # solver.SearchForAllSolutions(model, var_res)



    

