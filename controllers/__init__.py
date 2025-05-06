from .base_controller import base_controller

from .user_controller import user_controller
from .auth_controller import auth_controller

base_controller.register_blueprint(auth_controller)
base_controller.register_blueprint(user_controller)
