import json
import os
from flask import Flask, request, render_template
from flask_jwt import JWT, jwt_required, current_identity
from datetime import timedelta 
from flask_uploads import UploadSet, configure_uploads, IMAGES, TEXT, DOCUMENTS
from sqlalchemy.exc import IntegrityError

from models import db, User, SavedMovie, Movie, Cast, Crew

''' Begin boilerplate code '''
from App.views import (
    api_views,
    user_views
)

def get_db_uri(scheme='sqlite://', user='', password='', host='//demo.db', port='', name=''):
    return scheme+'://'+user+':'+password+'@'+host+':'+port+'/'+name 

def loadConfig(app):
    #try to load config from file, if fails then try to load from environment
    try:
        app.config.from_object('App.config')
        app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri() if app.config['SQLITEDB'] else app.config['DBURI']
    except:
        print("config file not present using environment variables")
        # DBUSER = os.environ.get("DBUSER")
        # DBPASSWORD = os.environ.get("DBPASSWORD")
        # DBHOST = os.environ.get("DBHOST")
        # DBPORT = os.environ.get("DBPORT")
        # DBNAME = os.environ.get("DBNAME")
        DBURI = os.environ.get("DBURI")
        SQLITEDB = os.environ.get("SQLITEDB", default="true")
        app.config['ENV'] = os.environ.get("ENV")
        app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri() if SQLITEDB in {'True', 'true', 'TRUE'} else DBURI

        
        
def create_app():
    app = Flask(__name__, static_url_path='/static')
    loadConfig(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bigData.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "MYSECRET"
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) 
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    
    db.init_app(app)
    return app

app = create_app()

app.app_context().push()
''' End Boilerplate Code '''

app.register_blueprint(api_views)
app.register_blueprint(user_views)

''' Set up JWT here (if using flask JWT)'''
# def authenticate(uname, password):
#   pass

# #Payload is a dictionary which is passed to the function by Flask JWT
# def identity(payload):
#   pass

# jwt = JWT(app, authenticate, identity)

def authenticate(uname, password):
  #search for the specified user
  user = User.query.filter_by(username=uname).first()
  #if user is found and password matches
  if user and user.check_password(password):
    return user

#Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
  return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)

''' End JWT Setup '''


# edit to query 50 pokemon objects and send to template
@app.route('/')
def index():
    movieList = Movie.query.limit(10)
    return render_template('index.html', movieList=movieList)

@app.route('/app')
def client_app():
    return app.send_static_file('app.html')



@app.route('/movies', methods=['GET'])
def movies():
    movieList = Movie.query.all()
    return render_template('app.html', movieList=movies)  

@app.route('/movies/<id>', methods=['GET'])
def moviess():
    movieList = Movie.query.all()
    movie = Movie.query.get(id)
    return render_template('app.html', movieList=movies)  


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    newuser = User(username=data['username'], email=data['email'])
    newuser.set_password(data['password'])
    try:
        db.session.add(newuser)
        db.session.commit()
    except IntegrityError:  # attempted to insert a duplicate user
        db.session.rollback()
        return 'username or email already exists' # error message
    return 'user created' # success
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
