from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    premium: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    desc: Mapped[str] = mapped_column(String(255), nullable=False, default="")