from apiflask import APIBlueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.sales_production_rd import ProductionBatch, ProductionItem, DailyCapacity, OrderItem

production_bp = APIBlueprint('production', __name__, tag='生產管理')

@production_bp.get('/batches')
@jwt_required()
def get_production_batches():
    """取得生產批次列表"""
    batches = ProductionBatch.query.order_by(
        ProductionBatch.production_date.desc()
    ).limit(50).all()
    
    return [{
        'id': b.id,
        'batch_number': b.batch_number,
        'production_date': b.production_date.isoformat(),
        'status': b.status.value,
        'total_items': b.total_items,
        'completed_items': b.completed_items,
        'progress': round((b.completed_items / b.total_items * 100) if b.total_items > 0 else 0, 2),
        'supervisor': b.supervisor.name if b.supervisor else None
    } for b in batches]

@production_bp.post('/batches')
@jwt_required()
def create_production_batch():
    """建立生產批次"""
    from datetime import datetime, date
    
    production_date = date.today()
    batch_count = ProductionBatch.query.filter(
        ProductionBatch.production_date == production_date
    ).count() + 1
    
    batch_number = f"BATCH{production_date.strftime('%Y%m%d')}{batch_count:03d}"
    
    batch = ProductionBatch(
        batch_number=batch_number,
        production_date=production_date,
        status='PLANNED',
        supervisor_id=get_jwt_identity()
    )
    
    db.session.add(batch)
    db.session.commit()
    
    return {'id': batch.id, 'batch_number': batch.batch_number}, 201

@production_bp.get('/daily-capacity')
@jwt_required()
def get_daily_capacity():
    """取得每日產能（未來7天）"""
    from datetime import date, timedelta
    
    today = date.today()
    capacities = []
    
    for i in range(7):
        check_date = today + timedelta(days=i)
        capacity = DailyCapacity.query.filter_by(date=check_date).first()
        
        if not capacity:
            capacity = DailyCapacity(
                date=check_date,
                max_cakes=100,
                scheduled_cakes=0
            )
            db.session.add(capacity)
        
        capacities.append({
            'date': check_date.isoformat(),
            'max_cakes': capacity.max_cakes,
            'scheduled_cakes': capacity.scheduled_cakes,
            'available': capacity.max_cakes - capacity.scheduled_cakes,
            'utilization': round((capacity.scheduled_cakes / capacity.max_cakes * 100), 2)
        })
    
    db.session.commit()
    return capacities

@production_bp.patch('/items/<int:item_id>/complete')
@jwt_required()
def complete_production_item(item_id):
    """完成生產項目"""
    from datetime import datetime
    
    item = ProductionItem.query.get_or_404(item_id)
    item.status = 'COMPLETED'
    item.actual_quantity = item.planned_quantity
    item.completed_at = datetime.utcnow()
    
    # 更新批次完成數量
    batch = item.batch
    batch.completed_items += item.actual_quantity
    
    db.session.commit()
    return {'message': 'Production item completed'}