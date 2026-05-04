from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class Task(Base):

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="todo")
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_by: Mapped[str] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    assignee_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    workspace_id: Mapped[int] = mapped_column(Integer, ForeignKey("workspaces.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), 
                                                 default=lambda:datetime.now(timezone.utc), 
                                                 onupdate=lambda:datetime.now(timezone.utc))
    
    creator = relationship("User", back_populates="created_tasks", foreign_keys=[created_by])
    assignee = relationship("User", foreign_keys=[assignee_id], back_populates="assigned_tasks")
    workspace = relationship("Workspace", back_populates="tasks")
    documents = relationship("Document", back_populates="task")
