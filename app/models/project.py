from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    summary: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    tech_stack: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    github: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    demo: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    bvid: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    cover: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
