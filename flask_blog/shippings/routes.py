from flask import render_template, Blueprint
from flask_blog.shippings.forms import ShippingForm
from flask_blog.models import Shipping
from flask_blog.shippings.utils import compare_shipping

shippings = Blueprint('shippings', __name__)

@shippings.route('/shipping', methods=['GET', 'POST'])
def shipping():
    shipping_prices = Shipping.query.all()
    form = ShippingForm()
    shipping = compare_shipping(form.weight.data)
    return render_template('shipping.html', title='Shipping', form=form, shipping=shipping, shipping_prices=shipping_prices)
