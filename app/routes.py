from app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, jsonify, make_response
from app.models import *
from app.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from app import engine as main_engine
from flask_cors import CORS, cross_origin

CORS(app)


@app.route('/')
@app.route('/home')
@cross_origin()
def home():
    student = Student.query.filter_by(studid=current_user.studid).first()
    semstudent = SemesterStudent.query.filter_by(studid=current_user.studid).all()
    latestsemstud = semstudent[-1]
    residency = db.session.query(SemesterStudent.sy).filter_by(studid=current_user.studid).distinct().count()
    studlevel = latestsemstud.studlevel
    student_program = Program.query.filter_by(progcode=latestsemstud.studmajor).first()
    subjecthistories = db.session.query(Registration.studid, Registration.sem, Registration.sy, Registration.subjcode, Registration.grade, Registration.section, Subject.subjdesc).filter(Registration.studid==student.studid).filter(Registration.subjcode==Subject.subjcode).all()

    res = []
    res.append({"studfirstname": str(student.studfirstname), "studlastname": str(student.studlastname), "studentlevel": studlevel, "studmajor": str(latestsemstud.studmajor)})
                     
    return jsonify({'status': 'ok', 'data': res, 'count': len(res)})


# @app.route('/login', methods=['GET', 'POST'])
# def login():
    
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
    
#     form = LoginForm()
#     if form.validate_on_submit():
#         student = Student.query.filter_by(emailadd=form.email.data).first()

#         # if student and bcrypt.check_password_hash(student.password, form.password.data):
#         if (student) and (student.password == form.password.data):
#             # print student.studid
#             res = []
#             login_user(student, remember=form.remember.data)
#             next_page = request.args.get('next')
#             res.append({"studid": student.studid})

#             return res, redirect(next_page) if next else redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful! Please check username and password', 'danger')

#     return render_template('login.html', title='Log In', form=form)

# @app.route('/login')
# def login():
#     auth = request.authorization

#     auth.username = 

#     if not auth or not auth.username or not auth.password:
#         return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

#     user = User.query.filter_by(name=auth.username).first()

#     if not user:
#         return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

#     if check_password_hash(user.password, auth.password):
#         token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

#         return jsonify({'token' : token.decode('UTF-8')})

#     return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})



@app.route('/studentinformation', methods=['POST', "GET"])
def student_info():
    student = Student.query.filter_by(studid='2018-0013').first()
    semstudent = SemesterStudent.query.filter_by(studid=student.studid).all()
    latestsemstud = semstudent[-1]
    residency = db.session.query(SemesterStudent.sy).filter_by(studid=student.studid).distinct().count()
    studlevel = latestsemstud.studlevel
    student_program = Program.query.filter_by(progcode=latestsemstud.studmajor).first()
    subjecthistories = db.session.query(Registration.studid, Registration.sem, Registration.sy, Registration.subjcode, Registration.grade, Registration.section, Subject.subjdesc).filter(Registration.studid==student.studid).filter(Registration.subjcode==Subject.subjcode).all()
    currentgpa = str(latestsemstud.gpa)
    student_program = Program.query.filter_by(progcode=latestsemstud.studmajor).first()
    gpas = db.session.query(SemesterStudent.studid, SemesterStudent.gpa, SemesterStudent.sy, SemesterStudent.sem).filter_by(studid=student.studid).all()


    cgpa = 0.0
    count = 0
    finalgpas = []
    for gpa in gpas:
        if gpa.gpa is not None:
            cgpa = cgpa + float(gpa.gpa)
            finalgpas.append({"gpa": str(gpa.gpa),"sy": gpa.sy, "sem": gpa.sem})
            count = count + 1
            
    cgpa = cgpa/float(count)

    res = []
    res.append({"studfirstname": str(student.studfirstname), "studlastname": str(student.studlastname), "studentlevel": studlevel, "studmajor": str(latestsemstud.studmajor), "progdesc": student_program.progdesc, "scholasticstatus": str(latestsemstud.scholasticstatus), "cgpa": cgpa, "currentgpa": currentgpa})
                     
    return jsonify({'status': 'ok', 'data': res, 'count': len(res)})


@app.route('/academicperformance', methods=['POST', 'GET'])
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
            
    cgpa = cgpa/float(count)

    res = []
    res.append({"cgpa": str(cgpa), "syandsem": syandsem, "studmajor": studmajorparsed, "studentprogram": str(student_program.progdesc), "subjecthistories": subjecthistories,"gpas": finalgpas, "studentlevel": studlevel})
                     
    return jsonify({'status': 'ok', 'data': res, 'count': len(res)})


@app.route('/adviseme', methods=['GET','POST'])
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
        
    return render_template('adviseme.html', title='AdviseMe', optionaldesc="Find a degree for shifters", student=student, semstudent=semstudent, student_program=student_program, studlevel=studlevel, degrees=degrees)


@app.route('/enginetest', methods=['GET','POST'])
@login_required
def enginetest():
    display = main_engine.main()

    return display


@app.route('/sampleapi', methods=['GET'])
# @login_required
@cross_origin
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