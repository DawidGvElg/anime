from flask import Flask, render_template, url_for, request, flash, redirect
import urllib.request
import os
from werkzeug.utils import secure_filename
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import random

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)
connection.autocommit = True

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
  
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET'])
@app.route("/anime", methods=['GET'])
def index():
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

    return render_template("index.html", anime=anime, characters=characters, randompic=randompic)

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
        filename = request.form['image_sourse']
        if not title:
            flash('title is required!')
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            conn = connection
            cur.execute('INSERT INTO anime1 (title, image, author, description, status, image_source) VALUES (%s, %s, %s, %s, %s, %s)',
                         (title, image, author, description, status, filename ))
            conn.commit()

    cur.execute('SELECT * FROM anime1')     
    anime = cur.fetchall()
    cur.close()
    return render_template("createanime.html", anime=anime)

@app.route("/anime/login")
def sign_in():
    return render_template("sign_in.html")


@app.route("/anime/register", methods=('GET', 'POST'))
def sign_up():
    conn = connection
    cur = conn.cursor()
    if request.method == 'POST':
        user_nick = request.form['user_nick']
        mail = request.form['mail']
        password = request.form['password']
        if not user_nick or mail or password:
            flash('You are missing something!')
        else:
            conn = connection
            cur.execute('INSERT INTO users (user_nick, mail, password) VALUES (%s, %s, crypt(%s, gen_salt(\'bf\', 8))',
                         (user_nick, mail, password))
            conn.commit()
    cur.execute('SELECT * FROM users')
    users = cur.fetchone()
    cur.close()
    return render_template("sign_up.html", users=users)


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
    