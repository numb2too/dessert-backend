from apiflask import APIBlueprint
from flask_jwt_extended import jwt_required
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app import db
from app.models.finance import Material, MaterialStockMovement, FinancialTransaction, CakeCost

finance_bp = APIBlueprint('finance', __name__, tag='財務管理')

@finance_bp.get('/materials')
@jwt_required()
def get_materials():
    """取得材料庫存列表"""
    materials = Material.query.order_by(Material.name).all()
    return [{
        'id': m.id,
        'code': m.code,
        'name': m.name,
        'unit': m.unit.value,
        'unit_price': float(m.unit_price),
        'current_stock': float(m.current_stock),
        'min_stock': float(m.min_stock),
        'stock_status': 'low' if m.current_stock <= m.min_stock else 'normal',
        'supplier': m.supplier
    } for m in materials]

@finance_bp.get('/materials/<int:material_id>/movements')
@jwt_required()
def get_material_movements(material_id):
    """取得材料庫存異動紀錄"""
    movements = MaterialStockMovement.query.filter_by(material_id=material_id)\
        .order_by(MaterialStockMovement.created_at.desc()).limit(100).all()
    return [{
        'id': m.id,
        'movement_type': m.movement_type.value,
        'quantity': float(m.quantity),
        'unit_price': float(m.unit_price) if m.unit_price else None,
        'reference_type': m.reference_type,
        'notes': m.notes,
        'created_at': m.created_at.isoformat()
    } for m in movements]

@finance_bp.get('/transactions')
@jwt_required()
def get_transactions():
    """取得財務交易紀錄"""
    from datetime import date
    transactions = FinancialTransaction.query.order_by(
        FinancialTransaction.transaction_date.desc()
    ).limit(100).all()
    return [{
        'id': t.id,
        'date': t.transaction_date.isoformat(),
        'type': t.transaction_type.value,
        'category': t.category.value,
        'amount': float(t.amount),
        'description': t.description
    } for t in transactions]

@finance_bp.get('/reports/profit-loss')
@jwt_required()
def profit_loss_report():
    """損益報表（即時盈利與成本分析）"""
    from datetime import date, timedelta
    
    # 本月開始日期
    today = date.today()
    month_start = today.replace(day=1)
    
    # 收入
    income = db.session.query(func.sum(FinancialTransaction.amount)).filter(
        FinancialTransaction.transaction_type == 'INCOME',
        FinancialTransaction.transaction_date >= month_start
    ).scalar() or 0
    
    # 支出
    expense = db.session.query(func.sum(FinancialTransaction.amount)).filter(
        FinancialTransaction.transaction_type == 'EXPENSE',
        FinancialTransaction.transaction_date >= month_start
    ).scalar() or 0
    
    # 材料成本
    material_cost = db.session.query(func.sum(CakeCost.material_cost)).filter(
        CakeCost.production_date >= month_start
    ).scalar() or 0
    
    # 計算淨利
    profit = float(income) - float(expense)
    profit_margin = (profit / float(income) * 100) if income > 0 else 0
    
    return {
        'period': f"{month_start.isoformat()} to {today.isoformat()}",
        'income': float(income),
        'expense': float(expense),
        'material_cost': float(material_cost),
        'profit': profit,
        'profit_margin': round(profit_margin, 2)
    }