from flask import Flask, jsonify, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_login import LoginManager, UserMixin, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, current_user, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import declarative_base

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
    db.init_app(app)
    JWTManager(app)
    app.app_context().push()
    return app

app = create_app()
login_manager = LoginManager(app)
login_manager.login_view = "login"
# Define the User model and other necessary models here...


class RegistrationForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Register')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(10), default='user') 

class StoreManager(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(10), default='pending')

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

# Logout route
@app.route('/user/logout', methods=['POST'])
@jwt_required()
def user_logout():
    # You can perform any additional cleanup or logging out logic here
    identity = get_jwt_identity()
    user_id = identity.get('id')
    return jsonify(message=f'User {user_id} logout successful'), 200
       
def create_first_user():
    # Check if an admin user already exists
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password=generate_password_hash('adminpassword'),type="admin")
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
            password = data.get('password')

            if User.query.filter_by(username=username).first():
                return jsonify({'message': 'Username already exists'}), 400

            new_user = User(username=username, password=generate_password_hash(password))
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

if __name__ == '__main__':
    db.create_all()
    create_first_user()
    app.run(debug=True, port=5000)
