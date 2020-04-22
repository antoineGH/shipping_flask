from datetime import datetime
from flask_blog import db

class Shipping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(40), nullable=False)
    weight = db.Column(db.String(40), nullable=False)
    price_per_pound = db.Column(db.Float, nullable=False)
    flat_charges = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Shipping('id: {self.id}, method: {self.method}, weight: {self.weight}, price_per_pound: {self.price_per_pound}, flat_charges: {self.flat_charges}')"

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(40), nullable=False)
    state = db.Column(db.String(40), nullable=False)
    postcode = db.Column(db.String(40), nullable=False)
    country = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    orders = db.relationship('Orders', backref='buy', lazy=True)

    def __repr__(self):
        return f"Customer('customer_id: {self.customer_id}, first_name: {self.first_name}, last_name: {self.last_name}, phone: {self.phone}, email: {self.email}')"

class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    shipper_id = db.Column(db.Integer, db.ForeignKey('shipper.shipper_id'), nullable=False)
    order_details = db.relationship('Details', backref='has', lazy=True)
    customer = db.relationship('Customer', backref='ordered', lazy=True)
    shipper = db.relationship('Shipper', backref='managed', lazy=True)
    
    def __repr__(self):
        return f"Orders('order_id: {self.order_id}, order_number: {self.order_number},)"

class Details(db.Model):
    order_details_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)  
    total = db.Column(db.Float, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    order = db.relationship('Orders', backref='fromorder', lazy=True)
    product = db.relationship('Products', backref='has', lazy=True)
    
    def __repr__(self):
        return f"Details('order_details_id: {self.order_details_id}, quantity: {self.quantity}, price: {self.price}, total: {self.total}')"

class Products(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(40), nullable=False)
    product_description = db.Column(db.String(100), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    order_details_id = db.Column(db.Integer, db.ForeignKey('details.order_details_id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    
    def __repr__(self):
        return f"Products('product_id: {self.product_id}, product_name: {self.product_name}, product_description: {self.product_description}, unit_price: {self.unit_price}')"

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(40), nullable=False)
    category_description = db.Column(db.String(100), nullable=False)
    products = db.relationship('Products', backref='contains', lazy=True)
    
    def __repr__(self):
        return f"Category('category_id: {self.category_id}, category_name: {self.category_name}, category_description: {self.category_description}')"

class Shipper(db.Model):
    shipper_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    orders = db.relationship('Orders', backref='shipped', lazy=True)
    
    def __repr__(self):
        return f"Shipper('shipper_id: {self.shipper_id}, company_name: {self.company_name}, phone: {self.phone}')"