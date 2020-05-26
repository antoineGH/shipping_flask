from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_blog.models import Category

class CategoryForm(FlaskForm):
    category_name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder":"Name"})
    category_description = StringField('Category Description', validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder":"Description"})
    submit = SubmitField('Add')

    def validate_category_name(self, category_name):
        category_name = Category.query.filter_by(category_name=category_name.data).first()
        if category_name:
            raise ValidationError('That category name already exists. Please choose a different one.')

class DeleteCategoryForm(FlaskForm):
    category_delete_id = HiddenField('Delete Category ID')
    delete = SubmitField('Delete')
