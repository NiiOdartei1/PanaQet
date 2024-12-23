import sqlite3
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import SubmitField
from database import db
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    country_code = db.Column(db.String(5), nullable=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=True)
    country = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(300))
    role = db.Column(db.String(20))
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    profile_image = db.Column(db.String(255), nullable=False, default='default_profile.png')
    cart_items = db.relationship('Cart', back_populates='user')
    user_theme = db.Column(db.String(50), default='light')
    is_active = db.Column(db.Boolean, default=False)  # Add this field to track email confirmation
    confirmed = db.Column(db.Boolean, default=False)  # New column for email confirmation
    confirmation_token = db.Column(db.String(100), unique=True)  # New column for token

    def set_theme(self, theme):
        self.user_theme = theme
        db.session.commit()
    
    def get_theme(self):
        return self.user_theme

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def update_location(self, new_location):
        self.country = new_location  # Update country instead of location
        db.session.commit()

        # If the user is a seller, update the Seller's location
        if self.role == 'seller':
            seller = Seller.query.filter_by(user_id=self.id).first()
            if seller:
                seller.location = new_location
                db.session.commit()
    
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')
    
    def confirm_email_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return False
        return User.query.get(data['confirm'])

#password="kcdg qfpj ibed talg"
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    condition = db.Column(db.String(50), nullable=True)
    brand = db.Column(db.String(150), nullable=True)
    gender = db.Column(db.String(150), nullable=True)
    color = db.Column(db.String(150), nullable=True)
    size = db.Column(db.String(150), nullable=True)
    is_package = db.Column(db.Boolean, nullable=False, default=False)
    qr_code = db.Column(db.String(255), nullable=True)

    # Relationships
    seller = db.relationship('Seller', backref='products')
    images = db.relationship('ProductImage', backref='associated_product', lazy=True)
    components = db.relationship('ProductComponent', back_populates='product', lazy=True)
    cart_entries = db.relationship('Cart', back_populates='product', lazy=True)

class Buyer(db.Model):
    __tablename__ = 'buyers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False)    

class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

class ProductVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    video_url = db.Column(db.String(200), nullable=False)

class ProductComponent(db.Model):
    __tablename__ = 'product_component'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    product = db.relationship('Product', back_populates='components')  # Adjusted

class SavedProduct(db.Model):
    __tablename__ = 'saved_products'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    date_saved = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='saved_products')
    product = db.relationship('Product', backref='saved_by_users')

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    component_id = db.Column(db.Integer, db.ForeignKey('product_component.id'))  # Optional link to components
    quantity = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates='cart_items')
    product = db.relationship('Product', back_populates='cart_entries')
    component = db.relationship('ProductComponent', backref='cart_items')

    @property
    def total_price(self):
        product_price = self.product.price
        if self.component:
            # Add component price if available
            product_price += self.component.price
        return product_price * self.quantity

class Seller(db.Model):
    __tablename__ = 'sellers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=True)  # This should be where the location is stored
    
class Theme(db.Model):
    __tablename__ = 'theme'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    css_file = db.Column(db.String(255), nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    buyer = db.relationship('Buyer', backref='orders')
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    product = db.relationship('Product', backref='order_items')
