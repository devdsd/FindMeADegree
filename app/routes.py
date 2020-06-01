from app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, jsonify, make_response
from app.models import *
from app.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from app import engine as main_engine
from flask_cors import CORS, cross_origin
import time

CORS(app)



@app.route('/')
@app.route('/home')
def home():
    start_time = time.time()
    data = request.args.get('studid')
    student = Student.query.filter_by(studid=data).first()

    login_user(student)

    semstudent = SemesterStudent.query.filter_by(studid=student.studid).all()
    latestsemstud = semstudent[-1]
    residency = db.session.query(SemesterStudent.sy).filter_by(studid=student.studid).distinct().count()
    studlevel = latestsemstud.studlevel
    student_program = Program.query.filter_by(progcode=latestsemstud.studmajor).first()
    
    res = []
    res.append({"studid": student.studid, "studfirstname": str(student.studfirstname), "studlastname": str(student.studlastname), "studentlevel": studlevel, "studmajor": str(latestsemstud.studmajor)})

    print('\n------ runtime: %s seconds ------' % round(time.time() - start_time, 5))                
    return jsonify({'status': 'ok', 'data': res, 'count': len(res)})



@app.route('/student_information', methods=['POST', "GET"])
def student_information():
    start_time = time.time()
    data = request.args.get('studid')
    student = Student.query.filter_by(studid=data).first()
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
    res.append({"studid": student.studid, "studfirstname": str(student.studfirstname), "studlastname": str(student.studlastname), "studentlevel": studlevel, "studmajor": str(latestsemstud.studmajor), "progdesc": student_program.progdesc, "scholasticstatus": str(latestsemstud.scholasticstatus), "cgpa": cgpa, "currentgpa": currentgpa})

    print('\n------ runtime: %s seconds ------' % round(time.time() - start_time, 5))     
    return jsonify({'status': 'ok', 'data': res, 'count': len(res)})



@app.route('/academic_performance', methods=['POST', 'GET'])
def academic_performance():
    start_time = time.time()
    data = request.args.get('studid')
    student = Student.query.filter_by(studid=data).first()
    semstudent = SemesterStudent.query.filter_by(studid=student.studid).all()
    latestsemstud = semstudent[-1]
    residency = db.session.query(SemesterStudent.sy).filter_by(studid=student.studid).distinct().count()
    student_program = Program.query.filter_by(progcode=latestsemstud.studmajor).first()
    studmajor = str(student_program.progcode)
    studmajorparsed = studmajor.rstrip()
    studlevel = latestsemstud.studlevel

    subjecthistories = db.session.query(Registration.studid, Registration.sem, Registration.sy, Registration.subjcode, Registration.grade, Registration.section, Subject.subjdesc).filter(Registration.studid==student.studid).filter(Registration.subjcode==Subject.subjcode).all()
    
    syandsem = db.session.query(SemesterStudent.sy, SemesterStudent.sem).filter_by(studid=student.studid).all()

    print(syandsem)

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

    print('\n------ runtime: %s seconds ------' % round(time.time() - start_time, 5))                 
    return jsonify({'status': 'ok', 'data': res, 'count': len(res)})



@app.route('/adviseme', methods=['GET','POST'])
def adviseme():
    start_time = time.time()
    data = request.args.get('studid')

    student = Student.query.filter_by(studid=data).first()

    login_user(student)

    semstudent = SemesterStudent.query.filter_by(studid=student.studid).all()
    latestsemstud = semstudent[-1]
    residency = db.session.query(SemesterStudent.sy).filter_by(studid=student.studid).distinct().count()
    studlevel = latestsemstud.studlevel
    student_program = Program.query.filter_by(progcode=latestsemstud.studmajor).first()
    

    res = []
    res.append({"studid": student.studid, "studfirstname": str(student.studfirstname), "studlastname": str(student.studlastname), "studentlevel": studlevel, "studmajor": str(latestsemstud.studmajor)})

    print('\n------ runtime: %s seconds ------' % round(time.time() - start_time, 5))                
    return jsonify({'status': 'ok', 'data': res, 'count': len(res)})



@app.route('/engine', methods=['GET','POST'])
@cross_origin()
def engine():
    start_time = time.time()
    data = request.args.get('studid')
    student = Student.query.filter_by(studid=data).first()
    login_user(student)
    semstudent = SemesterStudent.query.filter_by(studid=student.studid).all()
    latestsemstud = semstudent[-1]
    residency = db.session.query(SemesterStudent.sy).filter_by(studid=student.studid).distinct().count()
    studlevel = latestsemstud.studlevel
    student_program = Program.query.filter_by(progcode=latestsemstud.studmajor).first()
    programs = []

    data = main_engine.main()

    counter = 1
    for d in data:
        q = db.session.query(Program.progcode).filter(Program.progcode==d['DegreeName']).first()
        programs.append({'rank': counter, 'degreename': q})
        counter += 1
    
    data.append({"studid": student.studid, "studfirstname": str(student.studfirstname), "studlastname": str(student.studlastname), "studentlevel": studlevel, "studmajor": str(latestsemstud.studmajor), "studentprogram": str(student_program), "programs": programs})

    print('\n------ runtime: %s seconds ------' % round(time.time() - start_time, 5)) 
    return jsonify({'status': 'ok', 'data': data, 'count': len(data)})

    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))