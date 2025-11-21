from apiflask import Schema
from apiflask.fields import String, Integer, Date, Decimal, Boolean, Nested, List
from apiflask.validators import Length, Range, OneOf

class CustomerInput(Schema):
    customer_code = String(required=True, validate=Length(max=20))
    name = String(required=True, validate=Length(max=100))
    phone = String(required=True, validate=Length(max=20))
    email = String(validate=Length(max=120))
    address = String(validate=Length(max=255))
    birthday = Date()
    notes = String()
    is_vip = Boolean()

class CustomerOutput(Schema):
    id = Integer()
    customer_code = String()
    name = String()
    phone = String()
    email = String()
    address = String()
    birthday = Date()
    is_vip = Boolean()
    created_at = String()

class CustomerQuery(Schema):
    search = String()
    is_vip = Boolean()

class OrderItemInput(Schema):
    recipe_id = Integer(required=True)
    quantity = Integer(required=True)
    unit_price = Decimal(required=True)
    subtotal = Decimal(required=True)
    special_requirements = String()

class OrderItemOutput(Schema):
    id = Integer()
    recipe_id = Integer()
    quantity = Integer()
    unit_price = Decimal()
    subtotal = Decimal()
    special_requirements = String()

class OrderInput(Schema):
    customer_id = Integer(required=True)
    order_date = Date()
    delivery_date = Date(required=True)
    priority = Integer(validate=Range(min=1, max=4))
    notes = String()
    order_items = List(Nested(OrderItemInput), required=True)

class OrderOutput(Schema):
    id = Integer()
    order_number = String()
    customer_id = Integer()
    order_date = Date()
    delivery_date = Date()
    status = String()
    priority = Integer()
    total_amount = Decimal()
    paid_amount = Decimal()
    notes = String()

class OrderWithDetailsOutput(Schema):
    id = Integer()
    order_number = String()
    customer = Nested(CustomerOutput)
    order_date = Date()
    delivery_date = Date()
    status = String()
    priority = Integer()
    total_amount = Decimal()
    paid_amount = Decimal()
    order_items = List(Nested(OrderItemOutput))
    production_progress = Decimal()
    notes = String()

class OrderQuery(Schema):
    status = String(validate=OneOf(['PENDING', 'CONFIRMED', 'IN_PRODUCTION', 'COMPLETED', 'DELIVERED', 'CANCELLED']))
    customer_id = Integer()
    order_date_from = Date()
    order_date_to = Date()
    delivery_date_from = Date()
    delivery_date_to = Date()
    sort_by = String(validate=OneOf(['priority', 'delivery_date', 'order_date']))