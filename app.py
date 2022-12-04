from flask import Flask, render_template, url_for, request, flash, redirect
import os
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


# @app.route("/")
# def index():
#     conn = connection
#     cur = conn.cursor()
#     cur.execute('CREATE TABLE IF NOT EXISTS anime1 (id_anime int PRIMARY KEY,'
#                                  'title varchar (150) NOT NULL,'
#                                  'image bytea,'
#                                  'author varchar (50) NOT NULL,'
#                                  'decription varchar(200) NOT NULL,'
#                                  'rating integer NOT NULL,'
#                                  'status varchar (10) NOT NULL,'
#                                  'review text );'
#                                  )
    # cur.execute('CREATE TABLE IF NOT EXISTS characters (id_char int NOT NULL,'
    #                              'name varchar (150) NOT NULL );'
    #                              )
    # cur.execute('CREATE TABLE IF NOT EXISTS images (id_image int PRIMARY KEY,'
    #                              'image bytea );'
    #                              )                             
    # cur.execute("""INSERT INTO anime1 (id_anime, title, image, author, decription, rating, status, review) VALUES
    #             (1, 'Naruto',bytea('naruto.jpg'), 'Масаси Кисимото','Бездомный пацан хочет стать президентом', 9, 'Закончен','10 флэшбеков из 10'  ),
    #             (2, 'One Piece',bytea('onepiece.jpg'), 'Эйитиро Ода','Поехавшая резина с отбитыми ищет один кусок', 10, 'Ongoing','Я не доживу до конца аниме'  ),
    #             (3, 'One Punch Man',bytea('opm.jpg'), 'ONE','Лысый мужик ищет смысл жизни', 8, 'Ongoing','Не ну рука у него конечно рабочая'  );""")
    
    # cur.execute("""INSERT INTO characters (id_char, name) VALUES
    #             (1, 'Naruto'),
    #             (1, 'Saske'),
    #             (1, 'Sakura'),
    #             (2, 'Monky D Luffy'),
    #             (2, 'Roronora Zorro'),
    #             (2, 'Chopper'),
    #             (2, 'Nami'),
    #             (3, 'Лысый'),
    #             (3, 'Genos');""")

    # cur.execute("""INSERT INTO images (id_image, image) VALUES
    #             (1, bytea('naruto.jpg')),
    #             (2, bytea('onepiece.jpg')),
    #             (3, bytea('opm.jpg'));""")

@app.route("/", methods=['GET'])
@app.route("/anime", methods=['GET'])
def index():
    conn = connection
    cur = conn.cursor()
    cur.execute('SELECT * FROM anime1;')
    anime = cur.fetchall()
    cur.execute('SELECT * FROM characters;')
    characters = cur.fetchall()
    cur.execute('SELECT * FROM randompic ORDER BY random ()')
    randompic = cur.fetchone() 
    q= request.args.get('q')

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
        if not title:
            flash('title is required!')
        else:
            conn = connection
            cur.execute('INSERT INTO anime1 (title, image, author, description, status) VALUES (%s, %s, %s, %s, %s)',
                         (title, image, author, description, status ))
            conn.commit()

    cur.execute('SELECT * FROM anime1')
    anime = cur.fetchall()
    cur.close()
    return render_template("createanime.html", anime=anime)

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
    