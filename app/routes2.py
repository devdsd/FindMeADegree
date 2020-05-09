from app import app2, db, bcrypt2
from flask import render_template, url_for, flash, redirect, request, jsonify
from app.models2 import *
from app.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from app import engine as main_engine
from flask_cors import CORS, cross_origin

CORS(app2)


@app2.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(emailadd=form.email.data).first()

        if (student) and (student.password == form.password.data):
            login_user(student, remember=form.remember.data)
            studid = str(current_user.studid)
            next_page = request.args.get('next')

            if next_page is not None:
                if next_page == "/":
                    return redirect(url_for('home'))
                else:
                    next_pageparsed = str(next_page.strip('/'))
                    return redirect(url_for(next_pageparsed))
            else:
                return redirect(url_for('home'))

        else:
            flash('Login Unsuccessful! Please check username and password', 'danger')

    return render_template('login.html', title='Log In', form=form)


@app2.route("/")
@app2.route('/home')
@login_required
def home():
    return render_template('home.html', title="Home", studid=current_user.studid)


@app2.route('/student_information', methods=['GET', 'POST'])
@login_required
def student_information():
    return render_template('stud_info.html', title='Student Information', studid=current_user.studid)
    # return "Student Information!"


@app2.route('/academic_performance', methods=['POST', 'GET'])
@login_required
def academic_performance():
    return render_template('academicperformance.html', title='Academic Performance', optionaldesc="List of academic history of the student", studid=current_user.studid)
    # return "Academic Performance"


@app2.route('/adviseme', methods=['GET','POST'])
@login_required
def adviseme():
    progs = db.session.query(Program.progcode).all()
    degrees = []

    for prog in progs:
        degrees.append(prog[0])

    return render_template('adviseme.html', title='AdviseMe', optionaldesc="Find a degree for shifters", studid=current_user.studid, degrees=degrees)
    # return "Advise Me"


@app2.route('/recommendation', methods=['POST', 'GET'])
@login_required
def recommendation():

    return render_template('recommended.html', title="Recommended Degrees", studid=current_user.studid)


@app2.route('/enginetest', methods=['GET','POST'])
@cross_origin()
@login_required
def enginetest():
    # data = request.args.get('studid')
    student = Student.query.filter_by(studid=current_user.studid).first()
    # login_user(student)
    semstudent = SemesterStudent.query.filter_by(studid=student.studid).all()
    latestsemstud = semstudent[-1]
    residency = db.session.query(SemesterStudent.sy).filter_by(studid=student.studid).distinct().count()
    studlevel = latestsemstud.studlevel
    student_program = Program.query.filter_by(progcode=latestsemstud.studmajor).first()
    programs = []
    syandsem = []
    
    res = main_engine.main()

    print res[0]['residency']
    
    # for cs in bscs:
    #     syandsem.append({'year' : int(cs['yeartotake']), 'sem' : int(cs['semtotake'])})

    # # print(syandsem)
    # # syandsem = list(set(syandsem))
    # syandsem = [i for n, i in enumerate(syandsem) if i not in syandsem[:n]]
    
    # syandsem.sort(key = lambda i:(i['year'], i['sem']), reverse = False)

    # print(bscs)

    # print(syandsem)


    return "Done"


@app2.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))