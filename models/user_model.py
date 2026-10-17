from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, SoftDelete
from models.role_model import RoleModel


class UserModel(SoftDelete, BaseModel):
    __tablename__ = "users"
    __hidden__    = ['password']

    role_id     = Column(Integer, ForeignKey('roles.id'), nullable=False)
    name        = Column(String(255), nullable=False)
    email       = Column(String(255), nullable=False, unique=True)
    phone       = Column(String(30), nullable=True)
    password    = Column(String(255), nullable=False)
    avatar      = Column(String(500), nullable=True)
    verified_at = Column(DateTime, nullable=True)

    role        = relationship(RoleModel)
