from flask_blog.models import Shipping, Category

# --- Category Choices
 
def get_category_choice():
    category_list = (Category.query.all())
    category_choices = []
    for i in range(len(category_list)):
        tupple_id_name = (str(category_list[i].category_id), category_list[i].category_name) 
        category_choices.append(tupple_id_name)
    return category_choices

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

# Variables 

cost_premium = (Shipping.query.filter_by(method='Premium Shipping').first()).price_per_pound