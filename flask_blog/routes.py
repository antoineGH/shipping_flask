from flask import render_template, url_for, flash, redirect, request
from flask_blog import app, db
from flask_blog.forms import ShippingForm, ShipperForm, DeleteShipperForm
from flask_blog.models import Shipping, Customer, Orders, OrderDetails, Products, Category, Shipper
from flask_blog.functions import compare_shipping

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

@app.route('/manage_shippers', methods=['GET', 'POST'])
def manage_shippers():
    shipper = Shipper.query.all()
    
    form_shipper = ShipperForm()
    if form_shipper.validate_on_submit():
        shipper = Shipper(company_name=form_shipper.company_name.data, phone=form_shipper.phone.data)
        db.session.add(shipper)
        db.session.commit()
        flash(f'You have successfully created {shipper.company_name}', 'success')
        return redirect(url_for('manage_shippers'))

    form_delete_shipper = DeleteShipperForm()
    if form_delete_shipper.validate_on_submit(): 
        todelete = Shipper.query.filter_by(shipper_id=form_delete_shipper.shipper_delete_id.data).first()
        Shipper.query.filter_by(shipper_id=todelete.shipper_id).delete()   
        db.session.commit()
        flash(f'You have successfully delete {todelete.company_name}', 'success')
        return redirect(url_for('manage_shippers'))
    
    return render_template('manage_shippers.html', title='Manage Shippers', form_shipper=form_shipper, shipper=shipper, form_delete_shipper=form_delete_shipper)


