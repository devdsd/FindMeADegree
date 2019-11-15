# from app.sample import VarArraySolutionPrinter
from app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from app.models import *
from app.forms import *
from flask_login import login_user, current_user, logout_user, login_required
import re

@app.route('/')
@app.route('/home')
@login_required
def home():
    student = Student.query.filter_by(studid=current_user.studid).first()
    semstudent = SemesterStudent.query.filter_by(studid=student.studid).first()
    semstudent2 = db.session.query(SemesterStudent.studid, SemesterStudent.sy, SemesterStudent.studlevel, SemesterStudent.sem, SemesterStudent.scholasticstatus).filter_by(studid=current_user.studid).all()
    residency = db.session.query(SemesterStudent.sy).filter_by(studid=current_user.studid).distinct().count()
    studlevel = semstudent2[-1].studlevel
    student_program = Program.query.filter_by(progcode=semstudent.studmajor).first()

    # Practice
    lateststudent_record = semstudent2[-1]
    subjects = db.session.query(Subject.subjcode, Subject.subjdesc, Subject.subjcredit, Subject.subjdept).all()
    preqs = db.session.query(Prerequisite.subjcode, Prerequisite.prereq).all()
    curr = db.session.query(CurriculumDetails.subjcode).filter(CurriculumDetails.curriculum_id==Curriculum.curriculum_id).filter(Curriculum.progcode==semstudent.studmajor).all()

    # for c in curr:
    #     print c

    # subjecthistories = db.session.query(Registration.studid, Registration.sem, Registration.sy, Registration.subjcode, Registration.grade, Registration.section, Subject.subjdesc).filter(Registration.studid==current_user.studid).filter(Registration.subjcode==Subject.subjcode).all()

    current_sem = db.session.query(Semester.sy, Semester.sem).filter(Semester.is_online_enrollment_up==True).first()
    

    subjectsinformations = []
    passedsubjs = []
    failedsubjs = []
    subjectsindegree = []

    for s in subjects:
        
        # preq = db.session.query(Prerequisite.prereq).filter(Prerequisite.subjcode==s.subjcode).first()

        # if preq is not None:
            # entry1 = {
            #     'subjcode': s.subjcode,
            #     'subjdesc': s.subjdesc,
            #     'unit': s.subjcredit
            #     # 'prereq': preq[0]
            # }
        # else:
        entry1 = {
            'subjcode': s.subjcode,
            'subjdesc': s.subjdesc,
            'unit': s.subjcredit
            # 'prereq': "None"
        }

        subjectsinformations.append(entry1)


    prog = 'BSCS'

    for s in subjectsinformations:
        q = db.session.query(CurriculumDetails.subjcode, Curriculum.progcode, CurriculumDetails.curriculum_year, CurriculumDetails.curriculum_sem).filter(Curriculum.curriculum_id==CurriculumDetails.curriculum_id).filter(CurriculumDetails.subjcode==s['subjcode']).filter(Curriculum.progcode==semstudent.studmajor).first()

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

    test = []
    for sub in subjectsindegree:
        test.append(sub['subjcode'])
    
    
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
                        if item[0] in test:
                            subjectPerDegree.append(item)
            if len(subjectPerDegree)>0:
                queriedSubjects.append(subjectPerDegree)
                subjectWeight = subjectWeight + 1
            position=position+1

            # print str(s['subjcode']) + "     " + str(subjectWeight) + "    " + str(subjectPerDegree)
        s.update({'weight': subjectWeight})


    specific_courses_for_the_sem = []



    for subject in subjectsindegree:
        semsy = db.session.query(CurriculumDetails.curriculum_year,CurriculumDetails.curriculum_sem).filter(CurriculumDetails.subjcode == subject['subjcode']).filter(CurriculumDetails.curriculum_id == Curriculum.curriculum_id).filter(Curriculum.progcode == semstudent.studmajor).first()

        if semsy.curriculum_year == studlevel and semsy.curriculum_sem == current_sem.sem:
            specific_courses_for_the_sem.append(subject)

    
    for sp in specific_courses_for_the_sem:

        print  str(sp['weight'])+ str(sp['subjcode'])+ str(sp['unit'])

    unit = 0
    # for s in specific_courses_for_the_sem:

    # #note: mugana sya pero need further consideration


    # for s in specific_courses_for_the_sem:
    #     for pre in prereqs:
    #         for passed in passedsubjs:
    #             if s[0]==pre[0] and pre[1] == passed[3]:
    #                 if lateststudent_record.scholasticstatus == 'Warning':
    #                     unit += s.subjcredit
    #                     if unit > 17:
    #                         unit = unit-s.subjcredit
    #                     else:
    #                         print str(s.subjcode)
    #                         print unit
    #                 if lateststudent_record.scholasticstatus == 'Probation':
    #                     unit += s.subjcredit
    #                     if unit > 12:
    #                         unit = unit-s.subjcredit
    #                     else:
    #                         print str(s.subjcode)
    #                         print unit
    #                 else:
    #                     unit +=s.subjcredit
    #                     print str(s.subjcode)
    #                     print unit

        
    #         if s[0]==pre[0] and pre[1] == 'None':
    #             unit += s.subjcredit
    #             if lateststudent_record.scholasticstatus == 'Warning':
    #                 if unit>17:
    #                     unit = unit - s.subjcredit
    #                 else:
    #                     print str(s.subjcode)
    #                     print unit
    #             if lateststudent_record.scholasticstatus == 'Probation':
    #                 if unit>12:
    #                     unit = unit - s.subjcredit
    #                 else:
    #                     print str(s.subjcode)
    #                     print unit
    #             else:
    #                     unit +=s.subjcredit
    #                     print str(s.subjcode)
    #                     print unit
    # #Note: No priority


    return render_template('home.html', title='Home', student=student, semstudent=semstudent, student_program=student_program,semstudent2=semstudent2, studlevel=studlevel)


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(emailadd=form.email.data).first()

        # if student and bcrypt.check_password_hash(student.password, form.password.data):
        if (student) and (student.password == form.password.data):
            login_user(student, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful! Please check username and password', 'danger')

    return render_template('login.html', title='Log In', form=form)


@app.route('/student_information', methods=['GET', 'POST'])
@login_required
def student_info():
    student = Student.query.filter_by(studid=current_user.studid).first()
    semstudent = SemesterStudent.query.filter_by(studid=student.studid).first()
    semstudent2 = SemesterStudent.query.filter_by(studid=student.studid).all()
    current_gpa = semstudent2[-1].gpa
    student_program = Program.query.filter_by(progcode=semstudent.studmajor).first()
    gpas = db.session.query(SemesterStudent.studid, SemesterStudent.gpa, SemesterStudent.sy, SemesterStudent.sem).filter_by(studid=current_user.studid).all()
    residency = db.session.query(SemesterStudent.sy).filter_by(studid=current_user.studid).distinct().count()
    studlevel = semstudent2[-1].studlevel

    cgpa = 0.0
    count = 0
    for gpa in gpas:
        cgpa = cgpa + float(gpa.gpa)
        count = count + 1
    
    cgpa = cgpa/float(count)

    return render_template('stud_info.html', title='Student Information', student=student, semstudent=semstudent, student_program=student_program, cgpa=cgpa, current_gpa=current_gpa, residency=residency, studlevel=studlevel)


@app.route('/academic_performance', methods=['POST', 'GET'])
@login_required
def academicperformance():
    student = Student.query.filter_by(studid=current_user.studid).first()
    semstudent = SemesterStudent.query.filter_by(studid=student.studid).first()
    semstudent2 = db.session.query(SemesterStudent.studid, SemesterStudent.sy, SemesterStudent.studlevel, SemesterStudent.sem).filter_by(studid=current_user.studid).all()
    residency = db.session.query(SemesterStudent.sy).filter_by(studid=current_user.studid).distinct().count()
    studlevel = semstudent2[-1].studlevel
    student_program = Program.query.filter_by(progcode=semstudent.studmajor).first()

    subjecthistories = db.session.query(Registration.studid, Registration.sem, Registration.sy, Registration.subjcode, Registration.grade, Registration.section, Subject.subjdesc).filter(Registration.studid==current_user.studid).filter(Registration.subjcode==Subject.subjcode).all()

    # schoolyear = db.session.query(Registration.sy).filter_by(studid=current_user.studid).group_by(Registration.sy).all()
    schoolyear = db.session.query(SemesterStudent.sy).filter_by(studid=current_user.studid).distinct().all()
    # sems = db.session.query(Registration.sem).filter_by(studid=current_user.studid).group_by(Registration.sem).all()
    sems = db.session.query(SemesterStudent.sem).filter_by(studid=current_user.studid).group_by(SemesterStudent.sem).all()

    print "School year: " + str(schoolyear)

    print "Sems: " + str(sems)

    gpas = db.session.query(SemesterStudent.studid, SemesterStudent.gpa, SemesterStudent.sy, SemesterStudent.sem).filter_by(studid=current_user.studid).all()
    
    print "GPAs: " + str(gpas)

    cgpa = 0.0
    # print "TYPE: " + str(type(cgpa))
    count = 0
    for gpa in gpas:
        if gpa.gpa is not None:
            cgpa = cgpa + float(gpa.gpa)
            count = count + 1
    
    cgpa = cgpa/float(count)

    return render_template('academicperformance.html', title='Academic Performance', optionaldesc="List of academic history of the student", student=student, semstudent=semstudent, student_program=student_program, subjecthistories=subjecthistories, sems=sems, schoolyear=schoolyear, gpas=gpas, cgpa=cgpa, studlevel=studlevel)


@app.route('/adviseme', methods=['GET','POST'])
@login_required
def adviseme():
    student = Student.query.filter_by(studid=current_user.studid).first()
    semstudent = SemesterStudent.query.filter_by(studid=student.studid).first()
    student_program = Program.query.filter_by(progcode=semstudent.studmajor).first()

    return render_template('adviseme.html', title='AdviseMe', optionaldesc="Find a degree for shifters", student=student, semstudent=semstudent, student_program=student_program)


@app.route('/addstudent', methods=['GET', 'POST'])
def addstudent():
    form = StudentForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        firstname = form.firstName.data
        lastname = form.lastName.data

        username = firstname.lower().replace(" ", "")+'.'+lastname.lower().replace(" ", "")

        student = Students(idNum=form.idNumber.data, firstName=form.firstName.data, middleName=form.middleName.data, lastName=form.lastName.data, gender=form.gender.data, userName=username, emailAddress=form.emailAddress.data, degree_id=form.degree.data, password=hashed_password)

        db.session.add(student)
        db.session.commit()

        flash('Account Created Successfully!', 'success')

        return redirect(url_for('login'))

    return render_template('addstudent.html', title='Admin: Add student', form=form)


@app.route('/addinstitutionrecord', methods=['GET', 'POST'])
def addinstitutionrecord():
    form = InstitutionInformationForm()

    if form.validate_on_submit():
        collegerecord = Colleges(collegeCode=form.collegeCode.data, collegeName=form.collegeName.data)

        db.session.add(collegerecord)
        db.session.commit()

        departmentrecord = Departments(deptCode=form.departmentCode.data, deptName=form.departmentName.data, college_id=collegerecord.id)

        db.session.add(departmentrecord)
        db.session.commit()

        degreerecord = Degrees(degreeCode=form.degreeCode.data, degreeName=form.degreeName.data, department_id=departmentrecord.id)

        db.session.add(degreerecord)
        db.session.commit()

        return redirect(url_for(home))

    return render_template('addinstitutionrecord.html', title='Admin: Add Institution Record', form=form)


# @app.route('/addcoursesrecord', methods=['GET', 'POST'])
# def addcoursesrecord():
#     form = VarArraySolutionPrinter()

#     return render_template('addcoursesrecord.html', title='Admin: Add Courses Record', form=form)





# @app.route('/sample', methods=['GET','POST'])
# def sample():
    
#     cpsat = SearchForAllSolutionsSampleSat()

#     return cpsat


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))