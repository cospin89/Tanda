from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import relationship
from app.database import db

class Tanda(db.Model):
    __tablename__ = 'tandas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price_per_user = Column(Numeric(10, 2), nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)

    creator = relationship('User', backref='created_tandas')
    members = relationship('TandaMember', back_populates='tanda')

class TandaMember(db.Model):
    __tablename__ = 'tanda_members'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tanda_id = Column(Integer, ForeignKey('tandas.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    has_paid = Column(Boolean, default=False)

    tanda = relationship('Tanda', back_populates='members')
    user = relationship('User', backref='tanda_memberships')
