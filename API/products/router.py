from fastapi import APIRouter, Depends
from . import crud as c
from . import schemas as s
from users import models as um
from dependencies import getDB, isAdmin
from sqlalchemy.orm import Session
from typing import List
import uuid
from auth.crud import get_current_user

router = APIRouter()

@router.get("/list-all", response_model=List[s.ProductOut])
def list_all_products(db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        products = c.get_products(db)
        return products

@router.get("/list-active", response_model=List[s.ProductOut])
def list_active_products(db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        products = c.get_active_products(db)
        return products

@router.get("/list-inactive", response_model=List[s.ProductOut])
def list_inactive_products(db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        products = c.get_inactive_products(db)
        return products

@router.get(f"/list/{id}", response_model=s.ProductOut)
def list_one_group(id: uuid.UUID, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        products = c.get_product(id=id, db=db)
        return products

@router.post("/create", response_model=s.ProductOut)
def create_product(data: s.ProductCreate, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        product = c.create_product(db, data)
        return product

@router.put("/update", response_model=s.ProductOut)
def update_product(data: s.ProductUpdate, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        product = c.update_product(db, data)
        return product

@router.put(f"/deactivate/{id}", response_model=s.ProductOut)
def deactivate_product(id: uuid.UUID, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        product = c.deactivate_product(db=db, id=id)
        return product

@router.delete(f"/delete/{id}", response_model=s.ProductOut)
def delete_product(id: uuid.UUID, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        product = c.delete_product(db=db, id=id)
        return product
