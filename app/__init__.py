import os
from apiflask import APIFlask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name=None):
    """應用程式工廠函數"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = APIFlask(
        __name__,
        title='甜點店管理系統 API',
        version='1.0.0'
    )
    
    # 載入配置
    app.config.from_object(config[config_name])
    
    # 初始化擴展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # 註冊藍圖
    from app.routes import (
        auth_bp, hr_bp, finance_bp, 
        sales_bp, production_bp, rd_bp
    )
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(hr_bp, url_prefix='/api/hr')
    app.register_blueprint(finance_bp, url_prefix='/api/finance')
    app.register_blueprint(sales_bp, url_prefix='/api/sales')
    app.register_blueprint(production_bp, url_prefix='/api/production')
    app.register_blueprint(rd_bp, url_prefix='/api/rd')
    
    # 健康檢查端點
    @app.get('/health')
    def health_check():
        return {'status': 'healthy'}
    
    # 錯誤處理
    @app.errorhandler(404)
    def not_found(e):
        return {'message': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return {'message': 'Internal server error'}, 500
    
    return app