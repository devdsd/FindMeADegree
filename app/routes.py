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
    subjects = Subject.query.all()

    # subjecthistories = db.session.query(Registration.studid, Registration.sem, Registration.sy, Registration.subjcode, Registration.grade, Registration.section, Subject.subjdesc).filter(Registration.studid==current_user.studid).filter(Registration.subjcode==Subject.subjcode).all()

    current_sem = db.session.query(Semester.sy, Semester.sem).filter(Semester.is_online_enrollment_up==True).first()

    subjectsinformations = []
    passedsubjs = []
    failedsubjs = []
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
            else:
                failedsubjs.append(subj)

    # for p in failedsubjs:
    #     q = Registration.query.filter(Registration.subjcode==p['subjcode']).filter(Registration.studid==current_user.studid).first()
    #     if q is not None:
    #         p['grade'] = q.grade


    # for subj in subjectsinformations:
    #     print subj

    prog = 'BSA'

    for s in subjectsinformations:
        q = db.session.query(Curriculum.progcode, CurriculumDetails.curriculum_year, CurriculumDetails.curriculum_sem).filter(Curriculum.curriculum_id==CurriculumDetails.curriculum_id).filter(CurriculumDetails.subjcode==s['subjcode']).filter(Curriculum.progcode==prog).first()

        if q is not None:
            subjectsindegree.append(s)


    for subj in subjectsindegree:
        print subj

    # for k in listAll:
    #     print k['code']
    # Minors, Majors  = [],[]
    # for i in subjects:
    #     preqs = Prerequisite.query.all()
    #     position = 0
    #     subjectWeight = 0
    #     queriedSubjects = []
    #     queriedSubjects.append([i])
    #     while position<len(queriedSubjects):
    #         subjectPerDegree = []
    #         for o in queriedSubjects[position]:
    #             temp = Prerequisite.query.filter_by(prereq=o).all()
    #             if temp:
    #                 for item in temp:
    #                     subjectPerDegree.append(item.subjcode)
    #                 # map(lambda item: subjectPerDegree.append(database_char_parser(item.subjcode)), temp)
    #         if len(subjectPerDegree)>0:
    #             queriedSubjects.append(subjectPerDegree)
    #             subjectWeight = subjectWeight + 1
    #         position=position+1

    #         # print str(i) + "     " + str(subjectWeight) + "    " + str(subjectPerDegree)
    #     if subjectWeight == 0:
    #         Minors.append(i)
    #     else:
    #         Majors.append(i)
            # print subjectPerDegree
    
    # for m in Majors:
    #     print m

    # for i in subjects:
    #     current_subjectcode = []
    #     query1 = Prerequisite.query.filter_by(prereq=i).all()
    #     current_subjectcode.append(i)
    #     weight = 0
    #     if query1:
    #         for j in query1:
    #             if j in program:
    #                 current_subjectcode[:] = []
    #                 current_subjectcode.append(j)
    #         weight += 1
    #     else:
    #         weightSub = weight


    # subjectsindegree = db.session.query(CurriculumDetails.subjcode, Curriculum.progcode, CurriculumDetails.curriculum_year, CurriculumDetails.curriculum_sem, Subject.subjdesc, Subject.subjcredit).filter(CurriculumDetails.curriculum_id==Curriculum.curriculum_id).filter(Curriculum.progcode==prog).filter(CurriculumDetails.subjcode==Subject.subjcode).all()

    # for subj in subjectsindegree:
    #     q = db.session.query(Prerequisite.subjcode, Prerequisite.prereq).filter(Prerequisite.subjcode==subj.subjcode).first()
    #     if q != None:
    #         prereqs.append(q)
        
    
    # specific_courses_for_the_sem = []

    # for passed in passedsubjs:
    #     for s in subjectsindegree:
    #         if (s.subjcode == passed.subjcode):
    #             returnsubjs.append(s)

    # for subject in subjectsindegree:
    #     if subject.curriculum_year == residency and subject.curriculum_sem == current_sem.sem:
    #         specific_courses_for_the_sem.append(subject)

    # unit = 0
    # #note: mugana sya pero need further consideration

    # arr1, arr2, arr4 = [], [], []
    # for entry in prereqs:
    #     arr1.append(entry.subjcode)

    # for entry2 in subjectsindegree:
    #     arr2.append(entry2.subjcode)
   
    # arr3 = set(arr2) - set(arr1)

    # for i in arr3:
    #     prereqs.append(tuple((i,"None")))

    
    # print "Result: "
    # print "=============="
    # for arr in prereqs:
    #     print arr


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