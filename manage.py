import click
from flask.cli import FlaskGroup
from app import create_app, db
from app.models import *

def create_cli_app():
    return create_app()

@click.group(cls=FlaskGroup, create_app=create_cli_app)
def cli():
    """管理命令"""
    pass

@cli.command("init-db")
def init_db():
    """初始化資料庫"""
    click.echo("Creating database tables...")
    db.create_all()
    click.echo("Database initialized!")

@cli.command("seed-db")
def seed_db():
    """填充測試資料"""
    from datetime import date, datetime, timedelta
    from decimal import Decimal
    
    click.echo("Seeding database...")
    
    # 建立測試員工
    employees = [
        Employee(
            employee_code='EMP001',
            name='張經理',
            email='manager@bakery.com',
            phone='0912345678',
            department='HR',
            position='MANAGER',
            hire_date=date(2020, 1, 1),
            is_active=True
        ),
        Employee(
            employee_code='EMP002',
            name='李師傅',
            email='chef@bakery.com',
            phone='0923456789',
            department='PRODUCTION',
            position='STAFF',
            hire_date=date(2021, 3, 15),
            is_active=True
        ),
        Employee(
            employee_code='EMP003',
            name='王研發',
            email='rd@bakery.com',
            phone='0934567890',
            department='RD',
            position='SUPERVISOR',
            hire_date=date(2021, 6, 1),
            is_active=True
        ),
    ]
    
    for emp in employees:
        db.session.add(emp)
    db.session.commit()
    
    # 建立使用者帳號
    for emp in employees:
        user = User(
            employee_id=emp.id,
            username=emp.employee_code.lower(),
            is_active=True
        )
        user.set_password('password123')
        db.session.add(user)
    db.session.commit()
    
    # 建立測試材料
    materials = [
        Material(
            code='MAT001',
            name='高筋麵粉',
            unit='KG',
            unit_price=Decimal('50.00'),
            current_stock=Decimal('100.0'),
            min_stock=Decimal('20.0'),
            supplier='大華食品'
        ),
        Material(
            code='MAT002',
            name='雞蛋',
            unit='PIECE',
            unit_price=Decimal('5.00'),
            current_stock=Decimal('500'),
            min_stock=Decimal('100'),
            supplier='新鮮蛋行'
        ),
        Material(
            code='MAT003',
            name='奶油',
            unit='KG',
            unit_price=Decimal('200.00'),
            current_stock=Decimal('50.0'),
            min_stock=Decimal('10.0'),
            supplier='進口食材'
        ),
    ]
    
    for mat in materials:
        db.session.add(mat)
    db.session.commit()
    
    # 建立測試食譜
    recipes = [
        Recipe(
            code='CAKE001',
            name='經典巧克力蛋糕',
            category='CAKE',
            status='ACTIVE',
            version='1.0',
            description='濃郁巧克力風味',
            preparation_time=30,
            baking_time=45,
            serving_size=8,
            difficulty_level=3,
            selling_price=Decimal('500.00'),
            developer_id=employees[2].id
        ),
        Recipe(
            code='CAKE002',
            name='草莓蛋糕',
            category='CAKE',
            status='ACTIVE',
            version='1.0',
            description='新鮮草莓搭配鮮奶油',
            preparation_time=40,
            baking_time=40,
            serving_size=8,
            difficulty_level=4,
            selling_price=Decimal('600.00'),
            developer_id=employees[2].id
        ),
    ]
    
    for recipe in recipes:
        db.session.add(recipe)
    db.session.commit()
    
    # 建立食譜材料關聯
    recipe_materials = [
        RecipeMaterial(recipe_id=recipes[0].id, material_id=materials[0].id, quantity=Decimal('0.5')),
        RecipeMaterial(recipe_id=recipes[0].id, material_id=materials[1].id, quantity=Decimal('4')),
        RecipeMaterial(recipe_id=recipes[0].id, material_id=materials[2].id, quantity=Decimal('0.2')),
    ]
    
    for rm in recipe_materials:
        db.session.add(rm)
    db.session.commit()
    
    # 建立測試客戶
    customers = [
        Customer(
            customer_code='CUST001',
            name='陳小姐',
            phone='0987654321',
            email='chen@example.com',
            address='台中市西區',
            is_vip=True
        ),
        Customer(
            customer_code='CUST002',
            name='林先生',
            phone='0976543210',
            email='lin@example.com',
            address='台中市北區',
            is_vip=False
        ),
    ]
    
    for cust in customers:
        db.session.add(cust)
    db.session.commit()
    
    # 建立測試訂單
    order = Order(
        order_number='ORD20240101001',
        customer_id=customers[0].id,
        order_date=date.today(),
        delivery_date=date.today() + timedelta(days=3),
        status='CONFIRMED',
        priority='NORMAL',
        total_amount=Decimal('1100.00'),
        paid_amount=Decimal('0.00'),
        created_by=employees[0].id
    )
    db.session.add(order)
    db.session.commit()
    
    # 建立訂單項目
    order_items = [
        OrderItem(
            order_id=order.id,
            recipe_id=recipes[0].id,
            quantity=1,
            unit_price=Decimal('500.00'),
            subtotal=Decimal('500.00')
        ),
        OrderItem(
            order_id=order.id,
            recipe_id=recipes[1].id,
            quantity=1,
            unit_price=Decimal('600.00'),
            subtotal=Decimal('600.00')
        ),
    ]
    
    for item in order_items:
        db.session.add(item)
    db.session.commit()
    
    click.echo("✅ Database seeded successfully!")
    click.echo(f"Created {len(employees)} employees")
    click.echo(f"Created {len(materials)} materials")
    click.echo(f"Created {len(recipes)} recipes")
    click.echo(f"Created {len(customers)} customers")
    click.echo(f"Created 1 order with {len(order_items)} items")

@cli.command("create-admin")
@click.option('--username', prompt=True, help='管理員帳號')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='密碼')
def create_admin(username, password):
    """建立管理員帳號"""
    from datetime import date
    
    # 檢查是否已存在
    if User.query.filter_by(username=username).first():
        click.echo(f"❌ Username '{username}' already exists!")
        return
    
    # 建立管理員員工
    employee = Employee(
        employee_code='ADMIN',
        name='系統管理員',
        email='admin@bakery.com',
        department='HR',
        position='MANAGER',
        hire_date=date.today(),
        is_active=True
    )
    db.session.add(employee)
    db.session.commit()
    
    # 建立使用者
    user = User(
        employee_id=employee.id,
        username=username,
        is_active=True
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    click.echo(f"✅ Admin user '{username}' created successfully!")

if __name__ == '__main__':
    cli()