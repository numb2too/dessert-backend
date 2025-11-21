def test_login_success(client, test_user):
    """測試登入成功"""
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json

def test_login_invalid_credentials(client, test_user):
    """測試登入失敗（錯誤密碼）"""
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401

def test_get_current_user(client, auth_headers):
    """測試取得當前使用者資訊"""
    response = client.get('/api/auth/me', headers=auth_headers)
    assert response.status_code == 200
    assert 'username' in response.json