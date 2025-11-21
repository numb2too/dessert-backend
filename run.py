import os
import time
from apiflask import APIFlask
from sqlalchemy import text
from app import db
from app.routes.user_routes import user_bp


def create_app(config=None):
    """Application Factory Pattern"""
    app = APIFlask(__name__)

    # 預設配置
    default_config = {
        "SQLALCHEMY_DATABASE_URI": os.getenv("DATABASE_URL", "sqlite:///:memory:"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "TESTING": False,
    }

    # 套用配置
    app.config.update(default_config)
    if config:
        app.config.update(config)

    # 初始化資料庫
    db.init_app(app)

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


def init_database(app):
    """初始化資料庫表格"""
    with app.app_context():
        try:
            # 檢查是否為 SQLite 或 MySQL
            db_uri = app.config["SQLALCHEMY_DATABASE_URI"]

            if "mysql" in db_uri or "postgresql" in db_uri:
                # 對於 MySQL/PostgreSQL,檢查表是否存在
                with db.engine.connect() as conn:
                    result = conn.execute(text("SHOW TABLES LIKE 'users'")).fetchone()

                if result:
                    print("ℹ️  Tables already exist, skipping creation")
                    return

            print("🔨 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")

        except Exception as e:
            print(f"⚠️  Error during table creation: {e}")
            db.create_all()
            print("✅ Tables created (forced)")


# 創建應用實例
app = create_app()

# 只在非測試環境下初始化資料庫
if not os.getenv("TESTING"):
    wait_for_db(app)
    init_database(app)

if __name__ == "__main__":
    import debugpy

    debugpy.listen(("0.0.0.0", 5678))
    print("⏳ Waiting for debugger to attach...")

    app.run(host="0.0.0.0", port=1234, debug=False)
