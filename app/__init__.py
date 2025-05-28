import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_alembic import Alembic
from alembic import context
from flask_jwt_extended import JWTManager
import click
import importlib
import inspect

import app.models as models
from app.database import create_connection_string, db, Base
from app.controllers import base_controller
import app.seeds as seeder

def import_classes_from_directory(package_path, package_name, opt_filename=''):
    classes = []

    for filename in os.listdir(package_path):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            if opt_filename != '' and opt_filename is not None and opt_filename != module_name:
                continue
            full_module_name = f"{package_name}.{module_name}"
            module = importlib.import_module(full_module_name)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ == full_module_name:
                    classes.append(obj)

    return classes

def create_app():
    class MyAlembic(Alembic):
        def configure(self, config):
            super().configure(config)
            context.configure(
                connection=self.connection,
                target_metadata=Base.metadata
            )

    load_dotenv()

    app = Flask(__name__)
    CORS(app, origins=['*'])

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 24 * 60 * 60
    app.config['SQLALCHEMY_DATABASE_URI'] = create_connection_string(
        database_name=os.getenv("DB_NAME"),
        username=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
    )

    jwt = JWTManager(app)
    db.init_app(app)
    alembic = MyAlembic()
    alembic.init_app(app)

    app.register_blueprint(base_controller)

    @jwt.user_identity_loader
    def user_identity_lookup(user_id):
        return user_id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        user = models.UserModel.find(id=identity)
        return user

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.cli.command('seed-run')
    @click.option('--filename')
    def seed_run(filename):
        package_path = os.path.dirname(seeder.__file__)
        classes = import_classes_from_directory(package_path, 'app.seeds', filename)
        class_instances = []
        for cls in classes:
            c = cls()
            class_instances.append({
                'priority': c.priority,
                'cls': c
            })

        class_instances.sort(key=lambda ins: ins['priority'])

        for instance in class_instances:
            if hasattr(instance['cls'], 'run'):
                instance['cls'].run()

    return app