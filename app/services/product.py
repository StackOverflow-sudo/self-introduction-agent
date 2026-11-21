from sqlalchemy.orm import Session

from app.repositories.product import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)

    def get(self, product_id: int):
        return self.repo.get(product_id)

    def list(self):
        return self.repo.list()

    def create(self, data: ProductCreate):
        return self.repo.create(data)

    def update(self, product_id: int, data: ProductUpdate):
        return self.repo.update(product_id, data)

    def delete(self, product_id: int):
        return self.repo.delete(product_id)