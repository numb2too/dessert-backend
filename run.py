from dotenv import load_dotenv

load_dotenv()  # 載入 .env 檔

import os
import time
from apiflask import APIFlask
from sqlalchemy import text
from flask_migrate import Migrate  # 新增
from app import db
from app.routes.user_routes import user_bp

migrate = Migrate()  # 新增


def create_app(config=None):
    """Application Factory Pattern"""
    app = APIFlask(__name__)

    # 預設配置
    default_config = {
        "SQLALCHEMY_DATABASE_URI": os.getenv("DATABASE_URL", "sqlite:///dev.db"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "TESTING": False,
    }

    # 套用配置
    app.config.update(default_config)
    if config:
        app.config.update(config)

    # 初始化資料庫
    db.init_app(app)
    migrate.init_app(app, db)  # 新增

    # 註冊路由
    app.register_blueprint(user_bp, url_prefix="/api/users")

    return app


def wait_for_db(app, retries=30, delay=2):
    """等待資料庫連線就緒"""
    for i in range(retries):
        try:
            with app.app_context():
                with db.engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
            print("✅ Database connected!")
            return True
        except Exception as e:
            print(f"⏳ Waiting for database... ({i + 1}/{retries})")
            time.sleep(delay)
    raise Exception("❌ Could not connect to database after retries")


# 創建應用實例
app = create_app()

# 只在非測試環境下初始化資料庫
if not os.getenv("TESTING"):
    wait_for_db(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234, debug=True)
