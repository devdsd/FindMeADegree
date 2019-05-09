from app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from app.models import *
from app.forms import *
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
@login_required
def home():
	return render_template('starter.html', title='Home')


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


@app.route('/addcoursesrecord', methods=['GET', 'POST'])
def addcoursesrecord():
    form = CoursesInformationForm()

    return render_template('addcoursesrecord.html', title='Admin: Add Courses Record', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        stud = Student.query.filter_by(emailadd=form.email.data).first()

        # if student and bcrypt.check_password_hash(student.password, form.password.data):
        if (stud) and (stud.password == form.password.data):
            login_user(stud, remember=form.remember.data)
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
    program = Program.query.filter_by(progcode=semstudent.studmajor).first()
    program_desc = (program.progdesc).upper()

    return render_template('stud_info.html', title='Student Information', student=student, semstudent=semstudent, program_desc=program_desc)

@app.route('/academic_performance')
@login_required
def academics():
    return render_template('acad_per.html', title='Academic Performance')

@app.route('/adviseme')
@login_required
def adviseme():
    return render_template('ad_me.html', title='AdviseMe')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))