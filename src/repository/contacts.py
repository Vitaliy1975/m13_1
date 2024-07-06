from typing import List
import datetime

from sqlalchemy.orm import Session

from src.database.models import Contact,User
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int,user:User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id==user.id).offset(skip).limit(limit).all()


async def get_contact(tag_id: int,user:User, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == tag_id,Contact.user_id==user.id).first()


async def create_contact(body: ContactModel, db: Session,user:User) -> Contact:
    tag = Contact(user_id=user.id,first_name=body.first_name,last_name=body.last_name,email=body.email,phone_number=body.phone_number,birthday=body.birthday,additional_data=body.additional_data)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


async def update_contact(tag_id: int, body: ContactModel, db: Session,user:User) -> Contact | None:
    tag = db.query(Contact).filter(Contact.id == tag_id,Contact.user_id==user.id).first()
    if tag:
        tag.first_name = body.first_name
        tag.last_name=body.last_name
        tag.email=body.email
        tag.phone_number=body.phone_number
        tag.birthday=body.birthday
        tag.additional_data=body.additional_data
        db.commit()
    return tag


async def remove_contact(tag_id: int, db: Session,user:User)  -> Contact | None:
    tag = db.query(Contact).filter(Contact.id == tag_id,Contact.user_id==user.id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag


async def search_contacts(db: Session,user:User, first_name: str = None, last_name: str = None, email: str = None):
    if first_name and last_name and email:
        return db.query(Contact).filter(Contact.first_name == first_name,Contact.last_name == last_name,Contact.email == email,Contact.user_id==user.id).all()
    elif first_name and last_name:
        return db.query(Contact).filter(Contact.first_name == first_name,Contact.last_name == last_name,Contact.user_id==user.id).all()
    elif last_name and email:
        return db.query(Contact).filter(Contact.last_name == last_name,Contact.email == email,Contact.user_id==user.id).all()
    elif first_name and email:
        return db.query(Contact).filter(Contact.first_name == first_name,Contact.email == email,Contact.user_id==user.id).all()
    elif first_name:
        return db.query(Contact).filter(Contact.first_name == first_name,Contact.user_id==user.id).all()
    elif last_name:
        return db.query(Contact).filter(Contact.last_name == last_name,Contact.user_id==user.id).all()
    elif email:
        return db.query(Contact).filter(Contact.email == email,Contact.user_id==user.id).all()
    return None


async def birthdays(db: Session,user:User):
        contacts=db.query(Contact).filter(Contact.user_id==user.id).all()
        congratulation_list=[]
        today_date=datetime.datetime.today().date()
        today_year=today_date.year
        today_year_string=str(today_year)
        for contact in contacts:
            birthday_noyear_string=(contact.birthday).strftime("%m.%d")
            birthday_this_year_string=today_year_string+"."+birthday_noyear_string
            birthday_this_year=datetime.datetime.strptime(birthday_this_year_string,"%Y.%m.%d").date()
            difference=birthday_this_year-today_date
            if difference.days<0:
                continue
            elif difference.days>7:
                continue
            else:
                congratulation_list.append(contact)
        return congratulation_list