import os
import secrets
from PIL import Image
import random
from flask_blog import app
from flask_blog.models import Shipping, Category, Shipper
import pycountry

# --- Calculate Total Item

def calc_total_item(orderuser):
    total_item = 0
    for order in orderuser:
        total_item += order.quantity
    return total_item

# --- Calculate Total User
def calc_total_user(orderuser):
    total_user = 0
    for order in orderuser:
        total_user += order.total
    return total_user

# --- Order Details Number
def gen_order_number():
    order_number = 'ON_' + (random.choice('abcdefghij')).capitalize()  + (random.choice('abcdefghij')).capitalize()  + str(random.randrange(1000, 9999))
    return order_number 

# --- Save Pictures
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

# --- Coutries Selection
def get_country():
    country_choices=[]
    for country in list(pycountry.countries):
        tupple_country = (country.alpha_2, country.name)
        country_choices.append(tupple_country)
    return country_choices

# --- Category Choices
def get_category_choice():
    category_list = (Category.query.all())
    category_choices = []
    for i in range(len(category_list)):
        tupple_id_name = (str(category_list[i].category_id), category_list[i].category_name) 
        category_choices.append(tupple_id_name)
    return category_choices

# --- Shipper Choices
def get_shipper_choice():
    shipper_list = (Shipper.query.all())
    shipper_choices = []
    for i in range(len(shipper_list)):
        tupple_id_name = (str(shipper_list[i].shipper_id), shipper_list[i].company_name)
        shipper_choices.append(tupple_id_name)
    return shipper_choices

# --- Shipping Functions 
def ground_shipping(weight):
  if weight <= 2:
    gs_lt_2 = Shipping.query.filter_by(method='Ground Shipping').filter_by(weight='<2lb').first()
    cost = (weight * gs_lt_2.price_per_pound) + gs_lt_2.flat_charges
  elif weight <= 6:
    gs_lt_6 = Shipping.query.filter_by(method='Ground Shipping').filter_by(weight='<6lb').first()
    cost = (weight * gs_lt_6.price_per_pound) + gs_lt_6.flat_charges
  elif weight <= 10:
    gs_lt_10 = Shipping.query.filter_by(method='Ground Shipping').filter_by(weight='<10lb').first()
    cost = (weight * gs_lt_10.price_per_pound) + gs_lt_10.flat_charges
  else :
    gs_mt_10 = Shipping.query.filter_by(method='Ground Shipping').filter_by(weight='>10lb').first()
    cost = (weight * gs_mt_10.price_per_pound) + gs_mt_10.flat_charges
  return cost

def drone_shipping(weight):
    if weight <= 2:
        ds_lt_2 = Shipping.query.filter_by(method='Drone Shipping').filter_by(weight='<2lb').first()
        cost = (weight * ds_lt_2.price_per_pound) 
    elif weight <= 6:
        ds_lt_6 = Shipping.query.filter_by(method='Drone Shipping').filter_by(weight='<6lb').first()
        cost = (weight * ds_lt_6.price_per_pound)
    elif weight <= 10:
        ds_lt_10 = Shipping.query.filter_by(method='Drone Shipping').filter_by(weight='<10lb').first()
        cost = (weight * ds_lt_10.price_per_pound)
    else :
        ds_mt_10 = Shipping.query.filter_by(method='Drone Shipping').filter_by(weight='>10lb').first()
        cost = (weight * ds_mt_10.price_per_pound)
    return cost
      
def compare_shipping(weight=None):
    if weight:
        cost_ground = ground_shipping(weight)
        cost_drone = drone_shipping(weight)
        if (cost_ground < cost_drone) and (cost_ground < cost_premium):
            return cost_ground, "Ground Shipping"
        elif (cost_drone < cost_ground) and (cost_drone < cost_premium):
            return cost_drone, "Drone Shipping"
        else:
            return cost_premium, "Premium Shipping"
    else:
        return None

cost_premium = (Shipping.query.filter_by(method='Premium Shipping').first()).price_per_pound