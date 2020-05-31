import csv
import time
import pymysql
import random

# 'movieId', 'title', 'genres', 'overview', 'imgurl','hits'
db = pymysql.connect("121.36.171.234", "ncov", "123456", "ncov")
cur = db.cursor()
sql3 = "insert into movies(movieId, title,genres, overview, imgurl,hits) values(%s,%s,%s,%s,%s,%s)"
f1 = open('ml-latest-small/movie3.csv', 'r', encoding='utf-8')
reader = csv.reader(f1)
ti = time.time()
num = 0
for x in list(reader)[:]:
    num += 1
    hits = random.randint(0, 10000)
    # print(x+[hits])
    try:
        cur.execute(sql3, x+[hits])
        db.commit()
    except Exception as e:
        print(e.args)
        print('插入词条到表movies:', x[0])
        db.rollback()
    if num % 100 == 0:
        print(num, '、', x[0], ' ', time.time() - ti)
f1.close()
db.commit()
db.close()
