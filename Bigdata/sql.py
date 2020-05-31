import pymysql

db = pymysql.connect("121.36.171.234", "ncov", "123456", "ncov")
cur = db.cursor()
# cur.execute("drop table summary")
# 'movieId', 'title', 'genres', 'overview', 'imgurl','hits'


cur.execute('create table links(id int primary key auto_increment,movieId varchar(300), imdbId varchar(300), tmdbId varchar(300))')
cur.execute('create table ratings(id int primary key auto_increment,userId varchar(300),movieId varchar(300), rating varchar(300), timestamp varchar(300))')
cur.execute('create table tags(id int primary key auto_increment,userId varchar(300),movieId varchar(300), tag varchar(300), timestamp varchar(300))')
cur.execute('create table movies(id int primary key auto_increment,movieId varchar(300),title varchar(300), genres varchar(300), overview text,imgurl varchar(300),hits varchar(300))')
cur.execute("alter table links add unique index_name(movieId)")
cur.execute("alter table ratings add unique index_name(userId,movieId)")
cur.execute("alter table tags add unique index_name(userId,movieId)")
cur.execute("alter table movies add unique index_name(movieId)")



db.commit()
db.close()
