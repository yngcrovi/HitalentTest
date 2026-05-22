from .base import Base
from datetime import datetime, date
from sqlalchemy import String, Integer, Date, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

class EmployeeModel(Base):
    __tablename__ = "employee"
    __table_args__ = (
        CheckConstraint("full_name <> ''", name="check_employee_full_name_not_empty"),
        CheckConstraint("position <> ''", name="check_employee_position_not_empty"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    department_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("department.id", ondelete="CASCADE"),
        nullable=False
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[str] = mapped_column(String(255), nullable=False)
    hired_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now
    )

    # # Связь с отделом (многие сотрудники → один отдел)
    # department: Mapped["Department"] = relationship("Department", back_populates="employees")