from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog import db, bcrypt
from flask_blog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, DeleteAccountForm, RequestResetForm, ResetPasswordForm
from flask_blog.models import User
from flask_blog.users.utils import save_picture, send_welcome_email, send_reset_email

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('shops.shop'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('shops.shop'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for(('shops.shop')))

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('shops.shop'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password, address=form.address.data, city=form.city.data, state=form.state.data, postcode=form.postcode.data, country=form.country.data, phone=form.phone.data)
        db.session.add(user)
        db.session.commit()
        send_welcome_email(user)
        flash('Your account has been created! You are now able to Login', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)

@users.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.first_name.data = current_user.first_name.title()
        form.last_name.data = current_user.last_name.title()
        form.email.data = current_user.email

    if form_delete.validate_on_submit():
        User.query.filter_by(email=current_user.email).delete()
        db.session.commit()
        flash('You account has been deleted!', 'success')
        return redirect(url_for('users.logout'))

    image_file = url_for('static', filename='profile_pics/' +  current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form, form_delete=form_delete)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('shops.shop'))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('shops.shop'))
    user = User.verify_reset(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('You password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', title='Reset Password', form=form)
   