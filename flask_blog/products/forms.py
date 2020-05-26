from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, FloatField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from flask_blog.products.utils import get_category_choice
from flask_blog.models import Products

class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder":"Name"})
    product_description = StringField('Product Description', validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder":"Description"})
    unit_price = FloatField('Unit Price', validators=[DataRequired(), NumberRange(min=0, max=100)], render_kw={"placeholder": "Price"})
    category_id = SelectField(label='Category', validators=[DataRequired()])
    picture = FileField('Change Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.category_id.choices = get_category_choice()

    def validate_product_name(self, product_name):
        product_name = Products.query.filter_by(product_name=product_name.data).first()
        if product_name:
            raise ValidationError('That product name already exists. Please choose a different one.')

class DeleteProductForm(FlaskForm):
    product_delete_id = HiddenField('Delete Product ID')
    delete = SubmitField('Delete')
