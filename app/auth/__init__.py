from .routes import auth_bp

def init_auth(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
