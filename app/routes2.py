from app import app2, db, bcrypt2
from flask import render_template, url_for, flash, redirect, request, jsonify
from app.models2 import *
# from app.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from app import engine as main_engine
from flask_cors import CORS, cross_origin

CORS(app2)

@app2.route('/')
@app2.route('/home')
# @login_required
def home():
    return render_template('home.html', title="Home")


@app2.route('/student_information', methods=['GET', 'POST'])
# @login_required
def student_info():
    return render_template('stud_info.html', title='Student Information')
    # return "Student Information!"


@app2.route('/academic_performance', methods=['POST', 'GET'])
# @login_required
def academicperformance():
    return render_template('academicperformance.html', title='Academic Performance')
    # return "Academic Performance"


@app2.route('/adviseme', methods=['GET','POST'])
# @login_required
def adviseme():
    return render_template('adviseme.html', title='AdviseMe')
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