from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, TextField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms.fields.html5 import DateField
from wtforms_components import TimeField
from wtforms.validators import InputRequired
# from app.models import *

class StudentForm(FlaskForm):
    idNumber = StringField('ID Number', validators=[DataRequired(), Length(min=4,max=9)])
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    middleName = StringField('Middle Name', validators=[DataRequired(), Length(min=2, max=50)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    gender = SelectField('Gender', coerce=str, choices=[('Male', 'Male'), ('Female', 'Female')])
    emailAddress = StringField('Email', validators=[DataRequired(), Email()])
    # degree = SelectField('Degree', coerce=int, choices=[(degree.id, degree.degreeCode) for degree in Degrees.query.all()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

  # def validate_username(self, username):
  #   student = Student.query.filter_by(userName=username.data).first()
  #   if student:
  #     raise ValidationError('That username already exists. Please choose different one!')

    def validate_email(self, emailAddress):
        student = Student.query.filter_by(emailadd=email.data).first()
        if student:
            raise ValidationError('That email is already exists. Please choose different one!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    # username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

        # email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Login')

class InstitutionInformationForm(FlaskForm):
    collegeCode = StringField('College Code', validators=[DataRequired(), Length(max=20)])
    collegeName = StringField('College Name', validators=[DataRequired(), Length(max=100)])
    departmentCode = StringField('Department Code', validators=[DataRequired(), Length(max=100)])
    departmentName = StringField('Department Name', validators=[DataRequired(), Length(max=300)])
    degreeCode = StringField('Degree Code', validators=[DataRequired(), Length(max=15)])
    degreeName = StringField('Department Name', validators=[DataRequired(), Length(max=100)])
    courseCode = StringField('Course Code', validators=[DataRequired(), Length(max=10)])
    courseTitle = StringField('Course Title', validators=[DataRequired(), Length(max=150)])
    department = StringField('Dapartment', validators=[DataRequired(), Length(max=300)])
    units = IntegerField('Units', validators=[DataRequired()])
    semester = StringField('Semester', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Submit')

class CoursesInformationForm(FlaskForm):
    courseCode = StringField('Course Code', validators=[DataRequired(), Length(max=10)])
    courseTitle = StringField('Course Title', validators=[DataRequired(), Length(max=150)])
    department = StringField('Dapartment', validators=[DataRequired(), Length(max=300)])
    units = IntegerField('Units', validators=[DataRequired()])
    preRequisite = IntegerField('Pre-requisite', validators=[DataRequired()])
    coRequisite = IntegerField('Co-Requisite', validators=[DataRequired()])
    semester = StringField('Semester', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Submit')


# class EngineForms():
#     selectDegrees = SelectField('Select Specific Degree', coerce=int, choices=[(category.catId, category.categoryName) for category in Categories.query.all()])