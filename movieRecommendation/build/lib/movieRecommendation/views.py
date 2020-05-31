from flask import (
    Blueprint, request,render_template
)
from flask_sqlalchemy import SQLAlchemy
import random

bp = Blueprint('movie', __name__)
db = SQLAlchemy()


@bp.route('/recommendation', methods=['GET'])
def recommendation():
    selected_user_id=str(random.randint(1,610))
    # 反射数据库内所有的表
    db.reflect()
    all_table = {table_obj.name: table_obj for table_obj in db.get_tables_for_bind()}
    # 得到某个表
    movies_table=all_table["movies"]
    ratings_table=all_table["ratings"]
    prediction_table = all_table['prediction']
    # 查询数据库得到用户喜欢的电影信息
    movies_info1=db.session\
        .query(movies_table.c.title,movies_table.c.genres,movies_table.c.overview,movies_table.c.imgurl)\
        .join(ratings_table,movies_table.c.movieId==ratings_table.c.movieId)\
        .filter(ratings_table.c.userId==selected_user_id)\
        .order_by(ratings_table.c.rating.desc())\
        .limit(6).all()
    # 查询数据库得到推荐给用户的电影信息
    movies_info2 = db.session \
        .query(movies_table.c.title, movies_table.c.genres, movies_table.c.overview, movies_table.c.imgurl) \
        .join(prediction_table, movies_table.c.movieId == prediction_table.c.movieId) \
        .filter(prediction_table.c.userId == selected_user_id) \
        .order_by(prediction_table.c.rating.desc()) \
        .limit(6).all()
    return render_template('index.html',user_id=selected_user_id,like_movies=movies_info1,recommendation_movies=movies_info2)


@bp.route('/detail', methods=['GET'])
def detail():
    # 得到请求中的参数
    params = request.args
    # 若没有下面的参数，则返回404
    try:
        title = params['title']
        genres = params['genres']
        overview = params['overview']
        imgurl = params['imgurl']
    except Exception:
        return '404 not found'
    return render_template('detail.html',title=title,genres=genres,overview=overview,imgurl=imgurl)


@bp.route('/test', methods=['GET'])
def just_test():
    user_id=10
    like_movies=[('天气之子','anime','overview','https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2570059839.webp')
                 ,('天气之子','anime','overview','https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2570059839.webp')]
    recommendation_movies=[
        ('给我翅膀','encourage','overview', 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2561160802.webp'),
        ('给我翅膀','encourage','overview', 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2561160802.webp'),
    ]
    return render_template('index.html',user_id=user_id,like_movies=like_movies,recommendation_movies=recommendation_movies)