from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric
from app.database import db

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(120), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=True)
    password_hash = Column(String(256), nullable=False)
    balance = Column(Numeric(10, 2), default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    @property
    def password(self):
        """Prevent password from being accessed directly."""
        raise AttributeError("Password is not readable!")

    @password.setter
    def password(self, password):
        """Hash and store the password securely."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the hashed password."""
        return check_password_hash(self.password_hash, password)

    def deactivate(self):
        """Soft delete by deactivating the user."""
        self.is_active = False

    def __repr__(self):
        return f"<User {self.email}>"
