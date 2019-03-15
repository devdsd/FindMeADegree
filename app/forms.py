from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, TextField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms.fields.html5 import DateField
from wtforms_components import TimeField
from wtforms.validators import InputRequired

class SignupForm(FlaskForm):
  idNumber = StringField('ID Number', validators=[DataRequired(), Length(min=4,max=9)])
  firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
  middleName = StringField('Middle Name', validators=[DataRequired(), Length(min=2, max=50)])
  lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
  gender = SelectField('Gender', coerce=str, choices=[('Male', 'Male'), ('Female', 'Female')])
  emailAddress = StringField('Email', validators=[DataRequired(), Email()])
  # username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

  submit = SubmitField('Sign Up')

  # def validate_username(self, username):
  #   user = Students.query.filter_by(username=username.data).first()
  # if user:
  #   raise ValidationError('That username already exists. Please choose different one!')

  # def validate_email(self, email):
  #   user = Students.query.filter_by(email=email.data).first()
  # if user:
  #   raise ValidationError('That email is already exists. Please choose different one!')

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')

    # email = StringField('Email', validators=[DataRequired(), Email()])
  submit = SubmitField('Login')