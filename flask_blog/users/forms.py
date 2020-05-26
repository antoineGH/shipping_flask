from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user
from flask_blog.models import User
from flask_blog.users.utils import get_country

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is not account with that email, you must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Password"})
    submit = SubmitField('Reset Password')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Last Name"})
    email = StringField('Email address', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    email = StringField('Email address', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    phone = StringField('Phone', validators=[DataRequired(), Length(min=2, max=15)], render_kw={"placeholder": "Phone"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Enter password"})
    address = StringField('Address', validators=[DataRequired(), Length(min=3, max=50)], render_kw={"placeholder": "Address"})
    city = StringField('City', validators=[DataRequired(), Length(min=3, max=20)], render_kw={"placeholder": "City"})
    postcode = IntegerField('Postcode', validators=[DataRequired(), NumberRange(min=0, max=100000)], render_kw={"placeholder": "Postcode"})
    state = StringField('State', validators=[DataRequired(), Length(min=3, max=20)], render_kw={"placeholder": "State"})
    country_choice = get_country()
    country = SelectField(label='Country', choices=country_choice, validators=[DataRequired()], render_kw={"placeholder": "Country"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    first_name = StringField('Change First Name', validators=[DataRequired(), Length(min=3, max=20)], render_kw={"placeholder": "First Name"})
    last_name = StringField('Change Last Name', validators=[DataRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Last Name"})
    email = StringField('Change Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    picture = FileField('Change Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken. Please choose a different one.')

class DeleteAccountForm(FlaskForm):
    delete = SubmitField('Delete')
