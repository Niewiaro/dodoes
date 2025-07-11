import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from ..database.core import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"User(id={self.id}, email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}', created_at='{self.created_at}', updated_at='{self.updated_at}')"

    def __str__(self):
        return f"User(email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}')"
