from flask import Blueprint, jsonify
from flask_jwt_extended import verify_jwt_in_request
# from sqlalchemy import or_

from app.models.app_config_model import AppConfigModel

app_config_controller = Blueprint('app_config_controller', __name__, url_prefix='/app-config')

# @app_config_controller.before_request
# def before_request():
#     try:
#         verify_jwt_in_request()
#     except Exception as e:
#         return jsonify({
#             'error': True,
#             'message': str(e)
#         }), 401

@app_config_controller.route('/', methods=['GET'])
def index():
    try:
        # configs = AppConfigModel.where(or_(AppConfigModel.field == 'clock_in', AppConfigModel.field == 'clock_out')).all(serialize=True)
        configs = AppConfigModel.all(serialize=True)

        return jsonify({
            'error': False,
            'message': 'Success',
            'data': configs,
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e),
        })

@app_config_controller.route('/<int:config_id>', methods=['GET'])
def show(config_id):
    try:
        configs = AppConfigModel.find(config_id)

        return jsonify({
            'error': False,
            'message': 'Success',
            'data': configs,
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': str(e),
        })

@app_config_controller.route('/', methods=['POST'])
def store():
    pass

@app_config_controller.route('/', methods=['PUT'])
def update():
    pass

@app_config_controller.route('/', methods=['DELETE'])
def delete():
    pass
