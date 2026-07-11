"""
LaundryBot V7 Enterprise
Application Entry Point
"""

import logging

from flask import Flask, redirect, render_template
from flask_login import LoginManager

from config import Config

from services.auth_service import load_user

from routes import (
    auth_bp,
    dashboard_bp,
    customer_bp,
    machine_bp,
    repair_bp,
    manual_bp,
    part_bp,
    technician_bp,
    documents_bp,
    api_bp,
    ai_bp,
)
from routes.machine_master import machine_master_bp

# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ==========================================================
# Login Manager
# ==========================================================

login_manager = LoginManager()


@login_manager.user_loader
def user_loader(user_id):
    return load_user(user_id)


# ==========================================================
# Register Blueprint
# ==========================================================

def register_blueprints(app):

    app.register_blueprint(auth_bp)

    app.register_blueprint(dashboard_bp)

    app.register_blueprint(customer_bp)

    app.register_blueprint(machine_bp)
    app.register_blueprint(machine_master_bp)

    app.register_blueprint(repair_bp)

    app.register_blueprint(manual_bp)

    app.register_blueprint(part_bp)

    app.register_blueprint(technician_bp)

    app.register_blueprint(documents_bp)

    app.register_blueprint(api_bp)

    app.register_blueprint(ai_bp)


# ==========================================================
# Error Handler
# ==========================================================

def register_error_handlers(app):

    @app.errorhandler(404)
    def page_not_found(error):

        logger.warning("404 : %s", error)

        try:
            return render_template(
                "errors/404.html"
            ), 404

        except Exception:
            return "404 Not Found", 404

    @app.errorhandler(500)
    def internal_error(error):

        logger.exception(error)

        try:
            return render_template(
                "errors/500.html"
            ), 500

        except Exception:
            return "500 Internal Server Error", 500


# ==========================================================
# Create App
# ==========================================================

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)
    print("=" * 60)
    print("APP KEY :", Config.OPENAI_API_KEY)
    print("=" * 60)
    app.secret_key = Config.SECRET_KEY

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    login_manager.session_protection = "strong"

    register_blueprints(app)

    register_error_handlers(app)

    @app.route("/")
    def home():

        return redirect("/dashboard/")

    logger.info(
        "LaundryBot V7 Enterprise Started"
    )

    return app


# ==========================================================
# Application
# ==========================================================

app = create_app()


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    app.run(

        host=Config.HOST,

        port=Config.PORT,

        debug=Config.DEBUG,

    )