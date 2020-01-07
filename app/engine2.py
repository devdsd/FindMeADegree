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

                # Local Lists
    maxyear = 6
    unit = 0
    # degrees = []
    passedsubjs = []
    passedsubjslist = []
    passedsubjcodes = []
    failedsubjs = []
    failedsubjslist = []
    failedsubjcodes = []
    subjectsinformations = []
    subjectsindegree = []
    gpas = []

    # degrees = ['BSA', 'BSCS']
    ## TRIAL
    degree_program_dict = {}
    
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

    
    test2 = []
    for prog in progs:
        test = {}
        if prog == student_program:
            pass
        
        else:
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
                
                test.update({'degree': prog, 'subjects': subjectsindegree})
        test2.append(test)

        return test2

        # degree_program_dict['DEGREE_NAME'] = deg
        # degree_program_dict['subjs'] = subjectsindegree
 
    # return residency, maxyear, unit, degrees, passedsubjs, passedsubjslist, passedsubjcodes, failedsubjs, failedsubjslist, failedsubjcodes, subjectsinformations, degree_program_dict, lateststudent_record


#note: current modification here

def constraints(residency, maxyear, unit, degrees, passedsubjs, passedsubjslist, passedsubjcodes, failedsubjs, failedsubjslist, failedsubjcodes, subjectsinformations, degree_program_dict, lateststudent_record):

            ### model
    model = cp_model.CpModel()
    
    prog_bool = {}

    output = {}

            ### student cannot shift if MRR ###

    if residency > maxyear:
        print("Cannot shift!")

    ## student cannot shift when have 4 or greater failing grades in current sem
    countfail = 0
    for fail in failedsubjslist:
        if fail.sy == lateststudent_record.sy and fail.sem == lateststudent_record.sem:
            countfail += 1
                
    if countfail > 4:
        print("Cannot shift!")
    
    ### General Constraints
    psubjs = []
    for p in passedsubjs:
        psubjs.append(p['subjcode'])

    sub = []
    for deg in degree_program_dict:
        for s in deg[1]:
            sub.append(s['subjcode'])

        for s in deg[1]:
            preqs = db.session.query(Prerequisite.subjcode).filter(Prerequisite.subjcode == s).all()
            position, subjectWeight = 0, 0
            queriedSubjects = []
            queriedSubjects.append([s])
            
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

        for subject in deg[1]:
            semsy = db.session.query(CurriculumDetails.curriculum_year,CurriculumDetails.curriculum_sem).filter(CurriculumDetails.subjcode == subject['subjcode']).filter(CurriculumDetails.curriculum_id == Curriculum.curriculum_id).filter(Curriculum.progcode == 
            prog).first()

            if semsy is not None and semsy.curriculum_year <= studlevel and semsy.curriculum_sem == current_sem.sem:
                if subject['subjcode'] not in psubjs:
                        courses.append(subject)
                        courses.sort()

        specific_courses = []

        for  c in courses:
            if lateststudent_record.scholasticstatus == 'Warning':
                unit += c['unit']
                if unit <= 17:
                    specific_courses.append(c)
                    
            if lateststudent_record.scholasticstatus == 'Probation':
                unit += c['unit']
                if unit <= 12:
                    specific_courses.append(c)
                    
            if lateststudent_record.scholasticstatus == 'Regular':
                unit += c['unit']
                specific_courses.append(c)

        coursestaken = passedsubjs + specific_courses


        remaincourses = []
        for s in deg[1]:
            if s in coursestaken:
                pass
            else:
                remaincourses.append(s)
        output['degree'] = deg['degname']
        output['remaining_subjs'] = remaincourses
        



    # for deg in degrees:
    #     prog_bool[(deg)] = model.NewBoolVar('%s' % prog)


    # for deg in degrees:
          
    #                 ## Department Constraints
    #     for passed in passedsubjs:
    #         if prog == 'BSN':
    #             if semstudent2.gpa > 2.0:
    #                 model.Add(prog != 'BSN')


    #         if prog == 'BSEdMath' or prog == 'BSEdPhysics':
    #             if residency == 2:
    #                 patterned = re.compile(r'(ELC|SED|EDM|CPE)(\d{3}|\d{3}.\d{1})')
    #                 edsubjs = list(filter(patterned.match, passedsubjcodes))
    #                 if not edsubjs:
    #                     model.Add(prog != 'BSEdMath')
    #                     model.Add(prog != 'BSEdPhysics')


    #         if prog == 'BSMath' or prog == 'BSStat':
    #             patternms = re.compile(r'(MAT|STT)(\d{3}|\d{3}.\d{1})')
    #             mssubjs = list(filter(patternms.match, passedsubjcodes))
    #             mssubjsinfo = []
    #             for ms in mssubjs:
    #                 if passed['subjcode'] == ms:
    #                     mssubjsinfo.append(passed)
    #             for msinfo in mssubjsinfo:
    #                 if (msinfo['grade'] > '2.5'): ## if grades sa Math ug stat lapas sa 2.5
    #                     model.Add(prog != 'BSMath')
    #                     model.Add(prog != 'BSStat')
        

    #         if prog == 'BSCS':
    #             patterncs = re.compile(r'(MAT|STT|CSC|CCC)(\d{3}|\d{3}.\d{1})')
    #             csubjs = list(filter(patterncs.match, passedsubjcodes))
    #             cssubjsinfo = []
    #             for cs in csubjs:
    #                 if passed['subjcode'] == cs:
    #                     cssubjsinfo.append(passed)
    #             for csinfo in cssubjsinfo:
    #                 if(csinfo['grade'] > '2.5'):## if grades sa math,stat, ug cs lapas sa 2.5
    #                     model.Add(prog != 'BSCS')


    #         if prog == 'BSEE' or prog == 'BSCpE':
    #             if passed['subjcode'] != 'MAT060' and current_sem.sem != 1: #note: mkashift ra ani every 1st sem sa school year
    #                 model.Add(prog != 'BSEE')
    #                 model.Add(prog != 'BSCpE')


    #         if prog == 'BSPsych':
    #             if passed.subjcode != 'PSY100':
    #                 if semstudent2.gpa > 1.75:
    #                     model.Add(prog != 'BSPsych')

                
        # dictoutput.update({'prog': prog})
        # dictoutput['remaining'] = remaincourses

    return output
    

def main():
    var_datas = datas()
    # var_constraints = constraints(var_datas[0], var_datas[1], var_datas[2], var_datas[3], var_datas[4], var_datas[5], var_datas[6], var_datas[7], var_datas[8], var_datas[9], var_datas[10], var_datas[11], var_datas[12])

    # for i in var_datas[11]:
    #     print(i[0])
    #     print(i[1])

    print(var_datas)

    #solver
    solver = cp_model.CpSolver()

    # solution_printer = FindMeADegreeSolutionPrinter()

    # solver.SearchForAllSolutions(model, solution_printer)