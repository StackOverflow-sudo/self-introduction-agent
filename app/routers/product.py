from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.services.product import ProductService

router = APIRouter(prefix="/api/products", tags=["products"])


def get_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)


@router.get("", response_model=list[ProductOut])
def list_products(svc: ProductService = Depends(get_service)):
    return svc.list()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, svc: ProductService = Depends(get_service)):
    obj = svc.get(product_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="product not found")
    return obj


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, svc: ProductService = Depends(get_service)):
    return svc.create(data)


@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, data: ProductUpdate, svc: ProductService = Depends(get_service)):
    obj = svc.update(product_id, data)
    if obj is None:
        raise HTTPException(status_code=404, detail="product not found")
    return obj


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, svc: ProductService = Depends(get_service)):
    if not svc.delete(product_id):
        raise HTTPException(status_code=404, detail="product not found")