from sqlalchemy import Column, String
from models.base_model import BaseModel, SoftDelete


class RoleModel(SoftDelete, BaseModel):
    __tablename__ = "roles"

    name        = Column(String(50), nullable=False)
