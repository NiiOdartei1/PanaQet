from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, FileField, TextAreaField, DecimalField, FloatField, FormField, IntegerField, FieldList, SelectMultipleField, ValidationError
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, NumberRange
from models import User
import re


class SettingsForm(FlaskForm):
    theme = SelectField('Select Theme', choices=[
        ('default', 'Default'),
        ('dark', 'Dark'),
        ('light', 'Light'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('red', 'Red')
    ], validators=[DataRequired()])
    submit = SubmitField('Save Changes')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = DecimalField('Price', places=2, validators=[DataRequired()])
    category = SelectField('Category', choices=[('Electronics', 'Electronics'), 
                                                    ('Fashion', 'Fashion'), 
                                                    ('Vehicle', 'Vehicle'), 
                                                    ('Food', 'Food'), 
                                                    ('Others', 'Others')], 
                            validators=[DataRequired()])
        
    # New Fields to match the product model
    location = StringField('Location', validators=[Optional()])
    condition = SelectField('Condition', choices=[('New', 'New'), ('Used', 'Used')], default='New')  # Product condition
    brand = StringField('Brand')  # Product brand
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Unisex', 'Unisex')], default='Unisex')  # Gender category
    type = StringField('Type')  # Product type (e.g., T-shirt, Shoes)
    color = StringField('Color')  # Color of the product
    size = StringField('Size')  # Size of the product (e.g., M, L, XL)
    # Package fields
    is_package = BooleanField('Is this a package?')
    package_options = SelectMultipleField('Package Options', choices=[('option1', 'Option 1'), ('option2', 'Option 2')])
    # Image upload field
    images = FileField('Product Images', validators=[DataRequired()])
    # Submit button
    submit = SubmitField('Add Product')

class ComponentForm(FlaskForm):
    name = StringField('Component Name', validators=[DataRequired()])
    price = FloatField('Component Price', validators=[DataRequired()])
    image = FileField('Component Image', validators=[Optional(), FileAllowed(['jpg', 'png'])])  # Optional image for each component
    submit = SubmitField('Add Component')

from wtforms import SelectField

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    # Updated country code field with all African countries
    country_code = SelectField('Country Code', choices=[
        ('+213', 'Algeria (+213)'),
        ('+244', 'Angola (+244)'),
        ('+229', 'Benin (+229)'),
        ('+267', 'Botswana (+267)'),
        ('+226', 'Burkina Faso (+226)'),
        ('+257', 'Burundi (+257)'),
        ('+238', 'Cabo Verde (+238)'),
        ('+237', 'Cameroon (+237)'),
        ('+236', 'Central African Republic (+236)'),
        ('+235', 'Chad (+235)'),
        ('+269', 'Comoros (+269)'),
        ('+242', 'Congo (+242)'),
        ('+243', 'Democratic Republic of the Congo (+243)'),
        ('+253', 'Djibouti (+253)'),
        ('+20', 'Egypt (+20)'),
        ('+240', 'Equatorial Guinea (+240)'),
        ('+291', 'Eritrea (+291)'),
        ('+268', 'Eswatini (+268)'),
        ('+251', 'Ethiopia (+251)'),
        ('+241', 'Gabon (+241)'),
        ('+220', 'Gambia (+220)'),
        ('+233', 'Ghana (+233)'),
        ('+224', 'Guinea (+224)'),
        ('+245', 'Guinea-Bissau (+245)'),
        ('+225', 'Ivory Coast (+225)'),
        ('+254', 'Kenya (+254)'),
        ('+266', 'Lesotho (+266)'),
        ('+231', 'Liberia (+231)'),
        ('+218', 'Libya (+218)'),
        ('+261', 'Madagascar (+261)'),
        ('+265', 'Malawi (+265)'),
        ('+223', 'Mali (+223)'),
        ('+222', 'Mauritania (+222)'),
        ('+230', 'Mauritius (+230)'),
        ('+212', 'Morocco (+212)'),
        ('+258', 'Mozambique (+258)'),
        ('+264', 'Namibia (+264)'),
        ('+227', 'Niger (+227)'),
        ('+234', 'Nigeria (+234)'),
        ('+250', 'Rwanda (+250)'),
        ('+221', 'Senegal (+221)'),
        ('+248', 'Seychelles (+248)'),
        ('+232', 'Sierra Leone (+232)'),
        ('+27', 'South Africa (+27)'),
        ('+249', 'Sudan (+249)'),
        ('+228', 'Togo (+228)'),
        ('+216', 'Tunisia (+216)'),
        ('+256', 'Uganda (+256)'),
        ('+260', 'Zambia (+260)'),
        ('+263', 'Zimbabwe (+263)'),
    ], validators=[DataRequired()])

    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])

    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Password must be at least 6 characters"),
        EqualTo('confirm_password', message='Passwords must match')
    ])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])

    country = SelectField('Country', choices=[
        ('Algeria', 'Algeria'),
        ('Angola', 'Angola'),
        ('Benin', 'Benin'),
        ('Botswana', 'Botswana'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Burundi', 'Burundi'),
        ('Cabo Verde', 'Cabo Verde'),
        ('Cameroon', 'Cameroon'),
        ('Central African Republic', 'Central African Republic'),
        ('Chad', 'Chad'),
        ('Comoros', 'Comoros'),
        ('Congo', 'Congo'),
        ('Democratic Republic of the Congo', 'Democratic Republic of the Congo'),
        ('Djibouti', 'Djibouti'),
        ('Egypt', 'Egypt'),
        ('Equatorial Guinea', 'Equatorial Guinea'),
        ('Eritrea', 'Eritrea'),
        ('Eswatini', 'Eswatini'),
        ('Ethiopia', 'Ethiopia'),
        ('Gabon', 'Gabon'),
        ('Gambia', 'Gambia'),
        ('Ghana', 'Ghana'),
        ('Guinea', 'Guinea'),
        ('Guinea-Bissau', 'Guinea-Bissau'),
        ('Ivory Coast', 'Ivory Coast'),
        ('Kenya', 'Kenya'),
        ('Lesotho', 'Lesotho'),
        ('Liberia', 'Liberia'),
        ('Libya', 'Libya'),
        ('Madagascar', 'Madagascar'),
        ('Malawi', 'Malawi'),
        ('Mali', 'Mali'),
        ('Mauritania', 'Mauritania'),
        ('Mauritius', 'Mauritius'),
        ('Morocco', 'Morocco'),
        ('Mozambique', 'Mozambique'),
        ('Namibia', 'Namibia'),
        ('Niger', 'Niger'),
        ('Nigeria', 'Nigeria'),
        ('Rwanda', 'Rwanda'),
        ('Senegal', 'Senegal'),
        ('Seychelles', 'Seychelles'),
        ('Sierra Leone', 'Sierra Leone'),
        ('South Africa', 'South Africa'),
        ('Sudan', 'Sudan'),
        ('Togo', 'Togo'),
        ('Tunisia', 'Tunisia'),
        ('Uganda', 'Uganda'),
        ('Zambia', 'Zambia'),
        ('Zimbabwe', 'Zimbabwe'),
    ], validators=[DataRequired()])

    role = SelectField('Role', choices=[('buyer', 'Buyer'), ('seller', 'Seller')], validators=[DataRequired()])

    submit = SubmitField('Signup')

    def validate_password(self, field):
        username = self.username.data.lower()
        password = field.data.lower()

        # Condition 1: Password contains username
        if username in password:
            raise ValidationError("Password should not contain the username.")

        # Condition 2: Password contains sequences of numbers like '123', '456', etc.
        if re.search(r'\d{3,}', password):
            raise ValidationError("Password should not contain sequences of numbers (e.g., 123, 456).")

        # Condition 3: Password matches username directly with numbers
        if re.search(fr"{re.escape(username)}\d*", password):
            raise ValidationError("Password should not contain the username followed by numbers.")
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    
class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = DecimalField('Price', places=2, validators=[DataRequired()])
    category = SelectField('Category', choices=[('Clothing', 'Clothing'), ('Electronics', 'Electronics'), ('Vehicle', 'Vehicle'), ('Food', 'Food'), ('Others', 'Others')], validators=[DataRequired()])
    is_package = BooleanField('Is this a package?')
    package_options = SelectMultipleField('Package Options', choices=[], coerce=int)  # Dynamically populate
    images = FileField('Product Images', validators=[FileAllowed(['png', 'jpg', 'jpeg', 'gif'], 'Images only!'), Optional()], render_kw={"multiple": True})
    video = FileField('Product Video', validators=[FileAllowed(['mp4', 'avi', 'mov'], 'Videos only!'), Optional()])
    location = StringField('Location', validators=[DataRequired()])
    condition = SelectField('Condition', choices=[('New', 'New'), ('Used', 'Used')], validators=[DataRequired()])
    brand = StringField('Brand', validators=[Optional()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Unisex', 'Unisex')], validators=[Optional()])
    color = StringField('Color', validators=[Optional()])
    size = StringField('Size', validators=[Optional()])
    submit = SubmitField('Add Product')
    
class AddToCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    delivery_location = StringField('Delivery Location', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Add to Cart')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    country_code = StringField('Country Code', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])  # Confirm this exists
    profile_image = FileField('Profile Image')
    submit = SubmitField('Save Changes')

class CheckoutForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    address = TextAreaField('Shipping Address', validators=[DataRequired()])
    payment = SelectField(
        'Payment Method',
        choices=[
            ('credit_card', 'Credit Card'),
            ('paypal', 'PayPal'),
            ('bank_transfer', 'Bank Transfer'),
            ('cash_on_delivery', 'Cash On Delivery')
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Complete Purchase')