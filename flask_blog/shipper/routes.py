from flask import render_template, url_for, flash, redirect, abort, Blueprint
from flask_login import current_user, login_required
from flask_blog import db
from flask_blog.shipper.forms import ShipperForm, DeleteShipperForm
from flask_blog.models import Shipper

shipper = Blueprint('shipper', __name__)

@shipper.route('/shippers', methods=['GET', 'POST'])
@login_required
def shippers():
    if current_user.role == 0:
        abort(403)
    else:
        shipper = Shipper.query.all()
        form = ShipperForm()
        form_delete = DeleteShipperForm()

        if form.submit.data and form.validate_on_submit():
            shipper = Shipper(company_name=form.company_name.data, phone=form.phone.data)
            db.session.add(shipper)
            db.session.commit()
            flash(f'You have successfully created {shipper.company_name}', 'success')
            return redirect(url_for('shipper.shippers'))

        if form_delete.delete.data and form_delete.validate_on_submit():
            todelete = Shipper.query.filter_by(shipper_id=form_delete.shipper_delete_id.data).first()
            Shipper.query.filter_by(shipper_id=todelete.shipper_id).delete()
            db.session.commit()
            flash(f'You have successfully delete {todelete.company_name}', 'success')
            return redirect(url_for('shipper.shippers'))

        return render_template('shippers.html', title='Shippers', form=form, form_delete=form_delete, shipper=shipper)
