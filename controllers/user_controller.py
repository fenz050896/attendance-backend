import base64
from uuid import UUID
from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import verify_jwt_in_request, current_user
import tenseal as ts

from models import (
    UserModel,
    UserTensealContextModel,
    UserProfileModel,
    UserRegisteredFacesModel,
    UserEncryptedFaceEmbeddingModel,
)

from schemas.user.user_schema import UserSchema

user_controller = Blueprint('user_controller', __name__, url_prefix='/user')
user_profile_controller = Blueprint('user_profile_controller', __name__, url_prefix='/profile')
user_face_registration_controller = Blueprint('user_face_registration_controller', __name__, url_prefix='/face-registration')
user_face_verification_controller = Blueprint('user_face_verification_controller', __name__, url_prefix='/face-verification')

user_controller.register_blueprint(user_profile_controller)
user_controller.register_blueprint(user_face_registration_controller)
user_controller.register_blueprint(user_face_verification_controller)

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
    
@user_profile_controller.route('/check-saved-context-key', methods=['GET'])
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
    
@user_profile_controller.route('/get-saved-context-key', methods=['GET'])
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
    
@user_face_registration_controller.route('/register-faces', methods=['POST'])
def register_faces():
    try:
        user = current_user
        req_inputs = request.get_json()

        if not isinstance(req_inputs, list):
            return jsonify({
                'error': True,
                'message': 'Input not a list'
            }), 500

        for req_input in req_inputs:
            real_img = base64.b64decode(req_input['real_img'])
            rgb_img = base64.b64decode(req_input['rgb_img'])
            filename = req_input['filename']
            size = req_input['size']
            mime_type = req_input['mime_type']
            encrypted_embedding = base64.b64decode(req_input['encrypted_embedding'])
            detection_score = req_input['detection_score']

            registered_face = UserRegisteredFacesModel.create({
                'user_id': user.id,
                'filename': filename,
                'mime_type': mime_type,
                'size': size,
                'real_content': real_img,
                'rgb_content': rgb_img,
            })

            UserEncryptedFaceEmbeddingModel.create({
                'user_id': user.id,
                'source_file_id': registered_face.id,
                'embedding': encrypted_embedding,
                'detection_score': detection_score,
            })

        UserRegisteredFacesModel.commit()
        UserEncryptedFaceEmbeddingModel.commit()

        return jsonify({
            'error': False,
            'message': 'Faces registered successfully',
            'data': None
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e)
        }), 500
    
@user_face_registration_controller.route('/get-registered-faces', methods=['GET'])
def get_registered_faces():
    try:
        user = current_user
        user_registered_faces = UserRegisteredFacesModel.where(user_id=user.id).all()

        result = []
        for face in user_registered_faces:
            data = {
                'id': face.id,
                'mime_type': face.mime_type,
            }
            result.append(data)

        return jsonify({
            'error': False,
            'message': '',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e)
        }), 500
    
@user_face_registration_controller.route('/registered-face/<string:registered_face_id>', methods=['GET'])
def registered_face_get_content(registered_face_id):
    user = current_user
    user_registered_face = UserRegisteredFacesModel.where(id=registered_face_id, user_id=user.id).first()

    if not user_registered_face:
        return jsonify({
            'error': True,
            'message': 'Picture not found',
            'data': None
        })
    
    return Response(user_registered_face.real_content, mimetype=user_registered_face.mime_type, headers={
        'Content-Length': str(len(user_registered_face.real_content))
    })

@user_face_verification_controller.route('/verify', methods=['POST'])
def verify_face():
    try:
        user = current_user
        req_inputs = request.get_json()
        input_face = base64.b64decode(req_inputs['encrypted_embedding'])
        input_ctx = base64.b64decode(req_inputs['ctx'])

        context = ts.context_from(input_ctx)
        face_embedding = ts.ckks_vector_from(context, input_face)

        user_embeddings = UserEncryptedFaceEmbeddingModel.where(user_id=user.id).all()
        results = []
        for user_embedding in user_embeddings:
            registered_face = ts.ckks_vector_from(context, user_embedding.embedding)
            result = face_embedding.dot(registered_face)
            result = base64.b64encode(result.serialize()).decode()
            results.append(result)

        return jsonify({
            'error': False,
            'message': 'Success',
            'data': results
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e)
        }), 500
