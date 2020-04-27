import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_blog import app, db, bcrypt
from flask_blog.forms import ShippingForm, ShipperForm, DeleteShipperForm, CategoryForm, DeleteCategoryForm, ProductForm, DeleteProductForm, RegistrationForm, LoginForm, UpdateAccountForm
from flask_blog.models import Shipping, User, Orders, OrderDetails, Products, Category, Shipper
from flask_blog.functions import compare_shipping, get_category_choice
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/shipping', methods=['GET','POST'])
def shipping():
    shipping_prices = Shipping.query.all()
    form = ShippingForm()
    shipping = compare_shipping(form.weight.data)
    return render_template('shipping.html', title='Shipping', form=form, shipping=shipping, shipping_prices=shipping_prices)

@app.route('/shippers', methods=['GET', 'POST'])
def shippers():
    shipper = Shipper.query.all()
    form = ShipperForm()
    form_delete = DeleteShipperForm()

    if form.validate_on_submit():
        shipper = Shipper(company_name=form.company_name.data, phone=form.phone.data)
        db.session.add(shipper)
        db.session.commit()
        flash(f'You have successfully created {shipper.company_name}', 'success')
        return redirect(url_for('shippers'))

    if form_delete.validate_on_submit(): 
        todelete = Shipper.query.filter_by(shipper_id=form_delete.shipper_delete_id.data).first()
        Shipper.query.filter_by(shipper_id=todelete.shipper_id).delete()   
        db.session.commit()
        flash(f'You have successfully delete {todelete.company_name}', 'success')
        return redirect(url_for('shippers'))

    return render_template('shippers.html', title='Shippers', form=form, form_delete=form_delete, shipper=shipper)

@app.route('/category', methods=['GET', 'POST'])
def category():
    category = Category.query.all()
    form = CategoryForm()
    form_delete = DeleteCategoryForm()

    if form.validate_on_submit():
        category = Category(category_name=form.category_name.data, category_description=form.category_description.data)
        db.session.add(category)
        db.session.commit()
        flash(f'You have successfully created {category.category_name}', 'success')
        return redirect(url_for('category'))

    if form_delete.validate_on_submit(): 
        todelete = Category.query.filter_by(category_id=form_delete.category_delete_id.data).first()
        Category.query.filter_by(category_id=todelete.category_id).delete()   
        db.session.commit()
        flash(f'You have successfully delete {todelete.category_name}', 'success')
        return redirect(url_for('category'))
    
    return render_template('category.html', title='Categories', form=form, form_delete=form_delete, category=category)

@app.route('/product', methods=['GET', 'POST'])
def product():
    product = Products.query.all()
    category = Category.query.all()
    form = ProductForm()
    form_delete = DeleteProductForm()
    
    if form.validate_on_submit():
        product = Products(product_name=form.product_name.data, product_description=form.product_description.data, unit_price=form.unit_price.data, category_id=form.category_id.data)
        db.session.add(product)
        db.session.commit()
        flash(f'You have successfully created {product.product_name}', 'success')
        return redirect(url_for('product'))

    if form_delete.validate_on_submit(): 
        todelete = Products.query.filter_by(product_id=form_delete.product_delete_id.data).first()
        Products.query.filter_by(product_id=todelete.product_id).delete()   
        db.session.commit()
        flash(f'You have successfully delete {todelete.product_name}', 'success')
        return redirect(url_for('product'))
    
    return render_template('product.html', title='Products', form=form, product=product, form_delete=form_delete, category=category)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password, address=form.address.data, city=form.city.data, state=form.state.data, postcode=form.postcode.data, country=form.country.data, phone=form.phone.data)
        db.session.add(user)
        db.session.commit()
        flash('You account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (90, 90)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('You account has been updated!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.first_name.data = current_user.first_name.title()
        form.last_name.data = current_user.last_name.title()
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' +  current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for(('home')))