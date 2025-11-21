from app.extensions import db

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    estimated_cost = db.Column(db.Float, nullable=False) # 成本
    price = db.Column(db.Float, nullable=False)          # 售價
    
    # 簡易庫存概念：此食譜製作一個蛋糕扣除的庫存量，此處簡化為直接關聯
    daily_limit = db.Column(db.Integer, default=50) # 每日產能限制

    orders = db.relationship('OrderItem', backref='recipe', lazy=True)