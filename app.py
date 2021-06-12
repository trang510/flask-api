from flask import Flask
from flasgger import Swagger
from api.route.pool import pool_api


def create_app():
    app = Flask(__name__)

    app.config['SWAGGER'] = {
        'title': 'Flask API',
        'description': 'Welcome to the Swagger UI documentation site'
    }
    swagger = Swagger(app)

    app.register_blueprint(pool_api, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
