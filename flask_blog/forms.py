from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_blog.models import Shipper, Category, Products
from flask_blog.functions import get_category_choice

class ShippingForm(FlaskForm):
    weight = FloatField('Package Weight', validators=[DataRequired(), NumberRange(min=0, max=100)], render_kw={"placeholder": "Enter package weight"})
    submit = SubmitField('Calculate')

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
    shipper_delete_id = IntegerField('Delete Shipper ID', validators=[DataRequired(), NumberRange(min=0, max=1000)], render_kw={"placeholder": "Shipper ID "})
    delete = SubmitField('Delete')

    def validate_shipper_delete_id(self, shipper_delete_id):
        shipper_delete_id = Shipper.query.filter_by(shipper_id=shipper_delete_id.data).first()
        if not shipper_delete_id:
            raise ValidationError('Please select an existing Shipper ID.')

class CategoryForm(FlaskForm):
    category_name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder":"Category Name"})
    category_description = StringField('Category Description', validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder":"Category Description"})
    submit = SubmitField('Add')

    def validate_category_name(self, category_name):
        category_name = Category.query.filter_by(category_name=category_name.data).first()
        if category_name:
            raise ValidationError('That category name already exists. Please choose a different one.')

class DeleteCategoryForm(FlaskForm):
    category_delete_id = IntegerField('Delete Category ID', validators=[DataRequired(), NumberRange(min=0, max=1000)], render_kw={"placeholder": "Category ID "})
    delete = SubmitField('Delete')

    def validate_category_delete_id(self, category_delete_id):
        category_delete_id = Category.query.filter_by(category_id=category_delete_id.data).first()
        if not category_delete_id:
            raise ValidationError('Please select an existing Category ID.')

class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder":"Product Name"})
    product_description = StringField('Product Description', validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder":"Product Description"})
    unit_price = FloatField('Unit Price', validators=[DataRequired(), NumberRange(min=0, max=100)], render_kw={"placeholder": "Enter Unit Price"})
    category_choice = get_category_choice()
    category_id = SelectField(label='Category', choices=category_choice)
    submit = SubmitField('Add')

    def validate_product_name(self, product_name):
        product_name = Products.query.filter_by(product_name=product_name.data).first()
        if product_name:
            raise ValidationError('That product name already exists. Please choose a different one.')

class DeleteProductForm(FlaskForm):
    product_delete_id =  IntegerField('Delete Product ID', validators=[DataRequired(), NumberRange(min=0, max=1000)], render_kw={"placeholder": "Product ID "})
    delete = SubmitField('Delete')

    def validate_product_delete_it(self, product_delete_id):
        product_delete_id = Category.query.filter_by(product_id=product_delete_id.data).first()
        if not product_delete_id:
            raise ValidationError('Please select an existing Product ID.')