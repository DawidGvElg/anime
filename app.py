from flask import Flask, session, render_template, url_for, request, flash, redirect
import urllib.request
import os
from flask_login import login_manager
from werkzeug.utils import secure_filename
import psycopg2
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import random


load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Super545sEcr8гetKet5v4v8zx8xc89asdxc'
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)
connection.autocommit = True

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
  
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_logged_user():
    conn= connection
    cur = conn.cursor()
    if "user" in session:
        id = session['user'][0]
        cur.execute('SELECT * FROM users WHERE id_users= %s', str(id))
        user = cur.fetchone()
        return user
    return None


@app.route("/", methods=['GET'])
@app.route("/anime", methods=['GET'])
def index():
    get_logged_user()
    user= get_logged_user()
    query = request.args
    search=''
    if 'search' in query:
        search = query['search']
    conn = connection
    cur = conn.cursor()
    if search != "":
        cur.execute('SELECT * FROM anime1 WHERE title ILIKE \'{}%\''.format(search))
    else:
         cur.execute('SELECT * FROM anime1;')
    anime = cur.fetchall()
    cur.execute('SELECT * FROM characters;')
    characters = cur.fetchall()
    cur.execute('SELECT * FROM randompic ORDER BY random ()')
    randompic = cur.fetchone()
    cur.execute('SELECT user_nick FROM users;')
    user = cur.fetchone()
    return render_template("index.html", anime=anime, characters=characters, randompic=randompic, user=user)

@app.route("/anime/<string:anime_id>", methods=('GET', 'POST'))

def animewa(anime_id):
    conn = connection
    cur = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        if not name:
            flash('Name is required!')
        else:
            conn = connection
            cur.execute('INSERT INTO review (name, content, anime_id) VALUES (%s, %s, %s)',
                         (name, content, anime_id ))
            conn.commit()

    cur.execute('SELECT * FROM review WHERE anime_id=\'{}\''.format(anime_id))
    review = cur.fetchall()
    cur.execute('SELECT * FROM anime1 WHERE anime_id=\'{}\''.format(anime_id))
    anime = cur.fetchall()
    cur.execute('SELECT * FROM characters WHERE anime_id=\'{}\''.format(anime_id))
    characters = cur.fetchall()
    cur.close()
    return render_template("animewa.html", review=review, anime=anime, characters=characters, anime_id=anime_id)


@app.route("/anime/create-anime", methods=('GET', 'POST'))
def createanime():
    conn = connection
    cur = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        image = request.form['image']
        author = request.form['author']
        description = request.form['description']
        status = request.form['status']
        genre_id = request.form['genre_id']
        anime_id =request.form['anime_id']
        file= request.files['image_sourse']
        filename= file.filename
        if not title:
            flash('title is required!')
        if 'image_sourse' not in request.files:
            flash('No file part')
            return redirect(request.url)
        if file.filename == '':
            flash('No image selected for uploading')
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            conn = connection
            cur.execute('INSERT INTO anime1 (title, image, author, description, status, image_sourse) VALUES (%s, %s, %s, %s, %s, %s)',
                         (title, image, author, description, status, filename ))
            cur.execute('SELECT * FROM anime1 WHERE title= tile')
            cur.execute('INSERT INTO genre_anime (genre_id, anime_id) VALUES (%s,%s)',
                        (anime_id, genre_id))             
            conn.commit()
    
    cur.execute('SELECT * FROM anime1 INNER JOIN genre_anime ON genre_anime.anime_id = anime1.anime_id INNER JOIN genres ON genre_anime.genre_id = genres.genre_id')     
    anime = cur.fetchall()
    cur.execute('SELECT * FROM genres')
    genre = cur.fetchall()
    cur.close()
    return render_template("createanime.html", anime=anime, genre=genre)

@app.route('/login', methods =['GET', 'POST'])
def login():
    conn = connection
    cur = conn.cursor()
    if request.method == 'POST' and 'user_nick' in request.form and 'password' in request.form:
        user_nick = request.form['user_nick']
        password = request.form['password']
        cur.execute('SELECT * FROM users WHERE user_nick = %s AND password = crypt(%s, password)',
                    (user_nick, password))
        account = cur.fetchone()
        session['loggedin'] = True
        session['user'] = account
        cur.close()
        return redirect(url_for('index'))
    else:
        flash('Incorrect username/password')
    return render_template('sign_in.html')    



@app.route("/anime/register", methods=('GET', 'POST'))
def sign_up():
    conn = connection
    cur = conn.cursor()
    if request.method == 'POST':
        user_nick = request.form['user_nick']
        mail = request.form['mail']
        password = request.form['password']
        if not user_nick or not mail or not password:
            flash('You are missing something!') 
            return render_template("sign_up.html")     
        else:
            conn = connection
            cur.execute('INSERT INTO users (user_nick, mail, password) VALUES (%s, %s, crypt(%s, gen_salt(\'bf\', 8)))',
                         (user_nick, mail, password))
            conn.commit()  
    cur.execute('SELECT * FROM users')
    users = cur.fetchone()
    cur.close()
    return render_template('sign_up.html', users=users)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin')
   session.pop('user')
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/profile')
def profile(): 
    conn = connection
    cur = conn.cursor()
    if 'loggedin' in session:
        cur.execute('SELECT * FROM users WHERE id = %s', [session['id']])
        account = cur.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))

@app.route("/anime/story")
def testlink():
    return render_template("bibka.html")
    

@app.errorhandler(404)
def pageNotFOund(error):
    return render_template("page404.html")
    
# with app.test_request_context():
#     print( url_for ('index') )

if __name__ == "__main__":
    app.run(debug=True)
    