from flask import Flask, render_template, request, redirect, url_for, flash
import youtube_dl
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, UserMixin, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'OurProject'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, History

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    class MyModelView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated:
                if current_user.role == 'Admin':
                    return True
            else:
                False

        def inaccessible_callback(self, name, **kwargs):
            flash("Don't Have Permission", category='error')
            return redirect(url_for('views.home'))


    class AdminView(AdminIndexView):
        def is_accessible(self):
            if current_user.is_authenticated:
                if current_user.role == 'Admin':
                    return True
            else:
                False

        def inaccessible_callback(self, name, **kwargs):
            flash("Don't Have Permission", category='error')
            return redirect(url_for('views.home'))

    admin = Admin(app, index_view=AdminView(), template_mode='bootstrap4')
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(History, db.session))

    return app
    
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
