from flask import Flask
from app.extensions import db, cors
from app.routes.user import user_bp
from app.routes.auth import auth_bp
from app.routes.demand import demand_bp
from app.routes.plan import plan_bp
from app.routes.job import job_bp
from app.routes.resume import resume_bp
from app.routes.talent import talent_bp
from app.routes.interview import interview_bp
from app.routes.interviewer import interviewer_bp
from app.routes.selection import selection_bp

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
    app.register_blueprint(talent_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(interviewer_bp)
    app.register_blueprint(selection_bp)

    return app
