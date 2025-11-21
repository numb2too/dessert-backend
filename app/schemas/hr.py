from apiflask import Schema
from apiflask.fields import String, Integer, Date, Decimal, Boolean, Nested, List
from apiflask.validators import Length, Range, OneOf

class EmployeeInput(Schema):
    employee_code = String(required=True, validate=Length(max=20))
    name = String(required=True, validate=Length(max=100))
    email = String(required=True, validate=Length(max=120))
    phone = String(validate=Length(max=20))
    department = String(required=True, validate=OneOf(['HR', 'FINANCE', 'SALES', 'PRODUCTION', 'RD']))
    position = String(required=True, validate=OneOf(['MANAGER', 'SUPERVISOR', 'STAFF', 'INTERN']))
    hire_date = Date(required=True)
    is_active = Boolean()

class EmployeeOutput(Schema):
    id = Integer()
    employee_code = String()
    name = String()
    email = String()
    phone = String()
    department = String()
    position = String()
    hire_date = Date()
    is_active = Boolean()
    created_at = String()

class EmployeeQuery(Schema):
    department = String(validate=OneOf(['HR', 'FINANCE', 'SALES', 'PRODUCTION', 'RD']))
    position = String(validate=OneOf(['MANAGER', 'SUPERVISOR', 'STAFF', 'INTERN']))
    is_active = Boolean()
    search = String()

class SalaryRecordInput(Schema):
    effective_date = Date(required=True)
    base_salary = Decimal(required=True)
    bonus = Decimal()
    deductions = Decimal()
    notes = String()

class SalaryRecordOutput(Schema):
    id = Integer()
    employee_id = Integer()
    effective_date = Date()
    base_salary = Decimal()
    bonus = Decimal()
    deductions = Decimal()
    notes = String()
    created_at = String()

class LeaveRecordInput(Schema):
    employee_id = Integer(required=True)
    leave_type = String(required=True, validate=OneOf(['ANNUAL', 'SICK', 'PERSONAL', 'MATERNITY', 'PATERNITY']))
    start_date = Date(required=True)
    end_date = Date(required=True)
    days = Decimal(required=True)
    reason = String()

class LeaveRecordOutput(Schema):
    id = Integer()
    employee_id = Integer()
    leave_type = String()
    start_date = Date()
    end_date = Date()
    days = Decimal()
    reason = String()
    status = String()
    approved_by = Integer()
    approved_at = String()

class LeaveRecordQuery(Schema):
    employee_id = Integer()
    status = String(validate=OneOf(['PENDING', 'APPROVED', 'REJECTED', 'CANCELLED']))
    start_date = Date()
    end_date = Date()

class PerformanceRecordInput(Schema):
    reviewer_id = Integer(required=True)
    review_date = Date(required=True)
    rating = Integer(required=True, validate=Range(min=1, max=5))
    strengths = String()
    improvements = String()
    goals = String()
    comments = String()

class PerformanceRecordOutput(Schema):
    id = Integer()
    employee_id = Integer()
    reviewer_id = Integer()
    review_date = Date()
    rating = Integer()
    strengths = String()
    improvements = String()
    goals = String()
    comments = String()
    created_at = String()