from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange

class ShippingForm(FlaskForm):
    weight = FloatField('Package Weight', validators=[DataRequired(), NumberRange(min=0, max=100)], render_kw={"placeholder": "Enter package weight"})
    submit = SubmitField('Calculate')