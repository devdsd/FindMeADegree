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

    return semstudent2, sems, residency, progs,subjects, studlevel, student_program, lateststudent_record, current_sem

def data_lists(semstudent,sems,residency,progs,subjects,studlevel,student_program,lateststudent_record,current_sem):
    print ("hey datalist")
    passedsubjslist = []
    failedsubjslist = []
    subjectsinformations = []
    subjectsindegree = []
    gpas = []
    degrees = []
    sub = []
    

    for s in subjects:
        entry = {
            'subjcode': s.subjcode,
            'subjdesc': s.subjdesc,
            'unit': s.subjcredit
        } 

        subjectsinformations.append(entry)
    
    for prog in progs:
        
        degreeinfo = {}
        passedsubjs = []
        failedsubjs = []
        psubjs = []

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

        for d in degrees:
            if d['DegreeName'] == prog:

                for subj in d['subjects']:
                    q = Registration.query.filter(Registration.subjcode==subj['subjcode']).filter(Registration.studid==current_user.studid).first()
                    
                    if q is not None:
                        if q.grade != '5.0':
                            subj.update({'grade': q.grade})
                            passedsubjslist.append(q)
                            passedsubjs.append(subj)
                            
                        else:
                            subj.update({'grade': q.grade})
                            failedsubjslist.append(q)
                            failedsubjs.append(subj)
                    else:
                        subj.update({'grade': None})


                
                for p in passedsubjs:
                    psubjs.append(p['subjcode'])
                
                for s in d['subjects']:
                    sub.append(s['subjcode'])
            
                
                for s in d['subjects']:
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

    return degrees, failedsubjslist, psubjs, passedsubjs


def main_cons(degrees, prog, current_degree, residency, fail_subjects, lateststudent_record):
    print("mcon yeah")
    maxyear = 6

    if residency > maxyear:
        countfail = 0
        for f in fail_subjects:
            if f.sy == lateststudent_record.sy and f.sem == lateststudent_record.sem:
                countfail += 1
                if countfail > 4:
                    print("Cannot shift!")
    else:      
        for d in degrees:
            for di in d['DegreeName']:
            
                if d['DegreeName'] == current_degree:
                    degrees.remove(d)
                    pass
                else:
                    d['status'] = 1
                    # print()
                    # print("Degree:" + str(d['DegreeName'])+ " " + "status:" + str(d['status']))

            #         #call other functions
    return degrees

def dept_cons(degrees ,residency, lateststudent_record, passedsubjs, psubjs):
    progs = db.session.query(Program.progcode).all()
    for d in degrees:
        for p in progs:
            deg = str(p[0])
            degreeparsed = deg.rstrip()

            

            if degreeparsed == 'BSN':
                if lateststudent_record.gpa > float(2.0):
                    # print('BSEdMath and BSEdPhysics')
                    d.update({'status': 0})
                
            if degreeparsed == 'BSEdMath' or degreeparsed == 'BSEdPhysics':
                if residency >= 2:
                    patterned = re.compile(r'(ELC|SED|EDM|CPE)(\d{3}|\d{3}.\d{1})')
                    edsubjs = list(filter(patterned.match, psubjs))
                    # print('BSEdMath and BSEdPhysics')
                    if edsubjs == []:
                        d.update({'status': 0})
                    

            # if degreeparsed == 'BSMath' or degreeparsed == 'BSStat':
            #     for passed in passedsubjs:
            #         patternms = re.compile(r'(MAT|STT)(\d{3}|\d{3}.\d{1})')
            #         mssubjs = list(filter(patternms.match, psubjs))
            #         mssubjsinfo = []
            #         for ms in mssubjs:
            #             if passed['subjcode'] == ms:
            #                 mssubjsinfo.append(passed)
            #         counter = 0
            #         for msinfo in mssubjsinfo:
            #             if (msinfo['grade'] > '2.5'):
            #                 counter += 1
            #         if counter != 0:
            #             # print ("MathStat")
            #             d.update({'status': 0})
                

            # if degreeparsed == 'BSCS':
            #     for passed in passedsubjs:
            #         patterncs = re.compile(r'(MAT|STT|CSC|CCC)(\d{3}|\d{3}.\d{1})')
            #         csubjs = list(filter(patterncs.match, psubjs))
            #         cssubjsinfo = []
            #         for cs in csubjs:
            #             if passed['subjcode'] == cs:
            #                 cssubjsinfo.append(passed)
            #         counter = 0
            #         for csinfo in cssubjsinfo:
            #             if(csinfo['grade'] > '2.5'):## if grades sa math,stat, ug cs lapas sa 2.5
            #                 counter += 1
            #         if counter != 0:
            #             # print("BSCS ni Siya!!")
            #             d.update({'status': 0})
                    

            if degreeparsed == 'BSEE' or degreeparsed == 'BSCpE':
                for passed in passedsubjs:
                    if passed['subjcode'] != 'MAT060' and current_sem.sem != 1: #note: mkashift ra ani every 1st sem sa school year
                        # print('BSEE and BSCpE')
                        d.update({'status': 0})
                    


            if degreeparsed == 'BSPsych':
                if lateststudent_record.gpa > float(1.75):
                    for passed in psubjs:
                        pparsed = passed.rstrip()
                    
                    if pparsed == 'PSY100':
                        # print("Psych ni siya")
                        d.update({'status': 0})

    for d in degrees:
        print (d['DegreeName'])
        print(d['status'])        
            
    
    return degrees

def main():
    data = datas()
    d_list = data_lists(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8])
    mcon = main_cons(d_list[0], data[3],data[6],data[2], d_list[1], data[7])
    deptcon = dept_cons(mcon[0], data[2], data[7], d_list[2], d_list[3])

    # print (deptcon[0])
    # f = mcon
    
    # for i in f:
    #    print(i['DegreeName'])
    #    print(i['status'])

    # r = deptcon
    # # print (r)
    # for r in r:
    #     print (r['DegreeName'])
    #     print(r['status'])






