from sqlalchemy import Column, String
from models.base_model import BaseModel


class VerificationModel(BaseModel):
    __tablename__ = "verifications"

    email       = Column(String(255), nullable=False, index=True)
    value       = Column(String(20), nullable=False)
