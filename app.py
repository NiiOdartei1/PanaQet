from flask import Flask, send_from_directory, send_file, render_template, redirect, url_for, flash, request, session, abort, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_mail import Mail
from models import User, Cart, Product, ProductComponent, ProductImage, Buyer, Seller
from admin_routes import admin_bp
from seller_routes import seller_bp
from buyer_routes import buyer_bp
from database import db
from routes import routes
import webview
import os
import webbrowser  # Import webbrowser to open in the default browser

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # Set file size limit to 500MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'niiodartei24@gmail.com'
app.config['MAIL_PASSWORD'] = 'feroA5002'

mail = Mail(app)
csrf = CSRFProtect(app)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

# Register blueprints
app.register_blueprint(routes)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(seller_bp, url_prefix='/seller')
app.register_blueprint(buyer_bp, url_prefix='/buyer')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    return product

# Define the folder for saving receipts
RECEIPTS_FOLDER = 'receipts'
if not os.path.exists(RECEIPTS_FOLDER):
    os.makedirs(RECEIPTS_FOLDER)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        session['theme'] = current_user.get_theme()

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response

@app.context_processor
def inject_theme():
    return dict(user_theme=session.get('user_theme', 'light'))

@app.context_processor
def inject_cart_count():
    if current_user.is_authenticated:
        cart_count = Cart.query.filter_by(user_id=current_user.id).count()
    else:
        cart_count = 0
    return {'cart_count': cart_count}


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the SQLite database file and tables

    # Start the Flask application directly without threading
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
