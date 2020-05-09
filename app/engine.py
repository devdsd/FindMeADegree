from __future__ import division
from __future__ import print_function
from ortools.sat.python import cp_model
from app import app, db
from app.models import *
from flask_login import login_user, current_user, logout_user, login_required
import re


def datas():
                # Querying data from the database #
    semstudent = SemesterStudent.query.filter_by(studid=current_user.studid).all()
    latestsemstud = semstudent[-1]
    sems = db.session.query(Registration.sem).filter_by(studid=current_user.studid).group_by(Registration.sem).all()
    listgpas = db.session.query(SemesterStudent.studid, SemesterStudent.gpa, SemesterStudent.sy, SemesterStudent.sem).filter_by(studid=current_user.studid).all()
    residency = db.session.query(SemesterStudent.sy).filter_by(studid=current_user.studid).distinct().count() 
    progs = db.session.query(Program.progcode).all()
    subjects = db.session.query(Subject.subjcode, Subject.subjdesc, Subject.subjcredit, Subject.subjdept).all()
    studlevel = latestsemstud.studlevel
    student_program = db.session.query(Program.progcode).filter_by(progcode=latestsemstud.studmajor).first()
    current_sem = db.session.query(Semester.sy, Semester.sem).filter(Semester.is_online_enrollment_up==True).first()


                # Local Lists
    passedsubjslist = []
    passedsubjcodes = []
    failedsubjslist = []
    failedsubjcodes = []
    subjectsinformations = []
    gpas = []
    residency = residency - 1
    
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
                passedsubjcodes.append(q.subjcode) # iyang napasaran nga mga subjects in the previous degree
            else:
                failedsubjslist.append(q)
                failedsubjcodes.append(q.subjcode) # iyang nabagsak nga mga subjects in the previous degree

    degrees = []
    
    for prog in progs:
        subjectsindegree = []
        degreeinfo = {}
        curr = db.session.query(CurriculumDetails.subjcode).filter(CurriculumDetails.curriculum_id==Curriculum.curriculum_id).filter(Curriculum.progcode==prog).all()

        for s in subjectsinformations:
            q = db.session.query(CurriculumDetails.subjcode, Curriculum.progcode, CurriculumDetails.curriculum_year, CurriculumDetails.curriculum_sem).filter(Curriculum.curriculum_id==CurriculumDetails.curriculum_id).filter(CurriculumDetails.subjcode==s['subjcode']).filter(Curriculum.progcode==prog).first()

            if q is not None:
                q2 = db.session.query(Prerequisite.prereq).filter(Prerequisite.subjcode==q[0]).all()
                # print(q2)
                if len(q2) != 0:

                    for i in q2:
                        if i in curr:
                            s.update({'prereq': i[0], 'yeartotake': q[2], 'semtotake': q[3]})
                            break
                        else:
                            s.update({'prereq': "None", 'yeartotake': q[2], 'semtotake': q[3]})
                else:
                    s.update({'prereq': "None", 'yeartotake': q[2], 'semtotake': q[3]})
                subjectsindegree.append(s)


        degreeinfo['DegreeName'] = prog
        degreeinfo['subjects'] = subjectsindegree
        
        degrees.append(degreeinfo)

    return residency, passedsubjslist, passedsubjcodes, failedsubjslist, failedsubjcodes, subjectsinformations, latestsemstud, degrees, progs, studlevel, current_sem, student_program
    

def constraints(residency, passedsubjslist, passedsubjcodes, failedsubjslist, failedsubjcodes, subjectsinformations, latestsemstud, degrees, progs, studlevel, current_sem, student_program):
    

    # output = {}
    unit = 0
    maxyear = 6
    countfail = 0
    tempres = 0

    
    remaining_years = maxyear - residency

            ### student cannot shift if MRR ###
    if residency > maxyear:
        print("Cannot shift!")


            ## student cannot shift when have 4 or greater failing grades in current sem
    for fail in failedsubjslist:
        if fail.sy == latestsemstud.sy and fail.sem == latestsemstud.sem:
            countfail += 1
                
    if countfail > 4:
        print("Cannot shift!")
    

            ### General Constraints
    sub = []

    for deg in degrees:

        deg['status'] = 1
        if deg['DegreeName'] == student_program:
            deg.update({'status': 0})

        else:
            for prog in progs:
                if deg['DegreeName'] == prog:


                    degree = str(prog[0])
                    degreeparsed = degree.rstrip()
                    
                    passedsubjs = []
                    failedsubjs = []

                    ## putting grade in every subjects that the student already taken in their previous degree
                    for subj in deg['subjects']:
                        q = Registration.query.filter(Registration.subjcode == subj['subjcode']).filter(Registration.studid == current_user.studid).first()
                        if q is not None:
                            if q.grade != '5.0':
                                subj.update({'grade': str(q.grade)})
                                passedsubjs.append(subj) # list of dictionary about the passed subjects for that degree

                            else:
                                subj.update({'grade': str(q.grade)})
                                failedsubjs.append(subj) # list of dictionary about the failed subjects for that degree
                        else:
                            subj.update({'grade': None})

                    psubjs = []
                    for p in passedsubjs:
                        psubjs.append(p['subjcode']) # extrating the subject codes from the passedsubjs
                    

                    for s in deg['subjects']:
                        sub.append(s['subjcode']) # para asa ning sub nga list ?


                    # Determining the Weight of Every Subjects in the Degree
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

                        
                    current_courses = [] # specific courses nga iyang makuha for that specific nga sem
                    for subject in deg['subjects']:
                        semsy = db.session.query(CurriculumDetails.curriculum_year,CurriculumDetails.curriculum_sem).filter(CurriculumDetails.subjcode == subject['subjcode']).filter(CurriculumDetails.curriculum_id == Curriculum.curriculum_id).filter(Curriculum.progcode==prog).first()

                        if semsy is not None and semsy.curriculum_sem == current_sem.sem:
                            if subject['prereq'] in psubjs or subject['prereq'] == 'None':
                                if subject['subjcode'] not in psubjs:
                                    current_courses.append(subject)
                                    # courses.sort(key = lambda i:i['weight'], reverse = True)/ayaw sa ni idelete
                                    current_courses.sort(key = lambda i:(i['unit'], i['weight']), reverse = True)
                                    

                    ##  Per sem: the subjects that the students can take (based on the unit they need to take)
                    specific_courses = {}
                    ss_subjects = []
                    totalunit_sc = 0  # Total unit for specific courses

                    for c in current_courses:
                        if latestsemstud.scholasticstatus == 'Regular':
                            totalunit_sc += c['unit']
                            ss_subjects.append(c)

                        if latestsemstud.scholasticstatus == 'Warning':
                            totalunit_sc += c['unit']
                            if totalunit_sc <= 17:
                                ss_subjects.append(c)
                            else:
                                totalunit_sc -= c['unit']
                                
                        if latestsemstud.scholasticstatus == 'Probation':
                            totalunit_sc += c['unit']
                            if totalunit_sc <= 12:
                                ss_subjects.append(c)
                            else:
                                totalunit_sc -= c['unit']

                    specific_courses.update({'current_sem': str(current_sem.sem), 'specific_subjects': ss_subjects})


                    # For Remaining Courses
                    remaining_courses = []
                    for s in deg["subjects"]:

                        if s not in passedsubjs and s not in ss_subjects:
                            remaining_courses.append(s)
                            remaining_courses.sort(key = lambda i:(i['weight']), reverse = True)
                            # print(s['subjcode'])
                        

                    ## Departmental Constraints
                    ## Checking if every departmental constraints has been satisfied (status=0 is not otherwise : 1)
                    if degreeparsed == 'BSN':
                        if latestsemstud.gpa > float(2.0):
                            # print('BSEdMath and BSEdPhysics')
                            deg.update({'status': 0})
                        

                    if degreeparsed == 'BSEdMath' or degreeparsed == 'BSEdPhysics':
                        if residency >= 1:
                            patterned = re.compile(r'(ELC|SED|EDM|CPE)(\d{3}|\d{3}.\d{1})')
                            edsubjs = list(filter(patterned.match, passedsubjcodes))
                            if edsubjs == []:
                                deg.update({'status': 0})
                        else:
                            deg.update({'status': 1})
                            

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
                                deg.update({'status': 0})
                            

                    if degreeparsed == 'BSEE' or degreeparsed == 'BSCpE':
                        for passed in passedsubjs:
                            if passed['subjcode'] != 'MAT060' and current_sem.sem != '1': #note: mkashift ra ani every 1st sem sa school year
                                deg.update({'status': 0})
                            


                    if degreeparsed == 'BSPsych':
                        if latestsemstud.gpa > float(1.75):
                            for passed in psubjs:
                                pparsed = passed.rstrip()
                            
                                if pparsed == 'PSY100':
                                    deg.update({'status': 0})

                    # passedandspecific subjects to be minus sa deg['subjects']
                    passedandspecific = passedsubjs + ss_subjects
                    

                    # for loop para ma remove and mga subjects sa deg['subjects'] gamit ang passedandspecific
                    for pands in passedandspecific:
                        for j in range(len(deg['subjects'])):
                            if deg['subjects'][j]['subjcode'] == pands['subjcode']: 
                                del deg['subjects'][j]
                                break

                    total_units = 0
                    for s in deg['subjects']:
                        total_units = total_units + s['unit']

                    # butangan ang degress ug 'specific_courses' nga key and total units
                    total_units += total_units + totalunit_sc

                    deg.update({'total_units': float(total_units), 'specific_courses': specific_courses, 'passedsubjs': psubjs, 'residency': int(residency)})

                    deg['subjects'].sort(key = lambda i:(i['weight'], i['unit']), reverse = True)

                    unit = 0
                    ss_subjects = []
                    tempres = 0

        # ang nabilin nga deg['subjects'] kay mao ang remaining subjects
    return degrees

    

class DegreeSolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, degrees, bool_res, progs, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._degrees = degrees
        self._bool_res = bool_res
        self._progs = progs
        self._solutions = set(sols)
        self._solution_count = 0
        self._container = []

    def on_solution_callback(self):
        if self._solution_count in self._solutions:
            for d in self._degrees:
                if self.Value(self._bool_res[(d['DegreeName'])]):
                    for s in d['subjects']:
                        s.update({'unit': float(s['unit'])}) 

                    for s in d['specific_courses']['specific_subjects']:
                        s.update({'unit': float(s['unit'])})

                    self._container.append(d)
                    # pass

        self._solution_count += 1

        return self._container
        

    def solution_count(self):
        return self._solution_count



def main():
            ### model
    model = cp_model.CpModel()

    bool_res = {}

    var_datas = datas()
    var_constraints = constraints(var_datas[0], var_datas[1], var_datas[2], var_datas[3], var_datas[4], var_datas[5], var_datas[6], var_datas[7], var_datas[8], var_datas[9], var_datas[10], var_datas[11])
    

    for p in var_datas[8]:
        bool_res[(p)] = model.NewBoolVar('%s' % (p))

    for deg in var_constraints:
        if deg['status'] == 1:
            model.Add(bool_res[(deg['DegreeName'])] == 1)

    # # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    
    # # # # Display the first five solutions.
    a_few_solutions = range(1)
    solution_printer = DegreeSolutionPrinter(var_constraints, bool_res, var_datas[8], a_few_solutions)
    status = solver.SearchForAllSolutions(model, solution_printer)

    # return data to be process in UI
    return solution_printer._container