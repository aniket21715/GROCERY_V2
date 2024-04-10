from datetime import datetime, timedelta
from flask import Flask
from flask import jsonify, request, send_from_directory 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_login import LoginManager, UserMixin, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, create_access_token, current_user, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import declarative_base
from werkzeug.utils import secure_filename
from flask_caching import Cache
import os
from celery.schedules import crontab
from workers import make_celery, cache
from flask import send_file
import pandas as pd
from flask_mail import Mail, Message



engine = None
Base = declarative_base()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': 'http://localhost:8080'}})
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'thisisasecretkey'
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secret key of your choice

    #########################EMAIL#################################################
    app.config['MAIL_SERVER'] = "smtp.gmail.com"
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = "aniketagrawal715@gmail.com"
    app.config['MAIL_PASSWORD'] = "bynmywrktujpeyet"
    app.config['MAIL_DEFAULT_SENDER'] = "aniketagrawal715@gmail.com"



    db.init_app(app)
    JWTManager(app)
    app.app_context().push()
    return app

app = create_app()

user1 = {"username":"sandeep", "email":["anikettag2001@gmail.com"]}
mail = Mail(app)
celery = make_celery(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
# Define the User model and other necessary models here...

cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379/0'})

########################################################################################################3
@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(crontab(hour=20, minute=38), visit_reminder.s())
    sender.add_periodic_task(
        crontab( hour=20, minute=45),
        generate_monthly_activity_report.s()
    )


@celery.task()
def visit_reminder():
   # today = datetime.utcnow().date()
    users_to_remind = User.query.all()

#filter(User.bookings.any(Booking.booking_date <= today)).
    for user in users_to_remind:
        send_reminder(user)

    return f"Sent {len(users_to_remind)} reminders"
    
def send_reminder(user):
    with mail.connect() as conn:
        msg = Message(
            subject="Visit and buy  Reminder - grocery",
            recipients=[user.email],
            sender="aniketagrawal715@gmail.com"  # Replace with your sender email
        )
        msg.body = f"Hello {user.username},\n\nDon't forget to visit and buy some grocery today!\n\nRegards,\n Grocery app teams"
        conn.send(msg)

@celery.task(name='app.send_monthly_activity_report')
def generate_monthly_activity_report():
    with app.app_context():
        print("Monthly Activity Report Task started")

        current_date = datetime.utcnow()
        first_day_of_month = current_date.replace(day=1)

        user = User.query.all()
        

        for user in user:
            user_id= user.id
            recipients=[user.email]
            purchase_history = Purchase.query.filter_by(user_id=user_id)\
                .filter(Purchase.purchase_date >= first_day_of_month).all()

            # Calculate total expenditure and orders made by each user
            if purchase_history:
                subject = 'Monthly Activity Report'
                recipients = user.email
                html_body = f'<h2>{subject}</h2>'
                html_body += '<table border="1">'
                html_body += '<tr><th>Email</th><th>Product Name</th><th>Quantity</th><th>Price</th><th>Total</th></tr>'
            user_orders = {}
            total_expenditure = 0

            for purchase in purchase_history:
                user_id = purchase.user_id
                #username = User.query.get(user_id).username
                product_name = purchase.product.name
                price = purchase.product.price
                quantity = purchase.quantity
                expenditure = purchase.product.price * quantity
                
                total_expenditure += expenditure

                if user_id not in user_orders:
                    user_orders[user_id] = {
                        #'username': username,
                        'orders': [],
                        'total_expenditure': 0
                    }

                user_orders[user_id]['orders'].append({
                    'product_name': product_name,
                    'quantity': quantity,
                    'expenditure': expenditure
                })

                user_orders[user_id]['total_expenditure'] += expenditure
                html_body += (
                    f'<tr><td>{recipients}</td>'
                    f'<td>{purchase.product.name}</td>'
                    f'<td>{quantity}</td>'
                    f'<td>${price:.2f}</td>'
                    f'<td>${expenditure:.2f}</td></tr>'
                )

                html_body += '</table>'
                html_body += f'<p>Total Expenditure: ${total_expenditure:.2f}</p>'

                msg = Message(subject, sender="aniketagrawal715@gmail.com", recipients=[user.email])
                msg.html = html_body
                mail.send(msg)

                print(f"Monthly Activity Report email sent to {recipients}")

        print("Monthly Activity Report Task completed")


###################################################################################################



UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

class RegistrationForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    email = StringField('Email')
    submit = SubmitField('Register')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(10), default='user') 

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    # Define the relationship with the User model
    user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))

    @property
    def username(self):
        # Access the username from the associated User object
        return self.user.username if self.user else None

class StoreManager(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(10), default='pending')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

class CategoryRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_manager_id = db.Column(db.Integer, db.ForeignKey('store_manager.id'), nullable=False)
    category_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.String(10), default='pending')
    store_manager = db.relationship('StoreManager', backref='category_requests')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    price = db.Column(db.Integer, default=0)
    image = db.Column(db.String, nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    product = db.relationship('Product', backref='cart', lazy=True)
    user = db.relationship('User', backref='cart', lazy=True)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='purchases', lazy=True)
    product = db.relationship('Product', backref='purchases', lazy=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('store_manager.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, default=1)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False) 
    sender = db.relationship('StoreManager', foreign_keys=[sender_id], backref='sent_messages', lazy='joined')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages', lazy='joined')
    
       
login_manager = LoginManager(app)
login_manager.login_view = "login"
@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))
 #   if user:
  #      return user
   # else:
   #     return Admin.query.get(int(user_id))

@app.route('/')
def homepage():
    # Handle logic for the homepage API endpoint
    # Return data as needed

    return jsonify({'message': 'Welcome to the homepage!'})


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()


        if user and check_password_hash(user.password, password):
            # Create an access token
            access_token = create_access_token(identity={'id': user.id, 'name': user.username, 'type': user.type})
            return jsonify(access_token=access_token, user={'id': user.id, 'name': user.username, 'type': user.type}, message='Login successful'), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/get-user-details', methods=['GET'])
@jwt_required()
def get_user_details():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    return jsonify(user={'id': user.id, 'username': user.username, 'email': user.email})

@app.route('/edit-user-details', methods=['POST'])
@jwt_required()
def edit_user_details():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])

    data = request.json
    user.username = data.get('username') or user.username
    user.email = data.get('email') or user.email
    if data.get('password'):
        user.password = generate_password_hash(data['password'], method='sha256')

    db.session.commit()

    return jsonify({'message': 'User details updated successfully'}), 200

@app.route('/submit-feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    try:
        user_id = get_jwt_identity().get('id')
        content = request.json.get('content')

        new_feedback = Feedback(user_id=user_id, content=content)
        db.session.add(new_feedback)
        db.session.commit()

        return jsonify({'message': 'Feedback submitted successfully'}), 200
    except Exception as e:
        print('Error submitting feedback:', e)
        return jsonify({'error': 'An error occurred while submitting feedback'}), 500

@app.route('/get-feedback', methods=['GET'])
def get_feedback():
    try:
        feedback_list = Feedback.query.all()
        feedback_data = [
            {
                'id': feedback.id,
                'user_id': feedback.user_id,
                'content': feedback.content,
                'date_submitted': feedback.date_submitted.isoformat(),
            }
            for feedback in feedback_list
        ]

        return jsonify({'feedback_list': feedback_data}), 200
    except Exception as e:
        print('Error fetching feedback:', e)
        return jsonify({'error': 'An error occurred while fetching feedback'}), 500
     
def create_first_user():
    # Check if an admin user already exists
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin',email='admin@gmail.com', password=generate_password_hash('adminpassword'),type="admin")
        db.session.add(admin)
        db.session.commit()
        print('Admin user created successfully')
    else:
        print('Admin user already exists')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.json
            username = data.get('username')
            email=data.get('email')
            password = data.get('password')

            if User.query.filter_by(username=username).first():
                return jsonify({'message': 'Username already exists'}), 400

            new_user = User(username=username,email=email, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()

            # Create an access token for the new user
            access_token = create_access_token(identity=new_user.id)

            return jsonify(access_token=access_token, message='Registration successful'), 201

        except Exception as e:
            print(f"Error during registration: {str(e)}")
            return jsonify({'message': 'Internal Server Error'}), 500
        

@app.route('/register/store-manager', methods=['POST'])
def register_store_manager():
    if request.method == 'POST':
        try:
            data = request.json
            username = data.get('username')
            password = data.get('password')

            if StoreManager.query.filter_by(username=username).first():
                return jsonify({'message': 'Username already exists'}), 400

            new_store_manager = StoreManager(username=username, password=generate_password_hash(password))
            db.session.add(new_store_manager)
            db.session.commit()          
            return jsonify(message='Registration request sent for approval'), 201
    
        
        except Exception as e:
            print(f"Error during store manager registration: {str(e)}")
            return jsonify({'message': 'Internal Server Error'}), 500
        
@app.route('/store-manager/login', methods=['POST'])
def store_manager_login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')

        store_manager = StoreManager.query.filter_by(username=username).first()

        if not store_manager:
            return jsonify(error='Invalid data'), 400  # 400 Bad Request
        if store_manager.status != 'approved':
            return jsonify(error='Request for approval is pending'), 403  # 403 Forbidden

        if store_manager and check_password_hash(store_manager.password, password):
            # Create an access token for the approved store manager
            access_token = create_access_token(identity={"id": store_manager.id, "name": store_manager.username, "status": store_manager.status})
            return jsonify(access_token=access_token, status=store_manager.status, message='Store Manager login successful'), 200
        else:
            return jsonify(message='Invalid credentials or store manager not approved'), 401

# Assume you have a decorator for verifying JWT tokens, you can adjust it based on your implementation
def store_manager_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if identity.get('status') != 'approved':
            return jsonify(error='Store manager not approved'), 403  # 403 Forbidden
        return fn(*args, **kwargs)
    return wrapper

# Logout route
@app.route('/store-manager/logout', methods=['POST'])
@store_manager_required
def store_manager_logout():
    # You can perform any additional cleanup or logging out logic here
    return jsonify(message='Store Manager logout successful'), 200

        
@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    # Fetch all pending store manager registration requests
    pending_requests = StoreManager.query.filter_by(status='pending').all()

    # Convert the requests to a format suitable for frontend display
    requests_data = [
        {'id': request.id, 'username': request.username, 'status': request.status}
        for request in pending_requests
    ]

    return jsonify({'pendingRequests': requests_data}), 200

@app.route('/admin/approve-store-manager/<int:request_id>', methods=['PUT'])
def approve_store_manager(request_id):
    # Update the status of the store manager registration request to 'approved'
    request = StoreManager.query.get(request_id)
    if request:
        request.status = 'approved'
        db.session.commit()
        return jsonify({'message': 'Store manager registration approved'}), 200
    else:
        return jsonify({'message': 'Request not found'}), 404

@app.route('/admin/reject-store-manager/<int:request_id>', methods=['PUT'])
def reject_store_manager(request_id):
    # Update the status of the store manager registration request to 'rejected'
    request = StoreManager.query.get(request_id)
    if request:
        request.status = 'rejected'
        db.session.commit()
        return jsonify({'message': 'Store manager registration rejected'}), 200
    else:
        return jsonify({'message': 'Request not found'}), 404



@app.route('/admin/all-requests', methods=['GET'])
def all_requests():
    # Fetch all store manager registration requests
    all_requests = StoreManager.query.all()

    # Convert the requests to a format suitable for frontend display
    requests_data = [
        {'id': request.id, 'username': request.username, 'status': request.status}
        for request in all_requests
    ]

    return jsonify({'allRequests': requests_data}), 200

@app.route('/store-manager/dashboard', methods=['GET'])
@login_required
def store_manager_dashboard():
    # Access current user using current_user variable
    return jsonify({'message': f'Welcome {current_user.username} to Store Manager Dashboard!'})
@app.route('/store-manager/request-category', methods=['POST'])
@jwt_required()
def request_category():
    try:
        current_user_id = get_jwt_identity()

        data = request.get_json()
        category_name = data.get('category_name')
        description = data.get('description')

        # Create a new category request
        new_request = CategoryRequest(
            store_manager_id=current_user_id.get('id'),
            category_name=category_name,
            description=description,
        )
        db.session.add(new_request)
        db.session.commit()

        return jsonify({'message': 'Category request sent successfully'}), 200
    except Exception as e:
        print(f"Error in request_category: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


# Add these routes for admin to approve or reject category requests

@app.route('/admin/category-requests', methods=['GET'])
def get_category_requests():
    category_requests = CategoryRequest.query.all()
    requests_data = [
        {
            'id': request.id,
            'store_manager_username': request.store_manager.username,  # Access through relationship
            'category_name': request.category_name,
            'description': request.description,
            'status': request.status
        }
        for request in category_requests
    ]
    return jsonify({'categoryRequests': requests_data}), 200

@app.route('/admin/approve-category-request/<int:request_id>', methods=['PUT'])
def approve_category_request(request_id):
    request = CategoryRequest.query.get(request_id)
    if request:
        request.status = 'approved'
        # Create a new category with the requested name
        new_category = Category(name=request.category_name, description=request.description)
        db.session.add(new_category)
        db.session.commit()
        return jsonify({'message': 'Category request approved and category added'}), 200
    else:
        return jsonify({'message': 'Category request not found'}), 404

@app.route('/admin/reject-category-request/<int:request_id>', methods=['PUT'])
def reject_category_request(request_id):
    request = CategoryRequest.query.get(request_id)
    if request:
        request.status = 'rejected'
        db.session.commit()
        return jsonify({'message': 'Category request rejected'}), 200
    else:
        return jsonify({'message': 'Category request not found'}), 404


@app.route('/add-category', methods=['POST'])
def add_category():
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        description = data.get('description')

        new_category = Category(name=name, description=description)
        db.session.add(new_category)
        db.session.commit()

        return jsonify({'message': 'Category added successfully'}), 201


# Edit category
@app.route('/edit-category/<int:category_id>', methods=['PUT'])
def edit_category(category_id):
    data = request.json
    new_name = data.get('name')
    new_description = data.get('description')

    category = Category.query.get(category_id)
    if category:
        category.name = new_name
        category.description = new_description
        db.session.commit()
        return jsonify({'message': 'Category updated successfully'})
    else:
        return jsonify({'message': 'Category not found'}), 404

# Delete category
@app.route('/delete-category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'})
    else:
        return jsonify({'message': 'Category not found'}), 404


@app.route('/add-product', methods=['POST'])
def add_product():
    try:
        name = request.form['name']
        description = request.form['description']
        stock = int(request.form['stock'])
        price = float(request.form['price'])
        category_id = int(request.form['category_id'])

        # Validate and save the image
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '' and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                return jsonify({'error': 'Invalid file type for image'}), 400
        else:
            filename = None

        # Add the product to the database
        new_product = Product(
            name=name,
            description=description,
            stock=stock,
            price=price,
            category_id=category_id,
            image=filename
        )
        db.session.add(new_product)
        db.session.commit()

        return jsonify({'message': 'Product added successfully'}), 200

    except Exception as e:
        print('Error adding product:', e)  # Log the specific exception
        return jsonify({'error': 'An error occurred while adding the product'}), 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/get-products', methods=['GET'])
@cache.cached(timeout=20)
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        
        product_data={
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'stock': product.stock,
            'price': product.price,
            
            'image': f'uploads/{product.image}' if product.image else None,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
        }
        product_list.append(product_data)
        
    
    return jsonify({'products': product_list})

@app.route('/get-categories', methods=['GET'])
@cache.cached(timeout=20)
def get_categories():
    categories = Category.query.all()
    category_list = [{'id': category.id, 'name': category.name ,'description':category.description} for category in categories]
    return jsonify({'categories': category_list})


@app.route('/edit-product/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error':'product not found'}), 404
        
        name = request.form.get('name')
        if name: 
            product.name = name

        description = request.form.get('description')
        if description: 
            product.description = description

        stock = request.form.get('stock')
        if stock: 
            product.stock = stock

        price = request.form.get('price')
        if price: 
            product.price = price
        
        category_id = request.form.get('category_id')
        if category_id:
            category = Category.query.get(category_id)
            if category:
                product.category = category

        if 'image' in request.files:
            image = request.files['image']
            if image:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                product.image = filename

        db.session.commit()
        
        # Return a success response
        return jsonify({'message': 'Product updated successfully'})
    
    except Exception as e:
        print('Error updating product:', e)  
        # Log the specific exception
        return jsonify({'error': 'An error occurred while updating the product'}), 500

@app.route('/delete-product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    # Retrieve product from the database by ID
    product = Product.query.get_or_404(product_id)

    # Delete the product from the database
    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'Product deleted successfully'})

@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
@jwt_required()
def add_to_cart(product_id):
    try:
        user_id = get_jwt_identity().get('id')

        # Check if the product is already in the user's cart
        existing_cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

        quantity = request.json.get('quantity', 1)

        print(f"Product ID: {product_id}, User ID: {user_id}, Quantity: {quantity}")

        if existing_cart_item:
            # If the product is already in the cart, update the quantity
            existing_cart_item.quantity += quantity
        else:
            # If the product is not in the cart, add it
            new_cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
            db.session.add(new_cart_item)

        db.session.commit()

        return jsonify({'message': 'Product added to cart successfully'}), 200
    except Exception as e:
        print('Error adding to cart:', e)
        return jsonify({'error': 'An error occurred while adding to cart'}), 500


@app.route('/get-cart', methods=['GET'])
@jwt_required()
def get_cart():
    try:
        user_id = get_jwt_identity().get('id')

        # Retrieve the user's cart from the database
        user_cart = Cart.query.filter_by(user_id=user_id).all()

        # Convert the cart data to a format suitable for frontend display
        cart_data = [
    {
        'product': {
            'id': cart_item.product.id,
            'name': cart_item.product.name,
            'description': cart_item.product.description,
            'price': cart_item.product.price,
            'category': {
                'name': cart_item.product.category.name
            },
            'image': cart_item.product.image,
            'stock': cart_item.product.stock,
            # Add other product fields as needed
        },
        'quantity': cart_item.quantity,
    }
            for cart_item in user_cart
        ]

        return jsonify({'cart': cart_data}), 200

    except Exception as e:
        print('Error fetching cart:', e)
        return jsonify({'error': 'An error occurred while fetching the cart'}), 500
    
@app.route('/remove-from-cart/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(product_id):
    try:
        user_id = get_jwt_identity().get('id')

        # Find and delete the item from the user's cart
        cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()

            return jsonify({'message': 'Product removed from cart successfully'}), 200
        else:
            print(f'Product with ID {product_id} not found in the cart.')
            return jsonify({'error': 'Product not found in cart'}), 404

    except Exception as e:
        print('Error removing from cart:', e)
        return jsonify({'error': 'An error occurred while removing from cart'}), 500

# Import necessary modules
@app.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    try:
        user_id = get_jwt_identity().get('id')
        cart_data = request.json.get('cart', [])

        # Iterate over each item in the cart
        for cart_item in cart_data:
            product_id = cart_item['product']['id']
            quantity = cart_item['quantity']

            # Retrieve the product
            product = Product.query.get(product_id)

            # Check if the product and sufficient stock are available
            if product and product.stock >= quantity:
                # Update product stock
                product.stock -= quantity

                # Create a purchase record
                purchase = Purchase(user_id=user_id, product_id=product_id, quantity=quantity)
                db.session.add(purchase)

                # Commit changes to the database
                db.session.commit()
            else:
                # If there is insufficient stock, return an error response
                return jsonify({'error': f'Insufficient stock for product with ID {product_id}'}), 400

        # Clear the user's cart after successful checkout
        Cart.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        return jsonify({'message': 'Checkout successful'}), 200

    except Exception as e:
        print('Error during checkout:', e)
        return jsonify({'error': 'An error occurred during checkout'}), 500

@app.route('/purchase-history', methods=['GET'])
@jwt_required()
def purchase_history():
    try:
        user_id = get_jwt_identity().get('id')

        # Retrieve the user's purchase history from the database
        user_purchases = Purchase.query.filter_by(user_id=user_id).all()

        # Convert the purchase data to a format suitable for frontend display
        purchase_data = [
            {
                'product': {
                    'id': purchase.product.id,
                    'name': purchase.product.name,
                    'description': purchase.product.description,
                    'price': purchase.product.price,
                    'category': {
                        'name': purchase.product.category.name
                    },
                    'image': purchase.product.image,
                    'stock': purchase.product.stock,
                    # Add other product fields as needed
                },
                'quantity': purchase.quantity,
                'purchase_date': purchase.purchase_date.isoformat(),
            }
            for purchase in user_purchases
        ]

        return jsonify({'purchase_history': purchase_data}), 200

    except Exception as e:
        print('Error fetching purchase history:', e)
        return jsonify({'error': 'An error occurred while fetching the purchase history'}), 500

from sqlalchemy import func

@app.route('/export-products-csv', methods=['GET'])
def export_products_csv():
    # Fetch necessary data from the database (products, sales, etc.)
    products = Product.query.all()

    # Create a DataFrame with the product data
    product_data = {
        'Name': [],
        'Stock': [],
        'Description': [],
        'Price': [],
        'Units Sold': [],
        'Remaining Quantity': [],
    }

    for product in products:
        product_data['Name'].append(product.name)
        product_data['Stock'].append(product.stock)
        product_data['Description'].append(product.description)
        product_data['Price'].append(product.price)

        # Calculate units sold using func.sum
        units_sold = Purchase.query.with_entities(func.sum(Purchase.quantity)).filter_by(product_id=product.id).scalar() or 0
        remaining_quantity = product.stock - units_sold

        product_data['Units Sold'].append(units_sold)
        product_data['Remaining Quantity'].append(remaining_quantity)

    df = pd.DataFrame(product_data)

    # Save DataFrame to a CSV file
    csv_filename = 'product_details.csv'
    df.to_csv(csv_filename, index=False)

    # Send the CSV file as a response
    return send_file(csv_filename, as_attachment=True)


@app.route('/send-message', methods=['POST'])
@jwt_required()
def send_message():
    try:
        sender_id = get_jwt_identity().get('id')
        recipient_id = 1
        content = request.json.get('content')

        new_message = Message(sender_id=sender_id, recipient_id=recipient_id, content=content)
        db.session.add(new_message)
        db.session.commit()

        return jsonify({'message': 'Message sent successfully'}), 200
    except Exception as e:
        print('Error sending message:', e)
        return jsonify({'error': 'An error occurred while sending the message'}), 500

@app.route('/get-messages', methods=['GET'])
@jwt_required()
def get_messages():
    try:
        recipient_id = get_jwt_identity().get('id')

        messages = Message.query.filter_by(read=False).all()

        message_data = [
            {
                'id': message.id,
                'sender': {
                    'id': message.sender.id,
                    'username': message.sender.username,
                },
                'content': message.content,
                'timestamp': message.timestamp,
            }
            for message in messages
        ]

        return jsonify({'messages': message_data}), 200
    except Exception as e:
        print('Error fetching messages:', e)
        return jsonify({'error': 'An error occurred while fetching messages'}), 500


@app.route('/mark-as-read/<int:message_id>', methods=['PUT'])
@cross_origin()
def mark_as_read(message_id):
    try:
        # Fetch the message from the database
        message = Message.query.get(message_id)

        if message:
            # Update the message as read
            message.read = True

            # Commit the changes to the database
            db.session.commit()

            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Message not found'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    db.create_all()
    create_first_user()
    app.run(debug=True, port=5000)
