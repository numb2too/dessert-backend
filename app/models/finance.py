from datetime import datetime
from app import db
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
import enum

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

# ==================== 財務模組 ====================
class MaterialUnitEnum(enum.Enum):
    """材料單位枚舉"""
    KG = "公斤"
    G = "公克"
    L = "公升"
    ML = "毫升"
    PIECE = "個"
    PACKAGE = "包"

class Material(db.Model, TimestampMixin):
    """材料表"""
    __tablename__ = 'materials'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    unit = Column(Enum(MaterialUnitEnum), nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    current_stock = Column(Numeric(10, 2), default=0, nullable=False)
    min_stock = Column(Numeric(10, 2), default=0)
    supplier = Column(String(200))
    notes = Column(Text)
    
    # 關聯
    stock_movements = relationship('MaterialStockMovement', back_populates='material', cascade='all, delete-orphan')
    recipe_materials = relationship('RecipeMaterial', back_populates='material')
    
    def __repr__(self):
        return f'<Material {self.code}: {self.name}>'

class MovementTypeEnum(enum.Enum):
    """庫存異動類型枚舉"""
    IN = "入庫"
    OUT = "出庫"
    ADJUST = "調整"
    RETURN = "退貨"

class MaterialStockMovement(db.Model, TimestampMixin):
    """材料庫存異動表"""
    __tablename__ = 'material_stock_movements'
    
    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    movement_type = Column(Enum(MovementTypeEnum), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)
    unit_price = Column(Numeric(10, 2))
    reference_type = Column(String(50))  # 'order', 'production', 'purchase'
    reference_id = Column(Integer)
    notes = Column(Text)
    operated_by = Column(Integer, ForeignKey('employees.id'))
    
    material = relationship('Material', back_populates='stock_movements')
    operator = relationship('Employee')
    
    def __repr__(self):
        return f'<MaterialStockMovement {self.material_id}: {self.movement_type.value}>'

class TransactionTypeEnum(enum.Enum):
    """交易類型枚舉"""
    INCOME = "收入"
    EXPENSE = "支出"

class TransactionCategoryEnum(enum.Enum):
    """交易分類枚舉"""
    SALES = "銷售收入"
    MATERIAL = "材料採購"
    SALARY = "薪資支出"
    RENT = "租金"
    UTILITY = "水電費"
    MARKETING = "行銷費用"
    OTHER = "其他"

class FinancialTransaction(db.Model, TimestampMixin):
    """財務交易紀錄表"""
    __tablename__ = 'financial_transactions'
    
    id = Column(Integer, primary_key=True)
    transaction_date = Column(Date, nullable=False, index=True)
    transaction_type = Column(Enum(TransactionTypeEnum), nullable=False)
    category = Column(Enum(TransactionCategoryEnum), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    reference_type = Column(String(50))  # 'order', 'salary', 'material'
    reference_id = Column(Integer)
    description = Column(Text)
    created_by = Column(Integer, ForeignKey('employees.id'))
    
    creator = relationship('Employee')
    
    def __repr__(self):
        return f'<FinancialTransaction {self.transaction_date}: {self.amount}>'

class CakeCost(db.Model, TimestampMixin):
    """蛋糕製作成本紀錄表"""
    __tablename__ = 'cake_costs'
    
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    production_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    material_cost = Column(Numeric(10, 2), nullable=False)
    labor_cost = Column(Numeric(10, 2), default=0)
    overhead_cost = Column(Numeric(10, 2), default=0)
    total_cost = Column(Numeric(10, 2), nullable=False)
    cost_per_unit = Column(Numeric(10, 2), nullable=False)
    notes = Column(Text)
    
    recipe = relationship('Recipe')
    
    def __repr__(self):
        return f'<CakeCost {self.recipe_id}: {self.production_date}>'