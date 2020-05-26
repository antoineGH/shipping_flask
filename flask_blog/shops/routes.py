from flask import render_template, url_for, flash, redirect, request, make_response, Markup, Blueprint
from flask_login import current_user, login_required
import pdfkit
from sqlalchemy import and_
from flask_blog import db
from flask_blog.shops.forms import AddOrderForm, CreateOrderForm, GenInvoiceForm, FilterForm, DeleteOrderForm, UpdateOrderForm
from flask_blog.models import Orders, OrderDetails, Products, Category
from flask_blog.shops.utils import gen_order_number, calc_total_user, calc_total_item

shops = Blueprint('shops', __name__)

@shops.context_processor
def inject_quantity():
    if current_user.is_authenticated:
        orderuser = OrderDetails.query.filter_by(user_id=current_user.user_id).all()
        total_item = calc_total_item(orderuser)
        return {'g_total_item': total_item}
    else:
        return {'g_total_item': "empty"}

@shops.route('/')
@shops.route('/shop', methods=['GET', 'POST'])
def shop():
    page = request.args.get('page', 1, type=int)
    filter_str = request.args.get('filter_str', None, type=str)
    form = AddOrderForm()
    filterform = FilterForm()

    if request.method == 'GET':
        form.quantity.data = 1
    if current_user.is_authenticated:

        if filterform.filter.data == 'asc':
            print('asc form')
            products = Products.query.order_by(Products.unit_price.asc()).paginate(per_page=8, page=page)
            return render_template('shop.html', title='Shop', products=products, form=form, filter_str='asc', filterform=filterform)

        elif filterform.filter.data == 'desc':
            print('desc form')
            products = Products.query.order_by(Products.unit_price.desc()).paginate(per_page=8, page=page)
            return render_template('shop.html', title='Shop', products=products, form=form, filter_str='desc', filterform=filterform)

        elif filterform.filter.data == 'az':
            print('az form')
            products = Products.query.order_by(Products.product_name.asc()).paginate(per_page=8, page=page)
            return render_template('shop.html', title='Shop', products=products, form=form, filter_str='az', filterform=filterform)

        elif filterform.filter.data == 'za':
            print('za form')
            products = Products.query.order_by(Products.product_name.desc()).paginate(per_page=8, page=page)
            return render_template('shop.html', title='Shop', products=products, form=form, filter_str='za', filterform=filterform)

        elif filter_str == 'asc':
            print('asc not form')
            products = Products.query.order_by(Products.unit_price.asc()).paginate(per_page=8, page=page)
            return render_template('shop.html', title='Shop', products=products, form=form, filter_str='asc', filterform=filterform)

        elif filter_str == 'desc':
            print('desc not form')
            products = Products.query.order_by(Products.unit_price.desc()).paginate(per_page=8, page=page)
            return render_template('shop.html', title='Shop', products=products, form=form, filter_str='desc', filterform=filterform)

        elif filter_str == 'az':
            print('az not form')
            products = Products.query.order_by(Products.product_name.asc()).paginate(per_page=8, page=page)
            return render_template('shop.html', title='Shop', products=products, form=form, filter_str='az', filterform=filterform)

        elif filter_str == 'za':
            print('za not form')
            products = Products.query.order_by(Products.product_name.desc()).paginate(per_page=8, page=page)
            return render_template('shop.html', title='Shop', products=products, form=form, filter_str='za', filterform=filterform)

        if form.validate_on_submit():
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
                orderdetails = OrderDetails(quantity=quantity, price=price, total=total, user_id=user_id, order_id=0, product_id=product_id)

            db.session.add(orderdetails)
            db.session.commit()
            flash(Markup('You\'ve just added {} to your <a href="/cart">Cart</a>'.format(product.product_name)), 'success')
            return redirect(url_for('shops.shop'))
    elif form.validate_on_submit() or filterform.validate_on_submit():
        flash('Please Log In to Add in your Cart.', 'warning')
        return redirect(url_for('users.login'))

    products = Products.query.paginate(per_page=8, page=page)

    return render_template('shop.html', title='Shop', products=products, form=form, filter_str=filter_str, filterform=filterform)

@shops.route('/cart', methods=['GET', 'POST'])
def cart():
    form = CreateOrderForm()
    form_delete = DeleteOrderForm()
    form_update = UpdateOrderForm()
    orderuser = OrderDetails.query.filter_by(user_id=current_user.user_id).all()
    order_details = OrderDetails.query.filter_by(user_id=current_user.user_id).all()

    if form.validate_on_submit():
        if current_user.is_authenticated:
            order = Orders(order_number=gen_order_number(), user_id=current_user.user_id, shipper_id=form.shipper_id.data)
            db.session.add(order)
            db.session.commit()

            for order_detail in order_details:
                order_detail.order_id = order.order_id
                order_detail.user_id = 9999
            db.session.commit()
            return redirect(url_for('shops.confirm'))

        elif form.validate_on_submit():
            flash('Please Log In to Add to Cart.', 'warning')
            return redirect(url_for('users.login'))

    if form_update.update.data:
        if request.form['update'] == 'plus':
            to_update = OrderDetails.query.filter_by(user_id=current_user.user_id).filter_by(order_details_id=form_update.order_details_id.data).first()
            to_update.quantity = sum([to_update.quantity], start=1)
            to_update.total = 0
            to_update.total += (to_update.quantity * to_update.price)
            db.session.commit()
            total_item = calc_total_item(orderuser)
            total_user = calc_total_user(orderuser)
            return redirect(url_for('shops.cart'))

        elif request.form['update'] == 'minus':
            to_update = OrderDetails.query.filter_by(user_id=current_user.user_id).filter_by(order_details_id=form_update.order_details_id.data).first()
            to_update.quantity = sum([to_update.quantity], start=-1)
            to_update.total = 0
            to_update.total += (to_update.quantity * to_update.price)
            if to_update.total == 0:
                to_delete = OrderDetails.query.filter_by(user_id=current_user.user_id).filter_by(order_details_id=to_update.order_details_id).all()

                for delete in to_delete:
                    OrderDetails.query.filter_by(order_details_id=delete.order_details_id).delete()

            db.session.commit()

            return redirect(url_for('shops.cart'))
        else:
            pass
    if form_delete.delete.data and form_delete.validate_on_submit():
        todelete = OrderDetails.query.filter_by(user_id=current_user.user_id).filter_by(order_details_id=form_delete.order_details_id.data).all()
        for delete in todelete:
            OrderDetails.query.filter_by(order_details_id=delete.order_details_id).delete()
        db.session.commit()
        flash('Successfully deleted from your cart', 'success')
        return redirect(url_for('shops.cart'))

    total_item = calc_total_item(orderuser)
    total_user = calc_total_user(orderuser)

    return render_template('cart.html', title='Cart', form=form, form_delete=form_delete, order_details=order_details, total_user=total_user, total_item=total_item, form_update=form_update)

@shops.route('/confirm', methods=['GET', 'POST'])
@login_required
def confirm():
    order_user = Orders.query.filter_by(user_id=current_user.user_id).order_by(Orders.date_order.desc()).all()
    form = GenInvoiceForm()

    order_total = {}
    for order in order_user:
        order_details = OrderDetails.query.filter_by(order_id=order.order_id).all()
        total = 0
        for order_detail in order_details:
            total = sum([order_detail.total], start=total)
        order_total[order.order_id] = total

    order_details = {}
    for order in order_user:
        order_detail_id = OrderDetails.query.filter_by(order_id=order.order_id).all()
        order_details[order.order_id] = order_detail_id

    if form.validate_on_submit():
        url_redirect = '/gen/' + form.order_number.data
        return redirect(url_redirect)
    return render_template('confirm.html', title='Order', form=form, order_user=order_user, order_details=order_details, order_total=order_total)

@shops.route('/gen/<order_number>')
def pdf_template(order_number):
    order_user = Orders.query.filter_by(order_number=order_number).first()
    order_detail_list = OrderDetails.query.filter_by(order_id=order_user.order_id).all()

    total = 0
    for order_detail in order_detail_list:
        total = sum([order_detail.total], start=total)

    rendered = render_template('pdf_template.html', order_user=order_user, order_detail_list=order_detail_list, total=total)

    pdf = pdfkit.from_string(rendered, False)

    response = make_response(pdf)
    response.headers['content-type'] = 'shoplication/pdf'
    response.headers['content-disposition'] = 'inline; filename=invoice.pdf'

    return response

@shops.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_desc(product_id):
    form = AddOrderForm()
    product = Products.query.get_or_404(product_id)

    if request.method == 'GET':
        form.quantity.data = 1

    if current_user.is_authenticated:
        if form.validate_on_submit():
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
                orderdetails = OrderDetails(quantity=quantity, price=price, total=total, user_id=user_id, order_id=0, product_id=product_id)

            db.session.add(orderdetails)
            db.session.commit()
            return redirect(url_for('shops.shop'))
    elif form.validate_on_submit():
        flash('Please Log In to Add in your Cart.', 'warning')
        return redirect(url_for('users.login'))

    return render_template('product_desc.html', title=product.product_name, product=product, form=form)

@shops.route('/category/<int:category_id>', methods=['GET', 'POST'])
def shop_category(category_id):
    page = request.args.get('page', 1, type=int)
    products = Products.query.filter_by(category_id=category_id).paginate(per_page=8, page=page)
    category = Category.query.filter_by(category_id=category_id).first()
    category_name = category.category_name.title()
    form = AddOrderForm()

    if request.method == 'GET':
        form.quantity.data = 1

    if current_user.is_authenticated:
        if 'asc' in request.form:
            products = Products.query.order_by(Products.unit_price.asc()).filter_by(category_id=category_id).paginate(per_page=8, page=page)
            form.quantity.data = 1
            return render_template('shop_category.html', title='Shop - '+ category_name, products=products, form=form, category_name=category_name)

        if 'desc' in request.form:
            products = Products.query.order_by(Products.unit_price.desc()).filter_by(category_id=category_id).paginate(per_page=8, page=page)
            form.quantity.data = 1
            return render_template('shop_category.html', title='Shop - '+ category_name, products=products, form=form, category_name=category_name)

        if 'az' in request.form:
            products = Products.query.order_by(Products.product_name.asc()).filter_by(category_id=category_id).paginate(per_page=8, page=page)
            form.quantity.data = 1
            return render_template('shop_category.html', title='Shop - '+ category_name, products=products, form=form, category_name=category_name)

        if 'za' in request.form:
            products = Products.query.order_by(Products.product_name.desc()).filter_by(category_id=category_id).paginate(per_page=8, page=page)
            form.quantity.data = 1
            return render_template('shop_category.html', title='Shop - '+ category_name, products=products, form=form, category_name=category_name)


        if form.validate_on_submit():
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
                orderdetails = OrderDetails(quantity=quantity, price=price, total=total, user_id=user_id, order_id=0, product_id=product_id)

            db.session.add(orderdetails)
            db.session.commit()
            return redirect(url_for('shops.shop'))
    elif form.validate_on_submit() or 'asc' in request.form or 'desc' in request.form or 'az' in request.form or 'za' in request.form:
        flash('Please Log In to Add in your Cart.', 'warning')
        return redirect(url_for('users.login'))
    return render_template('shop_category.html', title='Shop - '+ category_name, products=products, form=form, category_name=category_name)
