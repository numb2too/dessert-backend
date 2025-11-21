import os
import time
from apiflask import APIFlask
from sqlalchemy import text
from app import db
from app.routes.user_routes import user_bp

app = APIFlask(__name__)

# 資料庫設定
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///:memory:")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 初始化資料庫
db.init_app(app)

# 註冊路由
app.register_blueprint(user_bp, url_prefix="/api/users")


def wait_for_db(retries=30, delay=2):
    """等待資料庫連線就緒"""
    for i in range(retries):
        try:
            with db.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database connected!")
            return True
        except Exception as e:
            print(f"Waiting for database... ({i + 1}/{retries})")
            time.sleep(delay)
    raise Exception("Could not connect to database")


# 只在非測試環境下等待資料庫
if not os.getenv("TESTING"):
    with app.app_context():
        wait_for_db()
        db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234, debug=True)
