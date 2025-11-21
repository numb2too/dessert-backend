import pytest
from app import create_app, db
from app.models.user import User
from app.models import Employee
from datetime import date

@pytest.fixture(scope='session')
def app():
    """建立測試應用程式"""
    app = create_app('testing')
    return app

@pytest.fixture(scope='session')
def _db(app):
    """建立測試資料庫"""
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()

@pytest.fixture(scope='function')
def session(_db, app):
    """為每個測試函數提供乾淨的資料庫會話"""
    with app.app_context():
        connection = _db.engine.connect()
        transaction = connection.begin()
        
        # 綁定會話到連接
        options = dict(bind=connection, binds={})
        session = _db.create_scoped_session(options=options)
        _db.session = session
        
        yield session
        
        # 回滾並清理
        transaction.rollback()
        connection.close()
        session.remove()

@pytest.fixture
def client(app, session):
    """建立測試客戶端"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """建立 CLI 測試執行器"""
    return app.test_cli_runner()

@pytest.fixture
def test_employee(session):
    """建立測試員工"""
    employee = Employee(
        employee_code='EMP001',
        name='測試員工',
        email='test@example.com',
        phone='0912345678',
        department='HR',
        position='MANAGER',
        hire_date=date(2023, 1, 1),
        is_active=True
    )
    session.add(employee)
    session.commit()
    return employee

@pytest.fixture
def test_user(session, test_employee):
    """建立測試使用者"""
    user = User(
        employee_id=test_employee.id,
        username='testuser',
        is_active=True
    )
    user.set_password('password123')
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def auth_headers(client, test_user):
    """取得認證標頭"""
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}
