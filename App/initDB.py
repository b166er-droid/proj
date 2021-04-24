from main import db, app, Movie, Cast, Crew
import csv, ast
import requests

db.drop_all()
db.create_all(app=app)

# replace any null values with None to avoid db errors

def isPictureStillWorking(url):
    try:
        page = requests.get(url)

    except Exception as e:
        print("error:", e)
        return False

    # check status code
    if (page.status_code != 200):
        return False

    return True

def noNull(val):
    if str(val) == "":
        return None
    return val

#'''
#Movies
movies = []
i = 0
with open('./Application/API/movies_metadata.csv', 'r', encoding="utf8") as movie:
    reader = csv.DictReader(movie)

    for line in reader:
        movies.append(
            {
                'title':line['title'],
                'lang':line['original_language'],
                'genres':"",
                'poster':"./Application/noPosterImage.jpg",
                'overview':line['overview'],
                'release_date':line['release_date'],

                'imdb_id':line['imdb_id']
            }
        )
        i = i+1
        if i == 5000:
            break

i = 0
with open('./Application/API/MovieGenre.csv', 'r') as movieStuff:
    reader = csv.DictReader(movieStuff)

    for line in reader:
        for movie in movies:
            if int(line['imdbId']) == int(movie['imdb_id']):
                movie['poster'] = line['Poster']
                movie['genres'] = line['Genre']
    
        i = i+1
        if i == 5000:
            break

for movie in movies:
    db.session.add(
        Movie(
            title=movie['title'],
            lang=movie['lang'],
            genres=movie['genres'],
            poster=movie['poster'],
            overview=movie['overview'],
            release_date=movie['release_date']
        )
    )

db.session.commit() #save

movieList = Movie.query.limit(10)
print(movieList[7].title, movieList[7].poster)
#'''
