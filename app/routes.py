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
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    return render_template('signup.html', title='Signup', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        student = Students.query.filter_by(userName=form.username.data).first()

        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful! Please check username and password', 'danger')

    return render_template('login.html', title='Log In', form=form)

@app.route('/student_information')
@login_required
def student_info():
    return render_template('starter.html', title='Student Information')

@app.route('/academic_performance')
@login_required
def academics():
    return render_template('starter.html', title='Academic Performance')

@app.route('/adviseme')
@login_required
def adviseme():
    return render_template('starter.html', title='AdviseMe')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))