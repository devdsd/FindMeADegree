from __future__ import division
from __future__ import print_function
from app.models import *
from ortools.sat.python import cp_model
import re


def datas():
                # Querying data from the database #
        semstudent = SemesterStudent.query.filter_by(studid=current_user.studid).first()
        sems = db.session.query(Registration.sem).filter_by(studid=current_user.studid).group_by(Registration.sem).all()
        listgpas = db.session.query(SemesterStudent.studid, SemesterStudent.gpa, SemesterStudent.sy, SemesterStudent.sem).filter_by(studid=current_user.studid).all()
        residency = db.session.query(SemesterStudent.sy).filter_by(studid=current_user.studid).distinct().count()
        progs = db.session.query(Program.progcode).all()
        ssubjects = db.session.query(Subject.subjcode, Subject.subjdesc, Subject.subjcredit, Subject.subjdept).all()
        # subjecthistories = db.session.query(Registration.studid, Registration.sem, Registration.sy, Registration.subjcode, Registration.grade, Registration.section, Subject.subjdesc).filter(Registration.studid==current_user.studid).filter(Registration.subjcode==Subject.subjcode).all()
        # prereqs = db.session.query(Prerequisite.subjcode, Prerequisite.prereq).all()

        return semstudent, sems, listgpas, residency, progs, subjects 


def main():
        datas = datas()

        gpas = []
        
        for gpa in datas.listgpas:
                gpas.append(gpa.gpa)

        cgpa = 0.0
        count = 0
        
        for gpa in gpas:
                if gpa is not None:
                        cgpa = cgpa + float(gpa)
                        count = count + 1

        cgpa = cgpa/float(count)


                ### model
        model = cp_model.CpModel()

                ### variables
        maxyear = 6
        degrees = []
        passedsubjs = []
        passedsubjslist = []
        failedsubjs = []
        failedsubjslist = []
        subjectsinformations = []
        subjectsindegree = []


        for s in subjects:
                preq = db.session.query(Prerequisite.prereq).filter(Prerequisite.subjcode==s.subjcode).first()
                if preq is not None:
                        entry1 = {
                                'subjcode': s.subjcode,
                                'subjdesc': s.subjdesc,
                                'unit': s.subjcredit,
                                'prereq': preq[0]
                        }
                else:
                        entry1 = {
                                'subjcode': s.subjcode,
                                'subjdesc': s.subjdesc,
                                'unit': s.subjcredit,
                                'prereq': "None"
                        }   
                subjectsinformations.append(entry1)


        for subj in subjectsinformations:
                q = Registration.query.filter(Registration.subjcode==subj['subjcode']).filter(Registration.studid==current_user.studid).first()
                if q is not None:
                        if q.grade != '5.0':
                                passedsubjs.append(subj)
                                passedsubjslist.append(q)
                        else:
                                failedsubjs.append(subj)
                                failedsubjslist.append(q)

        ### student cannot shift if MRR
        model.Add(residency < maxyear)

        ## student cannot shift when have 4 or greater failing grades in current sem
        countfail = 0
        for fail in failedsubjslist:
                if fail.sy and fail.sem:
                        countfail += 1
                        
        model.Add(countfail < 4)

        #student cannot shift when having 2 consecutive probation status
        model.Add()


        for prog in progs:
                model.Add(prog != semstudent.studmajor)

                        ##Department Constraints
                for passed in passedsubjs:
                        if prog == 'BSN':
                                if semstudent.gpa > 2.0:
                                        model.Add(prog != 'BSN')


                        if prog == 'BSEdMath' or prog == 'BSEdPhysics':
                                if residency == 2:
                                        patterned = re.compile(r'(ELC|SED|EDM|CPE)(\d{3}|\d{3}.\d{1})')
                                        edsubjs = list(filter(patterned.match, passedsubjcodes))
                                        if not edsubjs:
                                                model.Add(prog != 'BSEdMath')
                                                model.Add(prog != 'BSEdPhysics')

                        if prog == 'BSMath' or prog == 'BSStat':
                                patternms = re.compile(r'(MAT|STT)(\d{3}|\d{3}.\d{1})')
                                mssubjs = list(filter(patternms.match, passedsubjcodes))
                                mssubjsinfo = []
                                for ms in mssubjs:
                                        if passed.subjcode == ms:
                                                mssubjsinfo.append(passed)
                                for msinfo in mssubjsinfo:
                                        if  (msinfo.grades > '2.5'): ## if grades sa Math ug stat lapas sa 2.5
                                                model.Add(prog != 'BSMath')
                                                model.Add(prog != 'BSStat')
                        
                        if prog == 'BSCS':
                                patterncs = re.compile(r'(MAT|STT|CSC|CCC)(\d{3}|\d{3}.\d{1})')
                                csubjs = list(filter(patterncs.match, passedsubjcodes))
                                cssubjsinfo = []
                                for cs in csubjs:
                                        if passed.subjcode == cs:
                                                cssubjsinfo.append(passed)
                                for csinfo in cssubjsinfo:
                                        if(csinfo.grades > '2.5'):## if grades sa math,stat, ug cs lapas sa 2.5
                                                model.Add(prog != 'BSCS')

                        if prog == 'BSEE' or prog == 'BSCpE':
                                if passed.subjcode != 'MAT060' and sem != 1: #note: mkashift ra ani every 1st sem sa school year
                                        model.Add(prog != 'BSEE')
                                        model.Add(prog != 'BSCpE')

                        if prog == 'BSPsych':
                                if passed.subjcode != 'PSY100':
                                        if semstudent.gpa > 1.75:
                                                model.Add(prog != 'BSPsych') 
                        

                        for s in subjectsinformations:
                                q = db.session.query(Curriculum.progcode, CurriculumDetails.curriculum_year, CurriculumDetails.curriculum_sem).filter(Curriculum.curriculum_id==CurriculumDetails.curriculum_id).filter(CurriculumDetails.subjcode==s['subjcode']).filter(Curriculum.progcode==prog).first()
                                
                                if q is not None:
                                subjectsindegree.append(s)
                        

                        # for s in subjectsindegree:
                        #         if (s.subjcode == passed.subjcode):
                        #                 returnsubjs.append(s)
                
                # for returns in returnsubjs:
                #         subjectsindegree.remove(returns)


                # for pre in prereqs:
                #         for sb in subjectsindegree:
                #                 for passed in passedsubjs:    
                #                         if pre.prereq == sb.subjcode:
                #                                 if pre.prereq == passed.subjcode:
                #                                         print "Subject: " + str(pre.subjcode) + "   Pre-requisite: " + str(pre.prereq)
                #                                 else:
                #                                         pass


        #solver
        solver = cp_model.CpSolver()
