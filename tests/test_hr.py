def test_create_employee(client, auth_headers):
    """測試新增員工"""
    data = {
        'employee_code': 'EMP002',
        'name': '新員工',
        'email': 'new@example.com',
        'phone': '0923456789',
        'department': 'SALES',
        'position': 'STAFF',
        'hire_date': '2024-01-01',
        'is_active': True
    }
    response = client.post('/api/hr/employees', 
                          json=data, 
                          headers=auth_headers)
    assert response.status_code == 201
    assert response.json['employee_code'] == 'EMP002'

def test_get_employees(client, auth_headers, test_employee):
    """測試取得員工列表"""
    response = client.get('/api/hr/employees', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) >= 1

def test_get_employee_detail(client, auth_headers, test_employee):
    """測試取得員工詳情"""
    response = client.get(f'/api/hr/employees/{test_employee.id}', 
                         headers=auth_headers)
    assert response.status_code == 200
    assert response.json['name'] == '測試員工'