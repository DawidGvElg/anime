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