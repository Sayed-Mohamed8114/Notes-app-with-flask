from flask import Flask , template_rendered
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db=SQLAlchemy()
DB_name="database.db"

def create_app():
    app=Flask(__name__,template_folder='templates_folder')
    # to make the related cookies in our website , the secret key must be for only you don't gave it to any one
    app.config['SECRET_KEY']= 'sadkasjf sadjakljs asdflasjf'
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_name}'
    db.init_app(app)
        
    # make importion of the routes and the authors 
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    
    from .models import User , Note
    
    create_database(app)
    
    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    db_path = path.join(path.dirname(__file__), DB_name)
    if not path.exists(db_path):
        with app.app_context():
            db.create_all()
        print(f'Created database at {db_path}')


    




