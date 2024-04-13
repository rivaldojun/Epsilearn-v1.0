from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
import stripe
from pymongo import MongoClient
from dotenv import load_dotenv
import gevent
from flask_redis import FlaskRedis
import os
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager=LoginManager()
load_dotenv()

db = SQLAlchemy()
socketio = SocketIO()
migrate=Migrate()
# mongo_client = MongoClient(os.getenv("MONGO_DB"))
# db_no_sql = mongo_client['nosql_db']
redis_store = FlaskRedis()
def create_app(conf=None):
    app=Flask(__name__)
    CORS(app)
    if conf is None:
        conf="Development" 
    app.config.from_object(
        f'App.Configuration.config.Config{conf.capitalize()}'
    )
    stripe.api_key =os.getenv("STRIPE_SECRET_KEY")
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    login_manager.login_view='Main.connexion'
    login_manager.login_message="Vueillez-vous connecter"
    redis_store.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    # app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)  # Seuil d'inactivité de 15 minutes
    # toolbar = DebugToolbarExtension(app)
    # socketio = SocketIO(app, async_mode='gevent'
    from App.Main import MainBp
    app.register_blueprint(MainBp)
    from App.Admin import AdminBp
    app.register_blueprint(AdminBp)
    from App.Cours import CoursBp
    app.register_blueprint(CoursBp)
    from App.Event import EventBp
    app.register_blueprint(EventBp)
    from App.Pomodoro import PomodoroBp
    app.register_blueprint(PomodoroBp) 
    
    with app.app_context():
        db.create_all()
    
    return app

