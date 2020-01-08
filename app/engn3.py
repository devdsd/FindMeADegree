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
    student_program = db.session.query(Program.progcode).filter_by(progcode=semstudent.studmajor).first()
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

    test = {}
    test2 = []
    
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
        
        # res.update({'Degree': prog})
        # res.update({'Program of Study': subjectsindegree})

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

        
        test['DegreeName'] = prog
        test['subjects'] = subjectsindegree
        subjectsindegree = []
        test2.append(test)
        test = {}
        ### Note: Tiwason, passedsubjects problem
        print("Prog: " + str(prog))
        for p in passedsubjs:
            print (p['subjcode']

    return residency, maxyear, unit, passedsubjs, passedsubjslist, passedsubjcodes, failedsubjs, failedsubjslist, failedsubjcodes, subjectsinformations, lateststudent_record, test2, progs, studlevel, current_sem
    

def constraints(residency, maxyear, unit, passedsubjs, passedsubjslist, passedsubjcodes, failedsubjs, failedsubjslist, failedsubjcodes, subjectsinformations, lateststudent_record, test2, progs, studlevel, current_sem):
    
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
    
    # print (psubjs)

    sub = []
    # specific_courses = []
    for deg in test2:
        for prog in progs:
            if deg['DegreeName'] == prog:
                print (prog)
                for s in deg['subjects']:
                    # print (p['subjcode'])
                    sub.append(s['subjcode'])

                for s in deg['subjects']:
                    preqs = db.session.query(Prerequisite.subjcode).filter(Prerequisite.subjcode == s['subjcode']).all()
                    position, subjectWeight = 0, 0
                    queriedSubjects = []
                    queriedSubjects.append([s['subjcode']])

                    # print (queriedSubjects)
                    
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

                    # print (str(s['subjcode']) + "    " + str(s['weight']))

                courses = []
                for subject in deg['subjects']:
                    semsy = db.session.query(CurriculumDetails.curriculum_year,CurriculumDetails.curriculum_sem).filter(CurriculumDetails.subjcode == subject['subjcode']).filter(CurriculumDetails.curriculum_id == Curriculum.curriculum_id).filter(Curriculum.progcode == 
                    prog).first()

                    if semsy is not None and semsy.curriculum_year <= studlevel and semsy.curriculum_sem == current_sem.sem:
                        if subject['subjcode'] not in psubjs:
                                courses.append(subject)
                                courses.sort(key = lambda i:i['weight'], reverse = True)

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
                
                # for p in specific_courses:
                #     print("Unit: " + str(p['unit']) + "Subject: " + str(p['subjcode']))
                # unit = 0
                # specific_courses = []
                
                
                coursestaken = passedsubjs + specific_courses
                
            

                # remaincourses = []
                # for s in deg["subjects"]:
                #     if s not in coursestaken:
                #         remaincourses.append(s)

                # print("Remaining Courses to be taken for this degree: " + str(prog))
                # for p in remaincourses:
                #     print("Subjcode: " + str(p['subjcode']))

                unit = 0
                specific_courses = []
                remaincourses = []


            
    
def main():
    var_datas = datas()
    # var_constraints = constraints(var_datas[0], var_datas[1], var_datas[2], var_datas[3], var_datas[4], var_datas[5], var_datas[6], var_datas[7], var_datas[8], var_datas[9], var_datas[10], var_datas[11], var_datas[12],var_datas[13],var_datas[14])
    
    # var_constraints
    var_datas

    

