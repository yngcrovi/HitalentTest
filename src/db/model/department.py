from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class DepartmentModel(Base):
    __tablename__ = "department"
    __table_args__ = (
        CheckConstraint("name <> ''", name="check_department_name_not_empty"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        Integer, 
        ForeignKey("department.id", ondelete="SET NULL"),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.now
    )

    # # Связь с родительским отделом
    # parent: Mapped[Optional["Department"]] = relationship(
    #     "Department", 
    #     remote_side=[id],
    #     back_populates="children"
    # )
    
    # # Связь с дочерними отделами
    # children: Mapped[List["Department"]] = relationship(
    #     "Department",
    #     back_populates="parent"
    # )