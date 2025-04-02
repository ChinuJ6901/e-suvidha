from flask import Flask, send_from_directory
from app.main_routes import main_bp
from app.user_routes import user_bp
from app.provider_routes import provider_bp
from app.admin_routes import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(provider_bp, url_prefix='/provider')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @app.route("/data.xml")
    def get_data_xml():
        return send_from_directory("../", "data.xml")

    return app
