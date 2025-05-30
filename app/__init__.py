from flask import Flask
from app.extensions import db, cors
from app.routes.user import user_bp
from app.routes.auth import auth_bp
from app.routes.demand import demand_bp
from app.routes.plan import plan_bp
from app.routes.job import job_bp
from app.routes.resume import resume_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    db.init_app(app)
    cors.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(demand_bp)
    app.register_blueprint(plan_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(resume_bp)
    return app
