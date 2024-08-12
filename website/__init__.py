from flask import Flask
import os
# from flask_wtf.csrf import CSRFProtect



def create_app():
   
   app = Flask(__name__ )
   
   # upload_folder = os.path.join('static', 'img')
   app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'main_project', 'website', 'static', 'pdf')
   # upload_folder = r"C:\Users\user\Desktop\flask_practice\main_project\website\static\img"
   
  
   # csrf = CSRFProtect(app)
   # csrf.init_app(app)
   # configs
   app.config['SECRET_KEY'] = 'mouad'
   # app.config["UPLOAD_FOLDER"] = "website/static/img/"
   app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
   
   
   
   from .routes import routes   
   
   app.register_blueprint(routes,url_prefix="/")
   
   return app 