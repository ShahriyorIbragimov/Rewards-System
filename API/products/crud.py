from sqlalchemy.orm import Session
from . import schemas as s
from . import models as m
from fastapi import HTTPException, status
import uuid

def create_product(db: Session, data: s.ProductCreate):
    try:
        product = db.query(m.Products).filter(
            m.Products.name == data.name
        ).first()
        if product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product with this name already exists.",
            )
        product_data = data.model_dump()
        product = m.Users(**product_data)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def update_product(db: Session, data: s.ProductUpdate):
    try:
        product = db.query(m.Products).filter(m.Products.id == data.id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is not found."
            )
        for key, value in data.model_dump().items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

def get_products(db: Session):
    try:
        return db.query(m.Products).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def get_active_products(db: Session):
    try:
        return db.query(m.Products).filter(m.Products.is_active == True).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def get_inactive_products(db: Session):
    try:
        return db.query(m.Products).filter(m.Products.is_active == False).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def get_product(db: Session, id: uuid.UUID):
    try:
        product = db.query(m.Product).filter(m.Product.id == id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is not found."
            )
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def deactivate_product(db: Session, id: uuid.UUID):
    try:
        product = get_product(db=db, id=id)
        product.is_active = False
        db.commit()
        db.refresh(product)
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def delete_product(db: Session, id: uuid.UUID):
    try:
        product = get_product(db=db, id=id)
        db.delete(product)
        db.commit()
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
