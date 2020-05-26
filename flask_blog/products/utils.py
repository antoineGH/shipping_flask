import os
import secrets
from PIL import Image
from flask_blog import app
from flask_blog.models import Category

def get_category_choice():
    category_list = (Category.query.all())
    category_choices = []
    for i in range(len(category_list)):
        tupple_id_name = (str(category_list[i].category_id), category_list[i].category_name) 
        category_choices.append(tupple_id_name)
    return category_choices

def save_picture_product(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/products_pics', picture_fn)

    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
