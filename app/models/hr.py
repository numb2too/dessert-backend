from app.extensions import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50))  # e.g., 'Chef', 'Sales', 'Manager'
    base_salary = db.Column(db.Float, default=0.0)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 關聯
    leave_records = db.relationship('LeaveRecord', backref='employee', lazy=True)
    reviews = db.relationship('PerformanceReview', backref='employee', lazy=True)

class LeaveRecord(db.Model):
    __tablename__ = 'leave_records'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(200))
    leave_type = db.Column(db.String(50)) # 病假/事假

class PerformanceReview(db.Model):
    __tablename__ = 'performance_reviews'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    rating = db.Column(db.Integer) # 1-5
    comments = db.Column(db.Text)
    review_date = db.Column(db.DateTime, default=datetime.utcnow)