from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flask_blog import db
from flask_blog.products.forms import ProductForm, DeleteProductForm
from flask_blog.models import Products
from flask_blog.products.utils import save_picture_product

products = Blueprint('products', __name__)

@products.route('/product', methods=['GET', 'POST'])
@login_required
def product():
    print(current_user.role)
    print(type(current_user.role))
    if current_user.role == 0:
        abort(403)
    else:
        page = request.args.get('page', 1, type=int)
        product = Products.query.paginate(per_page=8, page=page)
        form = ProductForm()
        form_delete = DeleteProductForm()
    
        if form.submit.data and form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture_product(form.picture.data)     
                product = Products(product_name=form.product_name.data, product_description=form.product_description.data, unit_price=form.unit_price.data, category_id=form.category_id.data, image_product=picture_file)
            else:
                product = Products(product_name=form.product_name.data, product_description=form.product_description.data, unit_price=form.unit_price.data, category_id=form.category_id.data)
        
            db.session.add(product)
            db.session.commit()
            flash(f'You have successfully created {product.product_name}', 'success')
            return redirect(url_for('products.product'))

        if form_delete.delete.data and form_delete.validate_on_submit(): 
            todelete = Products.query.filter_by(product_id=form_delete.product_delete_id.data).first()
            Products.query.filter_by(product_id=todelete.product_id).delete()   
            db.session.commit()
            flash(f'You have successfully delete {todelete.product_name}', 'success')
            return redirect(url_for('products.product', page=page))
    
        return render_template('product.html', title='Products', form=form, product=product, form_delete=form_delete)
