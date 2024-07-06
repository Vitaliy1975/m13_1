from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel,ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse],description='No more than 10 requests per minute',dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user:User=Depends(auth_service.get_current_user)):
    tags = await repository_contacts.get_contacts(skip, limit,current_user,db)
    return tags


@router.get("/{tag_id}", response_model=ContactResponse,description='No more than 10 requests per minute',dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contact(tag_id: int, db: Session = Depends(get_db),current_user:User=Depends(auth_service.get_current_user)):
    tag = await repository_contacts.get_contact(tag_id,current_user,db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return tag


@router.post("/", response_model=ContactResponse,description='No more than 2 requests per minute',dependencies=[Depends(RateLimiter(times=2, seconds=60))])
async def create_contact(body: ContactModel,db: Session = Depends(get_db),current_user:User=Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body,db,current_user)


@router.put("/{tag_id}", response_model=ContactResponse,description='No more than 10 requests per minute',dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactModel, tag_id: int, db: Session = Depends(get_db),current_user:User=Depends(auth_service.get_current_user)):
    tag = await repository_contacts.update_contact(tag_id,body,db,current_user)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return tag


@router.delete("/{tag_id}", response_model=ContactResponse,description='No more than 10 requests per minute',dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_contact(tag_id: int, db: Session = Depends(get_db),current_user:User=Depends(auth_service.get_current_user)):
    tag = await repository_contacts.remove_contact(tag_id,db,current_user)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return tag


@router.get("/find/",response_model=List[ContactResponse],description='No more than 10 requests per minute',dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def find_contacts(first_name:str=None,last_name:str=None,email:str=None,db:Session=Depends(get_db),current_user:User=Depends(auth_service.get_current_user)):
    result=await repository_contacts.search_contacts(db,current_user,first_name,last_name,email)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Contact not found")
    return result


@router.get("/birthday/",response_model=List[ContactResponse],description='No more than 10 requests per minute',dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def birth_contacts(db:Session=Depends(get_db),current_user:User=Depends(auth_service.get_current_user)):
    result=await repository_contacts.birthdays(db,current_user)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Contact not found")
    return result