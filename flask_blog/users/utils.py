import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
import pycountry
from flask_blog import app, mail


def send_welcome_email(user):
    msg = Message('Thanks for signing up!', sender='templars69@mail.com', recipients=[user.email])
    msg.body = f'''Hi {user.first_name.title()} {user.last_name.title()}, 

Thanks for registering with us! Here's your login information: 

Username : {user.email}

Kind regards,

Templars69

    '''
    mail.send(msg)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='templars69@mail.com', recipients=[user.email])
    msg.body = f'''Hi, 

To reset your password, visit the following link: 

{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes would be made.

Regards, 

Amazon.

    '''
    mail.send(msg)

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

def get_country():
    country_choices = []
    for country in list(pycountry.countries):
        tupple_country = (country.alpha_2, country.name)
        country_choices.append(tupple_country)
    return country_choices
