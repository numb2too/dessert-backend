from datetime import datetime
from app import db
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text, ForeignKey, Enum, Date, Boolean
from sqlalchemy.orm import relationship
import enum

class TimestampMixin:
    """時間戳混入類"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

# ==================== 人資模組 ====================
class DepartmentEnum(enum.Enum):
    """部門枚舉"""
    HR = "人資"
    FINANCE = "財務"
    SALES = "銷售"
    PRODUCTION = "生產"
    RD = "研發"

class PositionEnum(enum.Enum):
    """職位枚舉"""
    MANAGER = "經理"
    SUPERVISOR = "主管"
    STAFF = "員工"
    INTERN = "實習生"

class Employee(db.Model, TimestampMixin):
    """員工表"""
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    employee_code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20))
    department = Column(Enum(DepartmentEnum), nullable=False)
    position = Column(Enum(PositionEnum), nullable=False)
    hire_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # 關聯
    salary_records = relationship('SalaryRecord', back_populates='employee', cascade='all, delete-orphan')
    leave_records = relationship('LeaveRecord', back_populates='employee', cascade='all, delete-orphan')
    performance_records = relationship('PerformanceRecord', back_populates='employee', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Employee {self.employee_code}: {self.name}>'

class SalaryRecord(db.Model, TimestampMixin):
    """薪資紀錄表"""
    __tablename__ = 'salary_records'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    effective_date = Column(Date, nullable=False)
    base_salary = Column(Numeric(10, 2), nullable=False)
    bonus = Column(Numeric(10, 2), default=0)
    deductions = Column(Numeric(10, 2), default=0)
    notes = Column(Text)
    
    employee = relationship('Employee', back_populates='salary_records')
    
    def __repr__(self):
        return f'<SalaryRecord {self.employee_id}: {self.effective_date}>'

class LeaveTypeEnum(enum.Enum):
    """請假類型枚舉"""
    ANNUAL = "特休"
    SICK = "病假"
    PERSONAL = "事假"
    MATERNITY = "產假"
    PATERNITY = "陪產假"

class LeaveStatusEnum(enum.Enum):
    """請假狀態枚舉"""
    PENDING = "待審核"
    APPROVED = "已核准"
    REJECTED = "已拒絕"
    CANCELLED = "已取消"

class LeaveRecord(db.Model, TimestampMixin):
    """請假紀錄表"""
    __tablename__ = 'leave_records'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    leave_type = Column(Enum(LeaveTypeEnum), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    days = Column(Numeric(3, 1), nullable=False)
    reason = Column(Text)
    status = Column(Enum(LeaveStatusEnum), default=LeaveStatusEnum.PENDING, nullable=False)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approved_at = Column(DateTime)
    
    employee = relationship('Employee', back_populates='leave_records', foreign_keys=[employee_id])
    approver = relationship('Employee', foreign_keys=[approved_by])
    
    def __repr__(self):
        return f'<LeaveRecord {self.employee_id}: {self.start_date} to {self.end_date}>'

class PerformanceRecord(db.Model, TimestampMixin):
    """績效評論紀錄表"""
    __tablename__ = 'performance_records'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    review_date = Column(Date, nullable=False)
    reviewer_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5分
    strengths = Column(Text)
    improvements = Column(Text)
    goals = Column(Text)
    comments = Column(Text)
    
    employee = relationship('Employee', back_populates='performance_records', foreign_keys=[employee_id])
    reviewer = relationship('Employee', foreign_keys=[reviewer_id])
    
    def __repr__(self):
        return f'<PerformanceRecord {self.employee_id}: {self.review_date}>'