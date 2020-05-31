from flask import Flask


def create_app():
    """
    创造Flask实例，并进行配置
    :return: app：flask实例
    """
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='awfdgb86c4z51dg78sg6fd',
        #SQLALCHEMY_DATABASE_URI='mysql://username:password@hostname/database',
        #SQLALCHEMY_DATABASE_URI='mysql://root:root@127.0.0.1/movie',
        SQLALCHEMY_DATABASE_URI='mysql://ncov:123456@121.36.137.235:3306/ncov',
        SQLALCHEMY_COMMIT_ON_TEARDOWN=True,
    )
    # 将app与蓝图bp绑定
    from movieRecommendation import views
    app.register_blueprint(views.bp)
    views.db.init_app(app)

    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app

if __name__=='__main__':
    app=create_app()
    app.run(debug=True)
