from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)

    def toDict(self):
        return{
            "user_id":self.user_id,
            "username":self.username,
            "password":self.password
        }

    def add_password(self,password):
        self.password = generate_password_hash(password, method='sha256')

    def verify_password():
        return check_password_hash(self.password, password)

class SavedMovie(db.Model):
    list_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    rating = db.Column(db.Integer, nullable = False)

    def toDict(self):
        return {
            "list_id":self.list_id,
            "user_id":self.user_id,
            "movie_id":self.movie_id,
            "rating":self.rating
        }

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    lang = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    poster = db.Column(db.String(120))
    overview = db.Column(db.String(180))
    release_date = db.Column(db.Integer)
    cast = db.relationship('Cast', backref='movie')
    crew = db.relationship('Crew', backref='movie')

    imdb_id = db.Column(db.String(120))
    #cast_id = db.Column(db.Integer, db.ForeignKey("cast.cast_id"))
    #crew_id = db.Column(db.Integer, db.ForeignKey("crew.crew_name"))

    def toDict(self):
        return {
            "id":self.id,
            "title":self.title,
            "cast":self.cast,
            "crew":self.crew,
            "release_date":self.release_date
        }

class Cast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cast_id = db.Column(db.Integer)
    credit_id = db.Column(db.String(120))
    name = db.Column(db.String(120)) #Cast member Real Name
    character = db.Column(db.String(120))

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))

    def toDict(self):
        return {
            "id":self.id,
            "cast_id":self.cast_id,
            "credit_id":self.credit_id,
            "cast_name":self.cast_name,
            "character":self.character
        }

class Crew(db.Model):
    id  = db.Column(db.Integer, primary_key = True)
    credit_id = db.Column(db.String(120))
    name = db.Column(db.String(120))
    department = db.Column(db.String(120))
    job = db.Column(db.String(120))

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))

    def toDict(self):
        return {
            "id":self.id,
            "credit_id":self.credit_id,
            "crew_name":self.crew_name,
            "department":self.department,
            "job":self.job
        }
