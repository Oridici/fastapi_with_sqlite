import sqlalchemy.orm as _orm
from geopy.geocoders import Nominatim

import models as _models, schemas as _schemas, database as _database


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(db: _orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id).first()


def get_user_by_email(db: _orm.Session, email: str):
    return db.query(_models.User).filter(_models.User.email == email).first()


def get_users(db: _orm.Session, limit: int = 100):
    return db.query(_models.User).limit(limit).all()


def create_user(db: _orm.Session, user: _schemas.UserCreate):
    fake_hashed_password = user.password + "thisisnotsecure"
    db_user = _models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_addresses(db: _orm.Session, limit: int = 10):
    return db.query(_models.Address).limit(limit).all()


def create_address(db: _orm.Session, address: _schemas.AddressCreate, user_id: int):
    address_dict = {
        "address": address.dict().get('address'),
        "coordinates": get_address_coordinates(address.dict().get('address'))
    }
    address = _models.Address(**address_dict, owner_id=user_id)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def get_address(db: _orm.Session, address_id: int):
    return db.query(_models.Address).filter(_models.Address.id == address_id).first()


def delete_address(db: _orm.Session, address_id: int):
    db.query(_models.Address).filter(_models.Address.id == address_id).delete()
    db.commit()


def update_address(db: _orm.Session, address_id: int, address: _schemas.AddressCreate):
    db_address = get_address(db=db, address_id=address_id)
    db_address.address = address.address
    address_coordinates = get_address_coordinates(address.address)
    db_address.coordinates = address_coordinates
    db.commit()
    db.refresh(db_address)
    return db_address


def get_address_coordinates(address):
    geolocator = Nominatim(user_agent="test")
    location = geolocator.geocode(address)
    coordinates = ""
    if location:
        coordinates = "Latitude : "+str(location.raw.get("lat"))+", Longitude: "+str(location.raw.get("lon"))
    return coordinates