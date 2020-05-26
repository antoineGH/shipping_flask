import random
from flask_blog.models import Shipper

def get_shipper_choice():
    shipper_list = (Shipper.query.all())
    shipper_choices = []
    for i in range(len(shipper_list)):
        tupple_id_name = (str(shipper_list[i].shipper_id), shipper_list[i].company_name)
        shipper_choices.append(tupple_id_name)
    return shipper_choices

def gen_order_number():
    order_number = 'ON_' + (random.choice('abcdefghij')).capitalize()  + (random.choice('abcdefghij')).capitalize()  + str(random.randrange(1000, 9999))
    return order_number

def calc_total_item(orderuser):
    total_item = 0
    for order in orderuser:
        total_item += order.quantity
    return total_item

def calc_total_user(orderuser):
    total_user = 0
    for order in orderuser:
        total_user += order.total
    return total_user
