from app.models.sales_production_rd import Customer

@pytest.fixture
def test_customer(session):
    """建立測試客戶"""
    customer = Customer(
        customer_code='CUST001',
        name='測試客戶',
        phone='0987654321',
        email='customer@example.com',
        is_vip=False
    )
    session.add(customer)
    session.commit()
    return customer

def test_create_customer(client, auth_headers):
    """測試新增客戶"""
    data = {
        'customer_code': 'CUST002',
        'name': '新客戶',
        'phone': '0912345678',
        'email': 'newcust@example.com'
    }
    response = client.post('/api/sales/customers', 
                          json=data, 
                          headers=auth_headers)
    assert response.status_code == 201
    assert response.json['customer_code'] == 'CUST002'

def test_get_customers(client, auth_headers, test_customer):
    """測試取得客戶列表"""
    response = client.get('/api/sales/customers', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) >= 1