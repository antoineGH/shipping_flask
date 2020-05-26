from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, HiddenField, SelectField
from wtforms.validators import DataRequired, NumberRange
from flask_blog.shops.utils import get_shipper_choice

class AddOrderForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0, max=10)], render_kw={"placeholder": "1"})
    product_id = HiddenField('Product_ID')
    order_details_id = HiddenField('Order Details ID')
    submit = SubmitField('Add to cart')

class UpdateOrderForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0, max=10)])
    order_details_id = HiddenField('Order Details ID')
    update = SubmitField('Update')

class CreateOrderForm(FlaskForm):
    shipper_choice = get_shipper_choice()
    shipper_id = SelectField(label='Select Shipper', validators=[DataRequired()])
    submit = SubmitField('Order')

    def __init__(self, *args, **kwargs):
        super(CreateOrderForm, self).__init__(*args, **kwargs)
        self.shipper_id.choices = get_shipper_choice()

class DeleteOrderForm(FlaskForm):
    order_details_id = HiddenField('Delete Product ID')
    delete = SubmitField('Remove')

class GenInvoiceForm(FlaskForm):
    order_number = HiddenField('Order Number')
    submit = SubmitField('Order')

class FilterForm(FlaskForm):
    filter = HiddenField('Filter')
