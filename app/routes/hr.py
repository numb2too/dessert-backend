from apiflask import APIBlueprint, abort, pagination_builder
from flask_jwt_extended import jwt_required
from app import db
from app.models import Employee, SalaryRecord, LeaveRecord, PerformanceRecord
from app.schemas.hr import (
    EmployeeInput, EmployeeOutput, EmployeeQuery,
    SalaryRecordInput, SalaryRecordOutput,
    LeaveRecordInput, LeaveRecordOutput, LeaveRecordQuery,
    PerformanceRecordInput, PerformanceRecordOutput
)

hr_bp = APIBlueprint('hr', __name__, tag='人資管理')

# ==================== 員工管理 ====================
@hr_bp.get('/employees')
@jwt_required()
@hr_bp.input(EmployeeQuery, location='query')
@hr_bp.output(EmployeeOutput(many=True), status_code=200)
def get_employees(query_data):
    """取得員工列表"""
    query = Employee.query
    
    # 過濾條件
    if 'department' in query_data:
        query = query.filter_by(department=query_data['department'])
    if 'position' in query_data:
        query = query.filter_by(position=query_data['position'])
    if 'is_active' in query_data:
        query = query.filter_by(is_active=query_data['is_active'])
    if 'search' in query_data:
        search = f"%{query_data['search']}%"
        query = query.filter(
            db.or_(
                Employee.name.like(search),
                Employee.employee_code.like(search),
                Employee.email.like(search)
            )
        )
    
    # 排序
    query = query.order_by(Employee.created_at.desc())
    
    return query.all()

@hr_bp.get('/employees/<int:employee_id>')
@jwt_required()
@hr_bp.output(EmployeeOutput, status_code=200)
def get_employee(employee_id):
    """取得員工詳情"""
    employee = Employee.query.get_or_404(employee_id)
    return employee

@hr_bp.post('/employees')
@jwt_required()
@hr_bp.input(EmployeeInput)
@hr_bp.output(EmployeeOutput, status_code=201)
def create_employee(json_data):
    """新增員工"""
    # 檢查員工編號是否重複
    if Employee.query.filter_by(employee_code=json_data['employee_code']).first():
        abort(400, message='Employee code already exists')
    
    employee = Employee(**json_data)
    db.session.add(employee)
    db.session.commit()
    
    return employee

@hr_bp.patch('/employees/<int:employee_id>')
@jwt_required()
@hr_bp.input(EmployeeInput(partial=True))
@hr_bp.output(EmployeeOutput, status_code=200)
def update_employee(employee_id, json_data):
    """更新員工資料"""
    employee = Employee.query.get_or_404(employee_id)
    
    for key, value in json_data.items():
        setattr(employee, key, value)
    
    db.session.commit()
    return employee

@hr_bp.delete('/employees/<int:employee_id>')
@jwt_required()
@hr_bp.output({}, status_code=204)
def delete_employee(employee_id):
    """刪除員工"""
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return ''

# ==================== 薪資管理 ====================
@hr_bp.get('/employees/<int:employee_id>/salaries')
@jwt_required()
@hr_bp.output(SalaryRecordOutput(many=True), status_code=200)
def get_salary_records(employee_id):
    """取得員工薪資紀錄"""
    records = SalaryRecord.query.filter_by(employee_id=employee_id)\
        .order_by(SalaryRecord.effective_date.desc()).all()
    return records

@hr_bp.post('/employees/<int:employee_id>/salaries')
@jwt_required()
@hr_bp.input(SalaryRecordInput)
@hr_bp.output(SalaryRecordOutput, status_code=201)
def create_salary_record(employee_id, json_data):
    """新增薪資紀錄"""
    employee = Employee.query.get_or_404(employee_id)
    
    record = SalaryRecord(employee_id=employee_id, **json_data)
    db.session.add(record)
    db.session.commit()
    
    return record

# ==================== 請假管理 ====================
@hr_bp.get('/leave-records')
@jwt_required()
@hr_bp.input(LeaveRecordQuery, location='query')
@hr_bp.output(LeaveRecordOutput(many=True), status_code=200)
def get_leave_records(query_data):
    """取得請假紀錄"""
    query = LeaveRecord.query
    
    if 'employee_id' in query_data:
        query = query.filter_by(employee_id=query_data['employee_id'])
    if 'status' in query_data:
        query = query.filter_by(status=query_data['status'])
    if 'start_date' in query_data:
        query = query.filter(LeaveRecord.start_date >= query_data['start_date'])
    if 'end_date' in query_data:
        query = query.filter(LeaveRecord.end_date <= query_data['end_date'])
    
    query = query.order_by(LeaveRecord.start_date.desc())
    return query.all()

@hr_bp.post('/leave-records')
@jwt_required()
@hr_bp.input(LeaveRecordInput)
@hr_bp.output(LeaveRecordOutput, status_code=201)
def create_leave_record(json_data):
    """新增請假紀錄"""
    record = LeaveRecord(**json_data)
    db.session.add(record)
    db.session.commit()
    return record

@hr_bp.patch('/leave-records/<int:record_id>/approve')
@jwt_required()
def approve_leave(record_id):
    """核准請假"""
    from datetime import datetime
    from flask_jwt_extended import get_jwt_identity
    
    record = LeaveRecord.query.get_or_404(record_id)
    record.status = 'APPROVED'
    record.approved_by = get_jwt_identity()
    record.approved_at = datetime.utcnow()
    
    db.session.commit()
    return {'message': 'Leave approved successfully'}

# ==================== 績效管理 ====================
@hr_bp.get('/employees/<int:employee_id>/performance')
@jwt_required()
@hr_bp.output(PerformanceRecordOutput(many=True), status_code=200)
def get_performance_records(employee_id):
    """取得員工績效紀錄"""
    records = PerformanceRecord.query.filter_by(employee_id=employee_id)\
        .order_by(PerformanceRecord.review_date.desc()).all()
    return records

@hr_bp.post('/employees/<int:employee_id>/performance')
@jwt_required()
@hr_bp.input(PerformanceRecordInput)
@hr_bp.output(PerformanceRecordOutput, status_code=201)
def create_performance_record(employee_id, json_data):
    """新增績效評論"""
    record = PerformanceRecord(employee_id=employee_id, **json_data)
    db.session.add(record)
    db.session.commit()
    return record