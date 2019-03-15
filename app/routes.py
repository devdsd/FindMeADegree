from app import app
from flask import render_template, url_for, flash, redirect, request
from app.forms import *

@app.route('/')
@app.route('/home')
def home():
	return render_template('starter.html', title='Home')
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    return render_template('signup.html', title='Signup', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    
    form = LoginForm()
    # if form.validate_on_submit():
	# 	flash('Login Successfully!', 'success')
    #     user = Users.query.filter_by(email=form.email.data).first()
    #     # user_email = Users.query.filter_by(email=form.email.data).first()
    #     if user and bcrypt.check_password_hash(user.password, form.password.data):
    #         login_user(user, remember=form.remember.data)
    #         next_page = request.args.get('next')
    #         return redirect(next_page) if next_page else redirect(url_for('account'))
    #         # return redirect(url_for('home'))
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