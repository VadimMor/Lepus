from sqlalchemy import Column, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
import uuid
import json
from server.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ip = Column(String, unique=True, nullable=False)

    alerts = relationship("Alert", back_populates="user")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    metrics = Column(Text, nullable=False)
    mse = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="pending")

    user = relationship("User", back_populates="alerts")

    def to_dict(self):
        return {
            "id": self.id,
            "ip": self.user.ip if self.user else None,
            "metrics": json.loads(self.metrics),
            "mse": self.mse,
            "status": self.status
        }
