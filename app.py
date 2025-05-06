from dotenv import dotenv_values
from flask import Flask
from flask_cors import CORS
from flask_alembic import Alembic
from alembic import context
from flask_jwt_extended import JWTManager

from database import create_connection_string, db, Base
import models
from controllers import base_controller

env = dotenv_values(".env")

class MyAlembic(Alembic):
    def configure(self, config):
        super().configure(config)
        context.configure(
            connection=self.connection,
            target_metadata=Base.metadata
        )

app = Flask(__name__)
CORS(app, origins=['*'])

app.config["JWT_SECRET_KEY"] = env["JWT_SECRET_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 24 * 60 * 60
app.config['SQLALCHEMY_DATABASE_URI'] = create_connection_string(
    database_name=env["DB_NAME"],
    username=env["DB_USERNAME"],
    password=env["DB_PASSWORD"],
    host=env["DB_HOST"],
    port=int(env["DB_PORT"]),
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

def main():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
