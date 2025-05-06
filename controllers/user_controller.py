import base64
from flask import Blueprint, jsonify, request
from flask_jwt_extended import verify_jwt_in_request, current_user

from models import UserModel, UserTensealContextModel, UserProfileModel

from schemas.user.user_schema import UserSchema

user_controller = Blueprint('user_controller', __name__, url_prefix='/user')
user_profile_controller = Blueprint('user_profile_controller', __name__, url_prefix='/profile')

user_controller.register_blueprint(user_profile_controller)

@user_controller.before_request
def before_request():
    try:
        verify_jwt_in_request()
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e)
        }), 401

@user_controller.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello World'})

@user_controller.route('/<string:user_id>', methods=['GET'])
def show(user_id):
    user = UserModel.find(id=user_id)
    if not user:
        return jsonify({
            'error': True,
            'message': 'User not found'
        }), 404
    user = user.to_dict()
    return jsonify({
        'error': False,
        'message': 'User found',
        'data': {
            'user': user,
        }
    })

@user_controller.route('/', methods=['POST'])
def store():
    pass

@user_controller.route('/', methods=['DELETE'])
def delete():
    pass

@user_profile_controller.route('/update/<string:user_id>', methods=['PUT'])
def update(user_id):
    try:
        user_profile = UserProfileModel.where(user_id=user_id).first()
        if not user_profile:
            return jsonify({
                'error': True,
                'message': 'User profile not found'
            }), 404

        data = request.get_json()

        validate = UserProfileModel.validate(data, 'update')
        if isinstance(validate, tuple):
            return jsonify({
                'error': True,
                'message': validate[0]
            }), validate[1]
        
        data = validate.model_dump()
        user_profile.address = data['address']
        user_profile.phone_number = data['phone_number']
        user_profile.birthdate = data['birthdate']
        user_profile.commit()

        if 'full_name' in data:
            user = UserModel.find(id=user_id)
            if not user:
                return jsonify({
                    'error': True,
                    'message': 'User not found'
                }), 404
            user.full_name = data['full_name']
            user.commit()

        return jsonify({
            'error': False,
            'message': 'User profile updated successfully',
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e)
        }), 500
    
@user_profile_controller.route('/save-context-key', methods=['POST'])
def save_context_key():
    try:
        user = current_user

        req_input = request.get_json()

        saved_context = UserTensealContextModel.where(user_id=user.id).first()
        context = base64.b64decode(req_input['context'])
        if saved_context:
            saved_context.context = context
            saved_context.commit()
        else:
            saved_context = UserTensealContextModel.create({
                'user_id': user.id,
                'context': context
            })
            saved_context.commit()

        return jsonify({
            'error': False,
            'message': 'Context key updated successfully',
            'data': None
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e)
        }), 500
    
@user_profile_controller.route('check-saved-context-key', methods=['GET'])
def check_saved_context_key():
    try:
        user = current_user

        saved_context = UserTensealContextModel.where(user_id=user.id).first()
        if not saved_context:
            return jsonify({
                'error': True,
                'message': 'No context key found',
                'data': None
            }), 404

        return jsonify({
            'error': False,
            'message': 'Context key found',
            'data': {
                'exists': True
            }
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e)
        }), 500
    
@user_profile_controller.route('get-saved-context-key', methods=['GET'])
def get_saved_context_key():
    try:
        user = current_user

        saved_context = UserTensealContextModel.where(user_id=user.id).first()
        if not saved_context:
            return jsonify({
                'error': True,
                'message': 'No context key found',
                'data': None
            }), 404
        
        data = {
            'context': base64.b64encode(saved_context.context).decode(),
            'created_at': saved_context.created_at,
            'updated_at': saved_context.updated_at,
        }

        return jsonify({
            'error': False,
            'message': 'Context key found',
            'data': data
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e)
        }), 500
