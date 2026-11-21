from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def list(self) -> list[Product]:
        return self.db.query(Product).all()

    def create(self, data: ProductCreate) -> Product:
        obj = Product(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, product_id: int, data: ProductUpdate) -> Product | None:
        obj = self.get(product_id)
        if obj is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, product_id: int) -> bool:
        obj = self.get(product_id)
        if obj is None:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True