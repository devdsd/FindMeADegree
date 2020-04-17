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

        # if student and bcrypt.check_password_hash(student.password, form.password.data):
        if (student) and (student.password == form.password.data):
            login_user(student, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful! Please check username and password', 'danger')

    return render_template('login.html', title='Log In', form=form)


@app2.route('/')
@app2.route('/home')
@login_required
def home():
    return render_template('home.html', title="Home")


@app2.route('/student_information', methods=['GET', 'POST'])
@login_required
def student_info():
    return render_template('stud_info.html', title='Student Information')
    # return "Student Information!"


@app2.route('/academic_performance', methods=['POST', 'GET'])
@login_required
def academicperformance():
    return render_template('academicperformance.html', title='Academic Performance', optionaldesc="List of academic history of the student")
    # return "Academic Performance"


@app2.route('/adviseme', methods=['GET','POST'])
@login_required
def adviseme():
    return render_template('adviseme.html', title='AdviseMe', optionaldesc="Find a degree for shifters")
    # return "Advise Me"


@app2.route('/sample', methods=['GET', 'POST'])
# @login_required
def sample():
    
    return render_template('sampleapi.html')
    # return render_template('starter.html', title="Home")


@app2.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app2.route('/enginetest', methods = ['GET','POST'])
def enginetest():
    display = main_engine.main()

    return display