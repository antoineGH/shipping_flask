from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_blog.models import Shipper

class ShippingForm(FlaskForm):
    weight = FloatField('Package Weight', validators=[DataRequired(), NumberRange(min=0, max=100)], render_kw={"placeholder": "Enter package weight"})
    submit = SubmitField('Calculate')

class ShipperForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Company Name"})
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)], render_kw={"placeholder": "Phone Number"})
    submit = SubmitField('Submit')

    def validate_company_name(self, company_name):
        company_name = Shipper.query.filter_by(company_name=company_name.data).first()
        if company_name:
            raise ValidationError('That company name already exists. Please choose a different one.')

    def validate_phone(self, phone):
        phone = Shipper.query.filter_by(phone=phone.data).first()
        if phone:
            raise ValidationError('That phone number already exists. Please choose a different one.')

class DeleteShipperForm(FlaskForm):
    shipper_delete_id = IntegerField('Delete Shipper ID', validators=[DataRequired(), NumberRange(min=0, max=1000)], render_kw={"placeholder": "Shipper ID "})
    delete = SubmitField('Delete')