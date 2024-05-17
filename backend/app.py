from flask import Flask, Blueprint
from flask_migrate import Migrate
from flask_cors import CORS
from src.models import db
from settings import DEBUG, DB_CONFIG
from src.apis import root_blueprint, user_blueprint, organization_blueprint, requirement_blueprint


## App Config ##
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

CORS(app) # Enable CORS
db.init_app(app) # Initialize db
migrate = Migrate(app, db) # Perform migrations

## Blueprints ##
api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')
api_v1.register_blueprint(root_blueprint)
api_v1.register_blueprint(user_blueprint)
api_v1.register_blueprint(organization_blueprint)
api_v1.register_blueprint(requirement_blueprint)

## Register Blueprints ##
app.register_blueprint(api_v1)


if __name__ == '__main__':
    app.run(debug=DEBUG)