from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_blog.models import Shipper

class ShipperForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Company Name"})
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)], render_kw={"placeholder": "Phone Number"})
    submit = SubmitField('Add')

    def validate_company_name(self, company_name):
        company_name = Shipper.query.filter_by(company_name=company_name.data).first()
        if company_name:
            raise ValidationError('That company name already exists. Please choose a different one.')

    def validate_phone(self, phone):
        phone = Shipper.query.filter_by(phone=phone.data).first()
        if phone:
            raise ValidationError('That phone number already exists. Please choose a different one.')

class DeleteShipperForm(FlaskForm):
    shipper_delete_id = HiddenField('Delete Shipper ID')
    delete = SubmitField('Delete')
