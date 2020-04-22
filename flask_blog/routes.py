from flask import render_template, url_for, flash, redirect, request
from flask_blog import app, db
from flask_blog.forms import ShippingForm
from flask_blog.models import Shipping, Customer, Orders, Details, Products, Category, Shipper
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