import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID

from ..database.core import Base


class Priority(enum.Enum):
    Normal = 0
    Low = 1
    Medium = 2
    High = 3
    Top = 4


class Todo(Base):
    __tablename__ = 'todos'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    description = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=True)
    starts_at = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, nullable=False, default=False)
    priority = Column(Enum(Priority), nullable=False, default=Priority.Medium)
    completed_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"Todo(id={self.id}, user_id={self.user_id}, description='{self.description}', " \
               f"due_date='{self.due_date}', starts_at='{self.starts_at}', is_completed={self.is_completed}, " \
               f"priority='{self.priority}', completed_at='{self.completed_at}', created_at='{self.created_at}', " \
               f"updated_at='{self.updated_at}')"

    def __str__(self):
        return f"Todo(description='{self.description}', due_date='{self.due_date}', " \
               f"starts_at='{self.starts_at}', is_completed={self.is_completed}, priority='{self.priority}')"

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "starts_at": self.starts_at.isoformat() if self.starts_at else None,
            "is_completed": self.is_completed,
            "priority": self.priority.name,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def from_dict(self, data: dict):
        self.id = uuid.UUID(data.get("id", str(uuid.uuid4())))
        self.user_id = uuid.UUID(data.get("user_id"))
        self.description = data.get("description")
        self.due_date = datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None
        self.starts_at = datetime.fromisoformat(data["starts_at"]) if data.get("starts_at") else None
        self.is_completed = data.get("is_completed", False)
        self.priority = Priority[data["priority"]] if "priority" in data else Priority.Medium
        self.completed_at = datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None
        return self
