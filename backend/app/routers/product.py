from fastapi import APIRouter, status, HTTPException, Body, Query
from sqlmodel import select, delete
from typing import Annotated
from sqlalchemy import or_, func

from ..schemas.product import Product, ProductCreate, ProductPublic, ProductUpdate, ProductAi, ProductAiCreate, ProductAiPublic, ProductAiUpdate
from ..utils.dependencies import SessionDep, TokenDep


router = APIRouter(prefix='/products', tags=["Product"])


# region Product
@router.post("/", response_model=ProductPublic, status_code=status.HTTP_201_CREATED)
def create_product(product_create: ProductCreate, session: SessionDep, token: TokenDep):
    db_product = Product.model_validate(product_create)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@router.get('/search')
def search_products(session: SessionDep, user_id: TokenDep, query:str = ""):
    search_pattern = f"%{query}%"
    conditions = or_(
        Product.trade_name.ilike(search_pattern),
        Product.internal_name.ilike(search_pattern),
        Product.product_name.ilike(search_pattern),  # 不区分大小写的模糊匹配
        Product.product_name_cn.ilike(search_pattern)
    )
    stmt = select(
        Product.id,
        Product.internal_name,        
    ).where(conditions)

    results = session.exec(stmt).mappings().all()
    # 转换为字典格式
    return results



@router.get("/{product_id}", response_model=ProductPublic)
def get_product(product_id: int, session: SessionDep, token: TokenDep):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.get("/", response_model=list[ProductPublic])
def get_products(session: SessionDep, token: TokenDep):
    db_products = session.exec(select(Product)).all()
    return db_products


@router.patch('/{product_id}', response_model=ProductPublic)
def update_product(product_id: int, product_update: dict, session: SessionDep, token: TokenDep):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    # product_data = product_update.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(product_update)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, session: SessionDep, token: TokenDep):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(db_product)
    session.commit()
    return {"message": "Product deleted successfully"}


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, summary='delete a list of products through list[id]')
def delete_products(product_ids: Annotated[list[int], Body()], session: SessionDep, token: TokenDep):
    stmt = delete(Product).where(Product.id.in_(product_ids))
    session.exec(stmt)
    session.commit()
    return None

# endregion

# region Product Ai


@router.post('/{product_id}/ais', response_model=ProductAiPublic, status_code=status.HTTP_201_CREATED)
def create_product_ai(ai_create: ProductAiCreate, session: SessionDep, user_id: TokenDep):
    db_product_ai = ProductAi.model_validate(ai_create)
    session.add(db_product_ai)

    try:
        session.commit()
        session.refresh(db_product_ai)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return db_product_ai


@router.get('/{product_id}/ais')
def get_product_ais(product_id: int, session: SessionDep, user_id: TokenDep):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product.ais


@router.get('/ais/{ai_id}', response_model=ProductAiPublic)
def get_product_ai(ai_id: int, session: SessionDep, token: TokenDep):
    db_ai = session.get(ProductAi, ai_id)

    if not db_ai:
        raise HTTPException(status_code=404, detail="Ai not found")
    return db_ai


@router.get('/ais', response_model=list[ProductAiPublic])
def get_product_ais(session: SessionDep, token: TokenDep):
    db_ais = session.exec(select(ProductAi)).all()
    return db_ais


@router.patch('/{product_id}/ais/{ai_id}', response_model=ProductAiPublic)
def update_product_ai(ai_id: int, ai_update: dict, session: SessionDep, token: TokenDep):
    db_ai = session.get(ProductAi, ai_id)
    if not db_ai:
        raise HTTPException(status_code=404, detail="Ai not found")

    db_ai.sqlmodel_update(ai_update)
    session.add(db_ai)
    session.commit()
    session.refresh(db_ai)
    return db_ai


@router.delete("/{product_id}/ais/{ai_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_ai(ai_id: int, session: SessionDep, token: TokenDep):
    db_ai = session.get(ProductAi, ai_id)
    if not db_ai:
        raise HTTPException(status_code=404, detail="Ai not found")
    session.delete(db_ai)
    session.commit()
    return {"message": "Ai deleted successfully"}

# endregion
