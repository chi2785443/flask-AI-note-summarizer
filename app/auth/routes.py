from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from ..models import db, User
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      201:
        description: User registered successfully
      400:
        description: Bad request
    """
    data = request.get_json()
    user = User(email=data['email'], password=generate_password_hash(data['password']))
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'Registed'}), 201

@auth.route('/login', methods=['POST'])
def login():
    """
    User login
    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Returns JWT token
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'token': access_token})
    return jsonify({"msg": "Invalid credentials"}), 401