"""Flask application factory and configuration"""
import logging
import os

from flask import Flask

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__,
                static_folder='../frontend',
                template_folder='../frontend')

    # Get default proxy URL from environment variable
    app.config['DEFAULT_PROXY_URL'] = os.environ.get("PROXY_URL")

    # Register blueprints
    from app.routes.api import api_bp
    from app.routes.proxy import proxy_bp
    from app.routes.static import static_bp

    app.register_blueprint(static_bp)
    app.register_blueprint(proxy_bp)
    app.register_blueprint(api_bp)

    logger.info("Flask application created and configured")

    return app
