from flask import render_template, url_for, flash, redirect, abort, Blueprint
from flask_login import current_user, login_required
from flask_blog.categories.forms import CategoryForm, DeleteCategoryForm
from flask_blog.models import Category
from flask_blog import db

categories = Blueprint('categories', __name__)

@categories.route('/category', methods=['GET', 'POST'])
@login_required
def category():
    if current_user.role == 0:
        abort(403)
    else:
        category = Category.query.all()
        form = CategoryForm()
        form_delete = DeleteCategoryForm()

        if form.submit.data and form.validate_on_submit():
            category = Category(category_name=form.category_name.data, category_description=form.category_description.data)
            db.session.add(category)
            db.session.commit()
            flash(f'You have successfully created {category.category_name}', 'success')
            return redirect(url_for('categories.category'))

        if form_delete.delete.data and form_delete.validate_on_submit():
            todelete = Category.query.filter_by(category_id=form_delete.category_delete_id.data).first()
            Category.query.filter_by(category_id=todelete.category_id).delete()
            db.session.commit()
            flash(f'You have successfully delete {todelete.category_name}', 'success')
            return redirect(url_for('categories.category'))
        return render_template('category.html', title='Categories', form=form, form_delete=form_delete, category=category)
