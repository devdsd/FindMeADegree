from app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, jsonify
from app.models import *
from app.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from app import engine as main_engine
from flask_cors import CORS, cross_origin

CORS(app)

@app.route('/')
@app.route('/home')
# @login_required
def home():
    student = Student.query.filter_by(studid='2018-0013').first()
    semstudent = SemesterStudent.query.filter_by(studid='2018-0013').all()
    latestsemstud = semstudent[-1]
    residency = db.session.query(SemesterStudent.sy).filter_by(studid='2018-0013').distinct().count()
    studlevel = latestsemstud.studlevel
    student_program = Program.query.filter_by(progcode=latestsemstud.studmajor).first()
    subjecthistories = db.session.query(Registration.studid, Registration.sem, Registration.sy, Registration.subjcode, Registration.grade, Registration.section, Subject.subjdesc).filter(Registration.studid==student.studid).filter(Registration.subjcode==Subject.subjcode).all()

    res = []
    # res.append({"studid": str(student.studid), "studfirstname": str(student.studfirstname), "studlastname": str(student.studlastname), "email": str(student.emailadd), "studmajor": str(student_program)})
    res.append({"studfirstname": str(student.studfirstname), "studlastname": str(student.studlastname), "studentlevel": studlevel, "studmajor": str(latestsemstud.studmajor)})
                     
    return jsonify({'status': 'ok', 'data': res, 'count': len(res)})

    
    # return render_template('home.html', title='Home', student=student, semstudent=semstudent, student_program=student_program,semstudent2=semstudent2, studlevel=studlevel)


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
    student = Student.query.filter_by(studid='2018-0013').first()
    semstudent = SemesterStudent.query.filter_by(studid='2018-0013').all()
    latestsemstud = semstudent[-1]
    residency = db.session.query(SemesterStudent.sy).filter_by(studid=student.studid).distinct().count()
    student_program = Program.query.filter_by(progcode=latestsemstud.studmajor).first()
    studmajor = str(student_program.progcode)
    studmajorparsed = studmajor.rstrip()
    studlevel = latestsemstud.studlevel

    subjecthistories = db.session.query(Registration.studid, Registration.sem, Registration.sy, Registration.subjcode, Registration.grade, Registration.section, Subject.subjdesc).filter(Registration.studid==student.studid).filter(Registration.subjcode==Subject.subjcode).all()
    
    syandsem = db.session.query(SemesterStudent.sy, SemesterStudent.sem).filter_by(studid=student.studid).all()

    gpas = db.session.query(SemesterStudent.studid, SemesterStudent.gpa, SemesterStudent.sy, SemesterStudent.sem).filter_by(studid=student.studid).all()

    cgpa = 0.0
    count = 0
    finalgpas = []
    for gpa in gpas:
        if gpa.gpa is not None:
            cgpa = cgpa + float(gpa.gpa)
            finalgpas.append({"gpa": str(gpa.gpa),"sy": gpa.sy, "sem": gpa.sem})
            count = count + 1
    
    print (finalgpas)

    gpalen = len(finalgpas)

    print (gpalen)
    
    syandsemlen = len(syandsem)
    subjecthistorieslen = len(subjecthistories)

    
    cgpa = cgpa/float(count)

    res = []
    res.append({"cgpa": str(cgpa), "syandsem": syandsem, "syandsemlen": syandsemlen, "studmajor": studmajorparsed, "studentprogram": str(student_program.progdesc), "subjecthistories": subjecthistories, "subjecthistorieslen": subjecthistorieslen,"gpas": finalgpas, "gpalen": gpalen, "studentlevel": studlevel})
                     
    return jsonify({'status': 'ok', 'data': res, 'count': len(res)})

    # return render_template('academicperformance.html', title='Academic Performance', optionaldesc="List of academic history of the student", student=student, semstudent=semstudent, student_program=student_program, subjecthistories=subjecthistories, gpas=gpas, cgpa=cgpa, studlevel=studlevel, syandsem=syandsem)


@app.route('/adviseme', methods=['GET','POST'])
@login_required
def adviseme():
    student = Student.query.filter_by(studid=current_user.studid).first()
    semstudent = SemesterStudent.query.filter_by(studid=student.studid).first()
    student_program = Program.query.filter_by(progcode=semstudent.studmajor).first()
    semstudent2 = db.session.query(SemesterStudent.studid, SemesterStudent.sy, SemesterStudent.studlevel, SemesterStudent.sem, SemesterStudent.scholasticstatus).filter_by(studid=current_user.studid).all()
    studlevel = semstudent2[-1].studlevel
    progs = db.session.query(Program.progcode).all()
    degrees = []

    for prog in progs:
        degrees.append(prog[0])

    # print degrees
    # print progs
    return render_template('adviseme.html', title='AdviseMe', optionaldesc="Find a degree for shifters", student=student, semstudent=semstudent, student_program=student_program, studlevel=studlevel, degrees=degrees)


@app.route('/enginetest', methods=['GET','POST'])
@login_required
def enginetest():
    display = main_engine.main()

    return display


# @app.route('/sample')
# @login_required
# def sample():
#     student = Student.query.filter_by(studid=current_user.studid).first()
#     semstudent = SemesterStudent.query.filter_by(studid=student.studid).first()
#     semstudent2 = db.session.query(SemesterStudent.studid, SemesterStudent.sy, SemesterStudent.studlevel, SemesterStudent.sem, SemesterStudent.scholasticstatus).filter_by(studid=current_user.studid).all()
#     residency = db.session.query(SemesterStudent.sy).filter_by(studid=current_user.studid).distinct().count()
#     studlevel = semstudent2[-1].studlevel
#     student_program = Program.query.filter_by(progcode=semstudent.studmajor).first()

#     return render_template('sampleapi.html', title='Sample', student=student, semstudent=semstudent, student_program=student_program,semstudent2=semstudent2, studlevel=studlevel)


@app.route('/sampleapi', methods=['GET'])
# @login_required
@cross_origin()
def sampleapi():
    semstudent = db.session.query(SemesterStudent).filter_by(studid='2018-0013').first()

    res = []
    res.append({"studid": semstudent.studid, "sem": semstudent.sem, "sy": semstudent.sy, "studlevel": semstudent.studlevel,
                     "scholasticstatus": semstudent.scholasticstatus, "scholarstatus": semstudent.scholarstatus, "studmajor": semstudent.studmajor, "gpa": str(semstudent.gpa),
                     "cgpa": str(semstudent.cgpa)})
                     
    return jsonify({'status': 'ok', 'entries': res, 'count': len(res)})


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# @app.route('/addstudent', methods=['GET', 'POST'])
# def addstudent():
#     form = StudentForm()

#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
#         firstname = form.firstName.data
#         lastname = form.lastName.data

#         username = firstname.lower().replace(" ", "")+'.'+lastname.lower().replace(" ", "")

#         student = Students(idNum=form.idNumber.data, firstName=form.firstName.data, middleName=form.middleName.data, lastName=form.lastName.data, gender=form.gender.data, userName=username, emailAddress=form.emailAddress.data, degree_id=form.degree.data, password=hashed_password)

#         db.session.add(student)
#         db.session.commit()

#         flash('Account Created Successfully!', 'success')

#         return redirect(url_for('login'))

#     return render_template('addstudent.html', title='Admin: Add student', form=form)


# @app.route('/addinstitutionrecord', methods=['GET', 'POST'])
# def addinstitutionrecord():
#     form = InstitutionInformationForm()

#     if form.validate_on_submit():
#         collegerecord = Colleges(collegeCode=form.collegeCode.data, collegeName=form.collegeName.data)

#         db.session.add(collegerecord)
#         db.session.commit()

#         departmentrecord = Departments(deptCode=form.departmentCode.data, deptName=form.departmentName.data, college_id=collegerecord.id)

#         db.session.add(departmentrecord)
#         db.session.commit()

#         degreerecord = Degrees(degreeCode=form.degreeCode.data, degreeName=form.degreeName.data, department_id=departmentrecord.id)

#         db.session.add(degreerecord)
#         db.session.commit()

#         return redirect(url_for(home))

#     return render_template('addinstitutionrecord.html', title='Admin: Add Institution Record', form=form)


# @app.route('/addcoursesrecord', methods=['GET', 'POST'])
# def addcoursesrecord():
#     form = VarArraySolutionPrinter()

#     return render_template('addcoursesrecord.html', title='Admin: Add Courses Record', form=form)


# @app.route('/sample', methods=['GET','POST'])
# def sample():
    
#     cpsat = SearchForAllSolutionsSampleSat()

#     return cpsat