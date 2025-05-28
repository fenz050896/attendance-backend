from flask import Blueprint, jsonify, request
from argon2 import PasswordHasher
from flask_jwt_extended import create_access_token, jwt_required

from app.models.user_model import UserModel
from app.models.user_profile_model import UserProfileModel
from app.schemas.user.user_schema import UserSchema

auth_controller = Blueprint('auth_controller', __name__, url_prefix='/auth')

@auth_controller.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    validate = UserModel.validate(data, 'register')
    if isinstance(validate, tuple):
        return jsonify({
            'error': True,
            'message': validate[0]
        }), validate[1]
    
    try:
        data = validate.model_dump()
        ph = PasswordHasher()

        password = ph.hash(data['password'])
        user_model = UserModel.create({
            'email': data['email'],
            'full_name': data['full_name'],
            'password': password
        })
        UserProfileModel.create({ 'user_id': user_model.id })
        user_model.commit()

        user = UserSchema.model_validate(user_model).model_dump()

        return jsonify({
            'error': False,
            'message': 'User created successfully',
            'data': user
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e)
        }), 500

@auth_controller.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    validate = UserModel.validate(data, 'login')
    if isinstance(validate, tuple):
        return jsonify({
            'error': True,
            'message': validate[0]
        }), validate[1]
    
    
    try:
        request_input = validate.model_dump()
        email = request_input['email']
        password = request_input['password']
        ph = PasswordHasher()
        
        user = UserModel.where(UserModel.email == email).first()

        if user is None:
            return jsonify({
                'error': True,
                'message': 'Pengguna tidak ditemukan'
            }), 404
        
        if not ph.verify(user.password, password):
            return jsonify({
                'error': True,
                'message': 'Password yang Anda masukkan salah'
            }), 401
        
        if ph.check_needs_rehash(user.password):
            user.password = ph.hash(password)
            user.commit()
        
        access_token = create_access_token(identity=f"{user.id}")
        user = UserSchema.model_validate(user).model_dump()

        return jsonify({
            'error': False,
            'data': {
                'access_token': access_token,
                'user': user,
            }
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e)
        }), 500

@auth_controller.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({
        'error': False,
        'message': 'Berhasil keluar'
    })
