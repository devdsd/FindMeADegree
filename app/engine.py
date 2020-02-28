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

    residency = residency - 1
    passedsubjslist = []
    passedsubjcodes = []
    failedsubjslist = []
    failedsubjcodes = []
    subjectsinformations = []
    subjectsindegree = []
    gpas = []
    degrees = []


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
    
    for prog in progs:
        
        degreeinfo = {}
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
        degreeinfo['status'] = 1
        subjectsindegree = []
        degrees.append(degreeinfo)

        passedsubjs = []
        failedsubjs = []
        sub = []
        for deg in degrees:
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
    return degrees, failedsubjslist, lateststudent_record, residency, student_program, current_sem, passedsubjs, progs


def constraints(degrees, fail_subjects, lateststudent_record, residency, current_degree, current_sem, passed_subjects):
    maxyear = 6
    countfail = 0
    psubjs = []
    for p in passed_subjects:
        psubjs.append(p['subjcode'])

    if residency > maxyear:
        print('Cant')
    for f in fail_subjects:
        if f.sy == lateststudent_record.sy and f.sem == lateststudent_record.sem:
            countfail += 1
            if countfail > 4:
                print("Cannot shift!")
    for d in degrees:
        if d['DegreeName'] == current_degree:
            d.update({'status': 0})
            pass
        else:
            progs = db.session.query(Program.progcode).all()
            for p in progs:
                if d['DegreeName'] == p:
                    degree = str(p[0])
                    degreeparsed = degree.rstrip()

                    if degreeparsed == 'BSN':
                        print('BSN')
                        if lateststudent_record.gpa > float(2.0):
                            d.update({'status': 0})
                    if degreeparsed == 'BSEdMath' or degreeparsed == 'BSEdPhysics':
                        print('BSEdMath and BSEdPhysics')
                        if residency >= 1:
                            patterned = re.compile(r'(ELC|SED|EDM|CPE)(\d{3}|\d{3}.\d{1})')
                            edsubjs = list(filter(patterned.match, psubjs))
                            if edsubjs == []:
                                d.update({'status': 0})
                    if degreeparsed == 'BSCS':
                        print("BSCS")
                        for passed in passed_subjects:
                            patterncs = re.compile(r'(MAT|STT|CSC|CCC)(\d{3}|\d{3}.\d{1})')
                            csubjs = list(filter(patterncs.match, psubjs))
                            cssubjsinfo = []
                            for cs in csubjs:
                                if passed['subjcode'] == cs:
                                    cssubjsinfo.append(passed)
                            counter = 0
                            for csinfo in cssubjsinfo:
                                if(csinfo['grade'] > '2.5'):
                                    counter += 1
                            if counter != 0:
                                d.update({'status': 0})
                    if degreeparsed == 'BSMath' or degreeparsed == 'BSStat':
                        print ("MathStat")
                        for passed in passed_subjects:
                            patternms = re.compile(r'(MAT|STT)(\d{3}|\d{3}.\d{1})')
                            mssubjs = list(filter(patternms.match, psubjs))
                            mssubjsinfo = []
                            for ms in mssubjs:
                                if passed['subjcode'] == ms:
                                    mssubjsinfo.append(passed)
                            counter = 0
                            for msinfo in mssubjsinfo:
                                if (msinfo['grade'] > '2.5'):
                                    counter += 1
                            if counter != 0:
                                d.update({'status': 0})
                            

                    if degreeparsed == 'BSEE' or degreeparsed == 'BSCpE':
                        print('BSEE and BSCpE')
                        for passed in passed_subjects:
                            if passed['subjcode'] != 'MAT060' and current_sem.sem != '1': #note: mkashift ra ani every 1st sem sa school year
                                d.update({'status': 0})

                    if degreeparsed == 'BSPsych':
                        print("Psych")
                        if lateststudent_record.gpa > float(1.75):
                            for passed in psubjs:
                                pparsed = passed.rstrip()
                            if pparsed == 'PSY100':
                                d.update({'status': 0})
                

        


    return degrees

# def gen_constraints(degrees):
#     year = range(1,5)
#     sem = range(1,4)
#     res = []
#     for y in year:
#         for s in sem:
#             for d in degrees:
#                 r = course(d, str(s))
#                 res.append(r)
#     return degrees



def course(degrees, sem, passed_subjects):
    courses = []
    psubjs = []
    for p in passed_subjects:
        psubjs.append(p['subjcode'])
    for d in degrees['DegreeName']:
        print(str(d['DegreeName']) + '\n')
        for subject in degrees['subjects']:
            semsy = db.session.query(CurriculumDetails.curriculum_year,CurriculumDetails.curriculum_sem).filter(CurriculumDetails.subjcode == subject['subjcode']).filter(CurriculumDetails.curriculum_id == Curriculum.curriculum_id).filter(Curriculum.progcode == 
            d).first()

            
            if semsy is not None and semsy.curriculum_sem == sem:
                if subject['prereq'] in psubjs or subject['prereq'] == 'None':
                    # print("Prereq:" + subject['prereq'] + "Subject:" + subject['subjcode'])
                    if subject['subjcode'] not in psubjs:
                        # print ("subject['subjcode']" + "not in psubjs -> ", subject['subjcode'], subject['subjcode'] not in psubjs)
                        courses.append(subject)
                        # courses.sort(key = lambda i:i['weight'], reverse = True)/ayaw sa ni idelete
                        courses.sort(key = lambda i:(i['unit'], i['weight']), reverse = True)
    return courses

def specificcourses(courses,lateststudent_record):
    specific_courses = []
    unit = 0

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
    unit = 0
    return specific_courses

    
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
                d2 = str(d['DegreeName'])
                d3 = re.findall(r"(\w+|\w+-\w+)", d2)
                dparsed = str(d3[1])
                # print(dparsed)
                # print(self._bool_res[(d['DegreeName'])])
                if self.Value(self._bool_res[(d['DegreeName'])]):
        #         if self.Value(self._bool_res[(dparsed)]):
                    print('{} is recommended'.format(dparsed))
                    # self._container.append(dparsed)
                else:
                    pass
        self._solution_count += 1
        
        

    def solution_count(self):
        return self._solution_count
            


def main():
    model = cp_model.CpModel()
    bool_res = {}
    data = datas()
    con = constraints(data[0],data[1],data[2],data[3],data[4],data[5],data[6])
    prog = []
    for c in con:
        prog.append(c['DegreeName'])

    for p in prog:
        bool_res[(p)] = model.NewBoolVar('%s' % (p))
        
    for d in con:
        if d['status'] == 1:
            model.Add(bool_res[(d['DegreeName'])] == 1)

    # # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    
    # # # Display the first five solutions.
    a_few_solutions = range(1)
    solution_printer = DegreeSolutionPrinter(con, bool_res, data[7], a_few_solutions)
    solver.SearchForAllSolutions(model, solution_printer)
        



    # gcon = gen_constraints(con[0])
    courses = course(data[0], data[5], data[6])