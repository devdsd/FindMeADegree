from app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from app.forms import *
from app.models import *


@app.route('/')
@app.route('/home')
# @login_required()
def home():
	return render_template('starter.html', title='Home')


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        firstname = form.firstName.data
        lastname = form.lastName.data

        username = firstname.lower().replace(" ", "")+'.'+lastname.lower().replace(" ", "")

        student = Students(idNum=form.idNumber.data, firstName=form.firstName.data, middleName=form.middleName.data, lastName=form.lastName.data, gender=form.gender.data, userName=username, emailAddress=form.emailAddress.data,password=hashed_password)

        db.session.add(student)
        db.session.commit()

        flash('Account Created Successfully!', 'success')

        return redirect(url_for('login'))

    return render_template('signup.html', title='Signup', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    # if form.validate_on_submit():
    #     flash('Login Successfully!', 'success')
    #     student = Students.query.filter_by(userName=form.username.data).first()
          
    #     if student and bcrypt.check_password_hash(student.password, form.password.data):
    #         # login_user(student, remember=form.remember.data)
    #         # next_page = request.args.get('next')
    #         # return redirect(next_page) if next_page else redirect(url_for('home'))
    #         flash('Login Successfully!', 'success')
    #         return redirect(url_for('home'))
    #     else:
    #         flash('Login Unsuccessful! Please check username/email and password', 'danger')
    return render_template('login.html', title='Log In', form=form)

@app.route('/student_information')
def student_info():
    return render_template('starter.html', title='Student Information')

@app.route('/academic_performance')
def academics():
    return render_template('starter.html', title='Academic Performance')

@app.route('/adviseme')
def adviseme():
    return render_template('starter.html', title='AdviseMe')

@app.route('/logout')
def logout():
    return render_template('logout.html', title='Logout')