from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """使用者模型"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )

    def set_password(self, password):
        """設定密碼（加密）"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """驗證密碼"""
        return check_password_hash(self.password, password)

    def to_dict(self, include_sensitive=False):
        """轉換為字典（預設不包含敏感資訊）"""
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_sensitive:
            data["updated_at"] = (
                self.updated_at.isoformat() if self.updated_at else None
            )
        return data

    @classmethod
    def get_by_id(cls, user_id):
        """透過 ID 取得使用者"""
        return db.session.get(cls, user_id)

    @classmethod
    def get_by_email(cls, email):
        """透過 Email 取得使用者"""
        return cls.query.filter_by(email=email).first()

    def __repr__(self):
        return f"<User {self.email}>"
