from flask import render_template, url_for, flash, redirect, request
from flask_blog import app, db
from flask_blog.forms import ShippingForm, ShipperForm, DeleteShipperForm, CategoryForm, DeleteCategoryForm, ProductForm, DeleteProductForm
from flask_blog.models import Shipping, Customer, Orders, OrderDetails, Products, Category, Shipper
from flask_blog.functions import compare_shipping, get_category_choice

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/shipping', methods=['GET','POST'])
def shipping():
    shipping_prices = Shipping.query.all()
    form_shipping = ShippingForm()
    shipping = compare_shipping(form_shipping.weight.data)
    return render_template('shipping.html', title='Python', form_shipping=form_shipping, shipping=shipping, shipping_prices=shipping_prices)

@app.route('/shippers', methods=['GET', 'POST'])
def shippers():
    shipper = Shipper.query.all()
    form_shipper = ShipperForm()
    form_delete_shipper = DeleteShipperForm()

    if form_shipper.validate_on_submit():
        shipper = Shipper(company_name=form_shipper.company_name.data, phone=form_shipper.phone.data)
        db.session.add(shipper)
        db.session.commit()
        flash(f'You have successfully created {shipper.company_name}', 'success')
        return redirect(url_for('shippers'))

    if form_delete_shipper.validate_on_submit(): 
        todelete = Shipper.query.filter_by(shipper_id=form_delete_shipper.shipper_delete_id.data).first()
        Shipper.query.filter_by(shipper_id=todelete.shipper_id).delete()   
        db.session.commit()
        flash(f'You have successfully delete {todelete.company_name}', 'success')
        return redirect(url_for('shippers'))
    
    return render_template('shippers.html', title='Shippers', form_shipper=form_shipper, shipper=shipper, form_delete_shipper=form_delete_shipper)

@app.route('/category', methods=['GET', 'POST'])
def category():
    category = Category.query.all()
    form_category = CategoryForm()
    form_delete_category = DeleteCategoryForm()

    if form_category.validate_on_submit():
        category = Category(category_name=form_category.category_name.data, category_description=form_category.category_description.data)
        db.session.add(category)
        db.session.commit()
        flash(f'You have successfully created {category.category_name}', 'success')
        return redirect(url_for('category'))

    if form_delete_category.validate_on_submit(): 
        todelete = Category.query.filter_by(category_id=form_delete_category.category_delete_id.data).first()
        Category.query.filter_by(category_id=todelete.category_id).delete()   
        db.session.commit()
        flash(f'You have successfully delete {todelete.category_name}', 'success')
        return redirect(url_for('category'))
    
    return render_template('category.html', title='Categories', form_category=form_category, category=category, form_delete_category=form_delete_category)

@app.route('/product', methods=['GET', 'POST'])
def product():
    product = Products.query.all()
    category = Category.query.all()
    form_product = ProductForm()
    form_delete_product = DeleteProductForm()
    

    if form_product.validate_on_submit():
        product = Products(product_name=form_product.product_name.data, product_description=form_product.product_description.data, unit_price=form_product.unit_price.data, category_id=form_product.category_id.data)
        db.session.add(product)
        db.session.commit()
        flash(f'You have successfully created {product.product_name}', 'success')
        return redirect(url_for('product'))

    if form_delete_product.validate_on_submit(): 
        todelete = Products.query.filter_by(product_id=form_delete_product.product_delete_id.data).first()
        Products.query.filter_by(product_id=todelete.product_id).delete()   
        db.session.commit()
        flash(f'You have successfully delete {todelete.product_name}', 'success')
        return redirect(url_for('product'))
    
    return render_template('product.html', title='Products', form_product=form_product, product=product, form_delete_product=form_delete_product, category=category)