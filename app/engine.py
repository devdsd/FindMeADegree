from __future__ import division
from __future__ import print_function
from app.models import *
from ortools.sat.python import cp_model
import re

           

def main():

                 # Querying data from the database #
        semstudent = SemesterStudent.query.filter_by(studid=current_user.studid).first()

        subjecthistories = db.session.query(Registration.studid, Registration.sem, Registration.sy, Registration.subjcode, Registration.grade, Registration.section, Subject.subjdesc).filter(Registration.studid==current_user.studid).filter(Registration.subjcode==Subject.subjcode).all()

        sems = db.session.query(Registration.sem).filter_by(studid=current_user.studid).group_by(Registration.sem).all()

        listgpas = db.session.query(SemesterStudent.studid, SemesterStudent.gpa, SemesterStudent.sy, SemesterStudent.sem).filter_by(studid=current_user.studid).all()

        residency = db.session.query(SemesterStudent.sy).filter_by(studid=current_user.studid).distinct().count()

        progs = db.session.query(Program.progcode).all()

        prereqs = db.session.query(Prerequisite.subjcode, Prerequisite.prereq).all()

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


                ### model
        model = cp_model.CpModel()

                ### variables
        maxyear = 6
        degrees = []
        passedsubjs = []
        failedsubjs = []
        passedsubjcodes = []
        returnsubjs = []

        for sh in subjecthistories:
                if (sh.grade != '5.0'):
                        passedsubjs.append(sh)
                else:
                        failedsubjs.append(sh)

        for extract in passedsubjs:
                passedsubjcodes.append(extract.subjcode)

        ### student cannot shift if MRR
        model.Add(residency < maxyear)

        ## student cannot shift when have 4 or greater failing grades in current sem
        countfail = 0
        for fail in failedsubjs:
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
                        

                        subjectsindegree = db.session.query(CurriculumDetails.subjcode, Subject.subjdesc, Subject.subjcredit).filter(CurriculumDetails.curriculum_id==Curriculum.curriculum_id).filter(Curriculum.progcode==prog).filter(CurriculumDetails.subjcode==Subject.subjcode).all()
                        

                        for s in subjectsindegree:
                                if (s.subjcode == passed.subjcode):
                                        returnsubjs.append(s)
                
                for returns in returnsubjs:
                        subjectsindegree.remove(returns)


                for pre in prereqs:
                        for sb in subjectsindegree:
                                for passed in passedsubjs:    
                                        if pre.prereq == sb.subjcode:
                                                if pre.prereq == passed.subjcode:
                                                        print "Subject: " + str(pre.subjcode) + "   Pre-requisite: " + str(pre.prereq)
                                                else:
                                                        pass


        #solver
        solver = cp_model.CpSolver()
