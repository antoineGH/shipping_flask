import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, make_response
import pdfkit
from flask_blog import app, db, bcrypt
from flask_blog.forms import ShippingForm, ShipperForm, DeleteShipperForm, CategoryForm, DeleteCategoryForm, ProductForm, DeleteProductForm, RegistrationForm, LoginForm, UpdateAccountForm, DeleteAccountForm, AddOrderForm, CreateOrderForm, GenInvoiceForm
from flask_blog.models import Shipping, User, Orders, OrderDetails, Products, Category, Shipper
from flask_blog.functions import compare_shipping, get_category_choice, save_picture, save_picture_product, gen_order_number, calc_total_user
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import and_

@app.route('/shipping', methods=['GET','POST'])
def shipping():
    shipping_prices = Shipping.query.all()
    form = ShippingForm()
    shipping = compare_shipping(form.weight.data)
    return render_template('shipping.html', title='Shipping', form=form, shipping=shipping, shipping_prices=shipping_prices)

@app.route('/shippers', methods=['GET', 'POST'])
@login_required
def shippers():
    shipper = Shipper.query.all()
    form = ShipperForm()
    form_delete = DeleteShipperForm()

    if form.submit.data and form.validate_on_submit():
        shipper = Shipper(company_name=form.company_name.data, phone=form.phone.data)
        db.session.add(shipper)
        db.session.commit()
        flash(f'You have successfully created {shipper.company_name}', 'success')
        return redirect(url_for('shippers'))

    if form_delete.delete.data and form_delete.validate_on_submit(): 
        todelete = Shipper.query.filter_by(shipper_id=form_delete.shipper_delete_id.data).first()
        Shipper.query.filter_by(shipper_id=todelete.shipper_id).delete()   
        db.session.commit()
        flash(f'You have successfully delete {todelete.company_name}', 'success')
        return redirect(url_for('shippers'))

    return render_template('shippers.html', title='Shippers', form=form, form_delete=form_delete, shipper=shipper)

@app.route('/category', methods=['GET', 'POST'])
@login_required
def category():
    category = Category.query.all()
    form = CategoryForm()
    form_delete = DeleteCategoryForm()

    if form.submit.data and form.validate_on_submit():
        category = Category(category_name=form.category_name.data, category_description=form.category_description.data)
        db.session.add(category)
        db.session.commit()
        flash(f'You have successfully created {category.category_name}', 'success')
        return redirect(url_for('category'))

    if form_delete.delete.data and form_delete.validate_on_submit(): 
        todelete = Category.query.filter_by(category_id=form_delete.category_delete_id.data).first()
        Category.query.filter_by(category_id=todelete.category_id).delete()   
        db.session.commit()
        flash(f'You have successfully delete {todelete.category_name}', 'success')
        return redirect(url_for('category'))
    
    return render_template('category.html', title='Categories', form=form, form_delete=form_delete, category=category)

@app.route('/product', methods=['GET', 'POST'])
@login_required
def product():
    product = Products.query.all()
    form = ProductForm()
    form_delete = DeleteProductForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture_product(form.picture.data)     
            product = Products(product_name=form.product_name.data, product_description=form.product_description.data, unit_price=form.unit_price.data, category_id=form.category_id.data, image_product=picture_file)
        else:
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
        return redirect(url_for('shop'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password, address=form.address.data, city=form.city.data, state=form.state.data, postcode=form.postcode.data, country=form.country.data, phone=form.phone.data)
        db.session.add(user)
        db.session.commit()
        flash('You account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('shop'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('shop'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    form_delete = DeleteAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('You account has been updated!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.first_name.data = current_user.first_name.title()
        form.last_name.data = current_user.last_name.title()
        form.email.data = current_user.email

    if form_delete.validate_on_submit():
        User.query.filter_by(email=current_user.email).delete()
        db.session.commit()
        flash('You account has been deleted!', 'success')
        return redirect(url_for('logout'))

    image_file = url_for('static', filename='profile_pics/' +  current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form, form_delete=form_delete)

@app.route('/')
@app.route('/shop', methods=['GET','POST'])
def shop():
    products = Products.query.all()  
    form = AddOrderForm()

    if form.validate_on_submit():
        if current_user.is_authenticated:
            product = Products.query.filter_by(product_id=form.product_id.data).first()
            price = product.unit_price
            product_id = product.product_id
            quantity = form.quantity.data
            user_id = current_user.user_id
            total = float(quantity * price)
        
            orderdetails = OrderDetails.query.filter(and_(OrderDetails.product_id == form.product_id.data, OrderDetails.order_id == 0)).first()
                 
            if orderdetails:
                orderdetails.quantity += form.quantity.data
                orderdetails.total += (form.quantity.data * orderdetails.price)
            else:
                orderdetails = OrderDetails(quantity=quantity, price=price, total=total, user_id=user_id , order_id = 0, product_id=product_id)

            db.session.add(orderdetails)
            db.session.commit()
            flash('Successfully added {} to your cart.'.format(product.product_name), 'success')
            return redirect(url_for('shop'))
    
        elif form.validate_on_submit():
            flash('Please Log In to Add in your Cart.', 'warning')
            return redirect(url_for('login'))
    
    elif request.method == 'GET':
        form.quantity.data = 1    

    return render_template('shop.html', title='Shop', products=products, form=form, )

@app.route('/cart', methods=['GET','POST'])
def cart():
    form = CreateOrderForm()
    orderuser = OrderDetails.query.filter_by(user_id=current_user.user_id).all()
    order_details = OrderDetails.query.filter_by(user_id=current_user.user_id).all()

    total_user = calc_total_user(orderuser)

    if form.validate_on_submit():
        if current_user.is_authenticated:
            order = Orders(order_number=gen_order_number(), user_id=current_user.user_id, shipper_id=form.shipper_id.data) 
            db.session.add(order)
            db.session.commit()

            for order_detail in order_details:
                order_detail.order_id = order.order_id
                order_detail.user_id = 9999
            db.session.commit()
            return redirect(url_for('confirm'))

        elif form.validate_on_submit():
            flash('Please Log In to Add to Cart.', 'warning')
            return redirect(url_for('login'))

    return render_template('cart.html', title='Cart', form=form, order_details=order_details, total_user=total_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for(('shop')))

@app.route('/confirm', methods=['GET','POST'])
@login_required
def confirm():
    order_user = Orders.query.filter_by(user_id=current_user.user_id).all()
    form = GenInvoiceForm()

    order_total = {}
    for order in order_user:
        order_details = OrderDetails.query.filter_by(order_id=order.order_id).all()
        total = 0
        for order_detail in order_details:      
            total= sum([order_detail.total], start=total)
        order_total[order.order_id] = total

    order_details = {}
    for order in order_user:
        order_detail_id = OrderDetails.query.filter_by(order_id=order.order_id).all()  
        order_details[order.order_id] = order_detail_id

    if form.validate_on_submit():
        url_redirect = '/gen/' + form.order_number.data
        return redirect(url_redirect)
         
    return render_template('confirm.html', title='Order', form=form, order_user=order_user, order_details=order_details, order_total=order_total)

@app.route('/gen/<order_number>') 
def pdf_template(order_number):
    
    order_user = Orders.query.filter_by(order_number=order_number).first()
    order_detail_list = OrderDetails.query.filter_by(order_id=order_user.order_id).all()  

    total = 0
    for order_detail in order_detail_list:
        total= sum([order_detail.total], start=total)

    rendered = render_template('pdf_template.html', order_user=order_user, order_detail_list=order_detail_list, total=total)

    pdf = pdfkit.from_string(rendered, False)

    response = make_response(pdf)
    response.headers['content-type'] = 'application/pdf'
    response.headers['content-disposition'] = 'inline; filename=invoice.pdf'

    return response


