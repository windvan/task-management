from sqlmodel import Field, Enum as dbEnum, Relationship

from ..database import SQLModel
from .enums import StageEnum


class ProductBase(SQLModel):
    internal_name: str
    lead_ai: str
    stage: StageEnum = Field(sa_column=dbEnum(StageEnum))
    a_number: str | None = None
    product_name: str | None = None
    product_name_cn: str | None = None
    trade_name: str | None = None
    product_origin: str | None = None
    # is_three_new: bool = False



class ProductCreate(ProductBase):
    pass


class ProductPublic(ProductBase):
    id: int


class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    ais: list['ProductAi'] = Relationship(back_populates='product')


class ProductUpdate(SQLModel):
    a_number: str | None = None
    lead_ai: str | None = None
    product_name: str | None = None
    product_name_cn: str | None = None
    trade_name: str | None = None
    internal_name: str | None = None
    product_origin: str | None = None
    # is_three_new: bool | None = None
    stage: StageEnum | None = None


class ProductAiBase(SQLModel):
    product_id: int = Field(foreign_key='product.id')
    abbreviation: str | None = None
    common_name: str
    common_name_cn: str | None = None
    design_code: str | None = None


class ProductAiCreate(ProductAiBase):
    pass


class ProductAiPublic(ProductAiBase):
    id: int


class ProductAiUpdate(SQLModel):
    product_id: int | None = None
    abbreviation: str | None = None
    common_name: str | None = None
    common_name_cn: str | None = None
    design_code: str | None = None


class ProductAi(ProductAiBase, table=True):
    __tablename__ = 'product_ai'
    id: int | None = Field(default=None, primary_key=True)

    product: Product = Relationship(back_populates="ais")
