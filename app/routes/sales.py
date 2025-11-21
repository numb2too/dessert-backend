from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, desc
from app import db
from app.models.sales_production_rd import Customer, Order, OrderItem, OrderStatusEnum
from app.schemas.sales import (
    CustomerInput, CustomerOutput, CustomerQuery,
    OrderInput, OrderOutput, OrderQuery, OrderWithDetailsOutput,
    OrderItemInput
)

sales_bp = APIBlueprint('sales', __name__, tag='銷售管理')

# ==================== 客戶管理 ====================
@sales_bp.get('/customers')
@jwt_required()
@sales_bp.input(CustomerQuery, location='query')
@sales_bp.output(CustomerOutput(many=True), status_code=200)
def get_customers(query_data):
    """取得客戶列表"""
    query = Customer.query
    
    if 'search' in query_data:
        search = f"%{query_data['search']}%"
        query = query.filter(
            db.or_(
                Customer.name.like(search),
                Customer.customer_code.like(search),
                Customer.phone.like(search)
            )
        )
    if 'is_vip' in query_data:
        query = query.filter_by(is_vip=query_data['is_vip'])
    
    query = query.order_by(Customer.created_at.desc())
    return query.all()

@sales_bp.get('/customers/<int:customer_id>')
@jwt_required()
@sales_bp.output(CustomerOutput, status_code=200)
def get_customer(customer_id):
    """取得客戶詳情（包含訂單歷史）"""
    customer = Customer.query.get_or_404(customer_id)
    return customer

@sales_bp.post('/customers')
@jwt_required()
@sales_bp.input(CustomerInput)
@sales_bp.output(CustomerOutput, status_code=201)
def create_customer(json_data):
    """新增客戶"""
    if Customer.query.filter_by(customer_code=json_data['customer_code']).first():
        abort(400, message='Customer code already exists')
    
    customer = Customer(**json_data)
    db.session.add(customer)
    db.session.commit()
    return customer

@sales_bp.patch('/customers/<int:customer_id>')
@jwt_required()
@sales_bp.input(CustomerInput(partial=True))
@sales_bp.output(CustomerOutput, status_code=200)
def update_customer(customer_id, json_data):
    """更新客戶資料"""
    customer = Customer.query.get_or_404(customer_id)
    for key, value in json_data.items():
        setattr(customer, key, value)
    db.session.commit()
    return customer

# ==================== 訂單管理 ====================
@sales_bp.get('/orders')
@jwt_required()
@sales_bp.input(OrderQuery, location='query')
@sales_bp.output(OrderOutput(many=True), status_code=200)
def get_orders(query_data):
    """取得訂單列表（可快速查詢與排序）"""
    query = Order.query
    
    # 過濾條件
    if 'status' in query_data:
        query = query.filter_by(status=query_data['status'])
    if 'customer_id' in query_data:
        query = query.filter_by(customer_id=query_data['customer_id'])
    if 'order_date_from' in query_data:
        query = query.filter(Order.order_date >= query_data['order_date_from'])
    if 'order_date_to' in query_data:
        query = query.filter(Order.order_date <= query_data['order_date_to'])
    if 'delivery_date_from' in query_data:
        query = query.filter(Order.delivery_date >= query_data['delivery_date_from'])
    if 'delivery_date_to' in query_data:
        query = query.filter(Order.delivery_date <= query_data['delivery_date_to'])
    
    # 排序：優先級降序（urgent優先），然後交付日期升序（越早越優先）
    sort_by = query_data.get('sort_by', 'priority')
    if sort_by == 'priority':
        query = query.order_by(desc(Order.priority), Order.delivery_date)
    elif sort_by == 'delivery_date':
        query = query.order_by(Order.delivery_date)
    elif sort_by == 'order_date':
        query = query.order_by(desc(Order.order_date))
    
    return query.all()

@sales_bp.get('/orders/<int:order_id>')
@jwt_required()
@sales_bp.output(OrderWithDetailsOutput, status_code=200)
def get_order(order_id):
    """取得訂單詳情（包含客戶資料、訂單項目、生產進度）"""
    order = Order.query.get_or_404(order_id)
    
    # 計算生產進度
    total_items = 0
    completed_items = 0
    for order_item in order.order_items:
        total_items += order_item.quantity
        for production_item in order_item.production_items:
            completed_items += production_item.actual_quantity
    
    production_progress = (completed_items / total_items * 100) if total_items > 0 else 0
    
    return {
        'id': order.id,
        'order_number': order.order_number,
        'customer': {
            'id': order.customer.id,
            'name': order.customer.name,
            'phone': order.customer.phone,
            'email': order.customer.email
        },
        'order_date': order.order_date,
        'delivery_date': order.delivery_date,
        'status': order.status.value,
        'priority': order.priority.value,
        'total_amount': float(order.total_amount),
        'paid_amount': float(order.paid_amount),
        'order_items': order.order_items,
        'production_progress': round(production_progress, 2),
        'notes': order.notes
    }

@sales_bp.post('/orders')
@jwt_required()
@sales_bp.input(OrderInput)
@sales_bp.output(OrderOutput, status_code=201)
def create_order(json_data):
    """新增訂單"""
    from datetime import datetime
    
    # 生成訂單編號
    order_date = json_data.get('order_date', datetime.now().date())
    order_count = Order.query.filter(
        func.date(Order.order_date) == order_date
    ).count() + 1
    order_number = f"ORD{order_date.strftime('%Y%m%d')}{order_count:04d}"
    
    # 計算總金額
    total_amount = sum(item['subtotal'] for item in json_data['order_items'])
    
    order = Order(
        order_number=order_number,
        customer_id=json_data['customer_id'],
        order_date=order_date,
        delivery_date=json_data['delivery_date'],
        priority=json_data.get('priority', 'NORMAL'),
        total_amount=total_amount,
        notes=json_data.get('notes'),
        created_by=get_jwt_identity()
    )
    
    # 新增訂單項目
    for item_data in json_data['order_items']:
        order_item = OrderItem(
            recipe_id=item_data['recipe_id'],
            quantity=item_data['quantity'],
            unit_price=item_data['unit_price'],
            subtotal=item_data['subtotal'],
            special_requirements=item_data.get('special_requirements')
        )
        order.order_items.append(order_item)
    
    db.session.add(order)
    db.session.commit()
    
    return order

@sales_bp.patch('/orders/<int:order_id>/status')
@jwt_required()
def update_order_status(order_id):
    """更新訂單狀態"""
    from apiflask import input
    
    @input({'status': {'type': 'string', 'required': True}})
    def _update(json_data):
        order = Order.query.get_or_404(order_id)
        order.status = OrderStatusEnum[json_data['status']]
        db.session.commit()
        return {'message': 'Order status updated successfully'}
    
    return _update()

@sales_bp.patch('/orders/<int:order_id>/priority')
@jwt_required()
def update_order_priority(order_id):
    """更新訂單優先級（排序功能）"""
    from apiflask import input
    
    @input({'priority': {'type': 'integer', 'required': True}})
    def _update(json_data):
        order = Order.query.get_or_404(order_id)
        order.priority = json_data['priority']
        db.session.commit()
        return {'message': 'Order priority updated successfully'}
    
    return _update()

# ==================== 統計報表 ====================
@sales_bp.get('/statistics/sales-summary')
@jwt_required()
def get_sales_summary():
    """取得銷售統計摘要"""
    from datetime import datetime, timedelta
    from sqlalchemy import extract
    
    today = datetime.now().date()
    this_month_start = today.replace(day=1)
    
    # 本月訂單統計
    monthly_orders = Order.query.filter(
        Order.order_date >= this_month_start
    ).all()
    
    monthly_revenue = sum(o.total_amount for o in monthly_orders)
    monthly_order_count = len(monthly_orders)
    
    # 待處理訂單
    pending_orders = Order.query.filter(
        Order.status.in_([OrderStatusEnum.PENDING, OrderStatusEnum.CONFIRMED])
    ).count()
    
    # 本月完成訂單
    completed_orders = Order.query.filter(
        Order.order_date >= this_month_start,
        Order.status == OrderStatusEnum.DELIVERED
    ).count()
    
    return {
        'monthly_revenue': float(monthly_revenue),
        'monthly_order_count': monthly_order_count,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders
    }