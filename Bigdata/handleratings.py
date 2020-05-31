import csv
import time
import pymysql

db = pymysql.connect("121.36.171.234", "ncov", "123456", "ncov")
cur = db.cursor()
sql3 = "insert into ratings(userId,movieId,rating,timestamp) values(%s,%s,%s,%s)"
f1 = open('ml-latest-small/ratings.csv', 'r', encoding='utf-8')
reader = csv.reader(f1)
ti = time.time()
num = 0
for x in list(reader)[1:]:
    num += 1
    try:
        cur.execute(sql3, x)
        db.commit()
    except Exception as e:
        print(e.args)
        print('插入词条到表ratings:', x[0])
        db.rollback()
    if num % 1000 == 0:
        print(num, '、', x[0], ' ', time.time() - ti)
f1.close()
db.commit()
db.close()
