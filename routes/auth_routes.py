from flask import Blueprint, request, session
from models import Admin
from extensions import db, bcrypt
from itsdangerous import URLSafeTimedSerializer

auth_bp = Blueprint('auth', __name__)
serializer = URLSafeTimedSerializer("SECRET_KEY")

# Signup
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json

    if not all([data.get('full_name'), data.get('email'), data.get('password'), data.get('confirm_password')]):
        return {"error": "All fields required"}, 400

    if data['password'] != data['confirm_password']:
        return {"error": "Passwords do not match"}, 400

    if len(data['password']) < 8:
        return {"error": "Password must be 8+ characters"}, 400

    if Admin.query.filter_by(email=data['email']).first():
        return {"error": "Account already exists"}, 400

    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    new_admin = Admin(
        full_name=data['full_name'],
        email=data['email'],
        password=hashed_pw
    )

    db.session.add(new_admin)
    db.session.commit()

    return {"message": "Signup successful"}, 201


# Login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    admin = Admin.query.filter_by(email=data['email']).first()

    if not admin or not bcrypt.check_password_hash(admin.password, data['password']):
        return {"error": "Invalid email or password"}, 401

    session['admin_id'] = admin.id

    if data.get("remember"):
        session.permanent = True

    return {"message": "Login successful"}, 200


# Forgot Password
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')

    admin = Admin.query.filter_by(email=email).first()

    if admin:
        token = serializer.dumps(email)
        print(f"Reset link: http://localhost:5000/reset/{token}")

    return {"message": "If email exists, reset link sent"}, 200