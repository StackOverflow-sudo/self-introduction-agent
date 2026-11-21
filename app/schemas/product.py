from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="产品名")
    premium: int = Field(..., ge=0, description="保费")
    desc: str = Field(default="", max_length=255, description="描述")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    premium: int | None = Field(default=None, ge=0)
    desc: str | None = None


class ProductOut(ProductBase):
    id: int

    model_config = {"from_attributes": True}   # 允许从 ORM 对象转成 Schema