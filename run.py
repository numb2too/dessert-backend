import os
import time
from apiflask import APIFlask
from sqlalchemy import text
from flask_migrate import Migrate

from app import db
from app.routes.user_routes import user_bp
from config import config
from app.utils.error_handlers import register_error_handlers

migrate = Migrate()


def create_app(config_name=None):
    """Application Factory Pattern"""
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = APIFlask(__name__, title="甜點店員工成本系統 API", version="1.0")

    # 載入對應環境的配置
    app.config.from_object(config[config_name])

    # 初始化擴展
    db.init_app(app)
    migrate.init_app(app, db)

    # 註冊錯誤處理器
    register_error_handlers(app)

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

# 只在非測試環境下等待資料庫
if os.getenv("FLASK_ENV") != "testing":
    wait_for_db(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234)
