from datetime import datetime
from app import db
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text, ForeignKey, Enum, Date, Boolean
from sqlalchemy.orm import relationship
import enum

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

# ==================== 銷售模組 ====================
class Customer(db.Model, TimestampMixin):
    """客戶表"""
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    customer_code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(120))
    address = Column(String(255))
    birthday = Column(Date)
    notes = Column(Text)
    is_vip = Column(Boolean, default=False)
    
    # 關聯
    orders = relationship('Order', back_populates='customer', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Customer {self.customer_code}: {self.name}>'

class OrderStatusEnum(enum.Enum):
    """訂單狀態枚舉"""
    PENDING = "待確認"
    CONFIRMED = "已確認"
    IN_PRODUCTION = "生產中"
    COMPLETED = "已完成"
    DELIVERED = "已交付"
    CANCELLED = "已取消"

class OrderPriorityEnum(enum.Enum):
    """訂單優先級枚舉"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4

class Order(db.Model, TimestampMixin):
    """訂單表"""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    order_number = Column(String(30), unique=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    order_date = Column(Date, nullable=False, index=True)
    delivery_date = Column(Date, nullable=False)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING, nullable=False, index=True)
    priority = Column(Enum(OrderPriorityEnum), default=OrderPriorityEnum.NORMAL, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    paid_amount = Column(Numeric(10, 2), default=0)
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey('employees.id'))
    
    # 關聯
    customer = relationship('Customer', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    creator = relationship('Employee')
    
    def __repr__(self):
        return f'<Order {self.order_number}: {self.status.value}>'

class OrderItem(db.Model, TimestampMixin):
    """訂單項目表"""
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    special_requirements = Column(Text)
    
    # 關聯
    order = relationship('Order', back_populates='order_items')
    recipe = relationship('Recipe')
    production_items = relationship('ProductionItem', back_populates='order_item')
    
    def __repr__(self):
        return f'<OrderItem {self.order_id}-{self.recipe_id}>'

# ==================== 生產模組 ====================
class ProductionStatusEnum(enum.Enum):
    """生產狀態枚舉"""
    PLANNED = "已排程"
    IN_PROGRESS = "進行中"
    COMPLETED = "已完成"
    CANCELLED = "已取消"

class ProductionBatch(db.Model, TimestampMixin):
    """生產批次表"""
    __tablename__ = 'production_batches'
    
    id = Column(Integer, primary_key=True)
    batch_number = Column(String(30), unique=True, nullable=False, index=True)
    production_date = Column(Date, nullable=False, index=True)
    status = Column(Enum(ProductionStatusEnum), default=ProductionStatusEnum.PLANNED, nullable=False)
    total_items = Column(Integer, default=0)
    completed_items = Column(Integer, default=0)
    notes = Column(Text)
    supervisor_id = Column(Integer, ForeignKey('employees.id'))
    
    # 關聯
    production_items = relationship('ProductionItem', back_populates='batch', cascade='all, delete-orphan')
    supervisor = relationship('Employee')
    
    def __repr__(self):
        return f'<ProductionBatch {self.batch_number}: {self.production_date}>'

class ProductionItem(db.Model, TimestampMixin):
    """生產項目表"""
    __tablename__ = 'production_items'
    
    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer, ForeignKey('production_batches.id'), nullable=False)
    order_item_id = Column(Integer, ForeignKey('order_items.id'))
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    planned_quantity = Column(Integer, nullable=False)
    actual_quantity = Column(Integer, default=0)
    status = Column(Enum(ProductionStatusEnum), default=ProductionStatusEnum.PLANNED, nullable=False)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    notes = Column(Text)
    
    # 關聯
    batch = relationship('ProductionBatch', back_populates='production_items')
    order_item = relationship('OrderItem', back_populates='production_items')
    recipe = relationship('Recipe')
    
    def __repr__(self):
        return f'<ProductionItem {self.batch_id}-{self.recipe_id}>'

class DailyCapacity(db.Model, TimestampMixin):
    """每日產能表"""
    __tablename__ = 'daily_capacities'
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, unique=True, nullable=False, index=True)
    max_cakes = Column(Integer, nullable=False)
    scheduled_cakes = Column(Integer, default=0)
    notes = Column(Text)
    
    def __repr__(self):
        return f'<DailyCapacity {self.date}: {self.scheduled_cakes}/{self.max_cakes}>'

# ==================== 研發模組 ====================
class RecipeCategoryEnum(enum.Enum):
    """食譜分類枚舉"""
    CAKE = "蛋糕"
    TART = "塔派"
    COOKIE = "餅乾"
    MOUSSE = "慕斯"
    BREAD = "麵包"
    OTHER = "其他"

class RecipeStatusEnum(enum.Enum):
    """食譜狀態枚舉"""
    DRAFT = "草稿"
    TESTING = "測試中"
    ACTIVE = "使用中"
    ARCHIVED = "已封存"

class Recipe(db.Model, TimestampMixin):
    """食譜表"""
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(30), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    category = Column(Enum(RecipeCategoryEnum), nullable=False)
    status = Column(Enum(RecipeStatusEnum), default=RecipeStatusEnum.DRAFT, nullable=False)
    version = Column(String(10), default='1.0')
    description = Column(Text)
    instructions = Column(Text)
    preparation_time = Column(Integer)  # 分鐘
    baking_time = Column(Integer)  # 分鐘
    serving_size = Column(Integer)
    difficulty_level = Column(Integer)  # 1-5
    selling_price = Column(Numeric(10, 2))
    developer_id = Column(Integer, ForeignKey('employees.id'))
    
    # 關聯
    recipe_materials = relationship('RecipeMaterial', back_populates='recipe', cascade='all, delete-orphan')
    developer = relationship('Employee')
    
    def __repr__(self):
        return f'<Recipe {self.code}: {self.name}>'

class RecipeMaterial(db.Model, TimestampMixin):
    """食譜材料表（多對多關聯表）"""
    __tablename__ = 'recipe_materials'
    
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)
    notes = Column(String(200))
    
    # 關聯
    recipe = relationship('Recipe', back_populates='recipe_materials')
    material = relationship('Material', back_populates='recipe_materials')
    
    def __repr__(self):
        return f'<RecipeMaterial {self.recipe_id}-{self.material_id}>'