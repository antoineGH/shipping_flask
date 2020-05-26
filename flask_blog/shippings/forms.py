from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange

class ShippingForm(FlaskForm):
    weight = FloatField(validators=[DataRequired(), NumberRange(min=0, max=100)], render_kw={"placeholder": "Enter package weight"})
    submit = SubmitField('Calculate')
