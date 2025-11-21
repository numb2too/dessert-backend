from apiflask import APIBlueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.user import User
from app.schemas.auth import LoginInput, LoginOutput, RefreshOutput

auth_bp = APIBlueprint('auth', __name__)

@auth_bp.post('/login')
@auth_bp.input(LoginInput)
@auth_bp.output(LoginOutput, status_code=200)
def login(json_data):
    """使用者登入"""
    username = json_data['username']
    password = json_data['password']
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        abort(401, message='Invalid username or password')
    
    if not user.is_active:
        abort(403, message='Account is disabled')
    
    # 更新最後登入時間
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # 生成 Token
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'employee_id': user.employee_id,
            'employee_name': user.employee.name,
            'department': user.employee.department.value
        }
    }

@auth_bp.post('/refresh')
@jwt_required(refresh=True)
@auth_bp.output(RefreshOutput, status_code=200)
def refresh():
    """刷新 Token"""
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    
    return {
        'access_token': access_token
    }

@auth_bp.get('/me')
@jwt_required()
def get_current_user():
    """取得當前使用者資訊"""
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    
    return {
        'id': user.id,
        'username': user.username,
        'employee': {
            'id': user.employee.id,
            'name': user.employee.name,
            'email': user.employee.email,
            'department': user.employee.department.value,
            'position': user.employee.position.value
        }
    }