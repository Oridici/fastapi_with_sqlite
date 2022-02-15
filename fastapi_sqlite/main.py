from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas

app = _fastapi.FastAPI()

_services.create_database()


@app.post("/users/", response_model=_schemas.User)
def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = _services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail="user already exists"
        )
    return _services.create_user(db=db, user=user)


@app.get("/users/", response_model=List[_schemas.User])
def read_users(
    limit: int = 10,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    users = _services.get_users(db=db, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=_schemas.User)
def read_user(user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="user does not exist"
        )
    return db_user


@app.post("/users/{user_id}/addresses/", response_model=_schemas.Address)
def create_address(
    user_id: int,
    address: _schemas.AddressCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="user does not exist"
        )
    return _services.create_address(db=db, address=address, user_id=user_id)


@app.get("/addresses/", response_model=List[_schemas.Address])
def read_addresses(
    limit: int = 10,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    addresses = _services.get_addresses(db=db, limit=limit)
    return addresses


@app.get("/addresses/{address_id}", response_model=_schemas.Address)
def read_address(address_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    address = _services.get_address(db=db, address_id=address_id)
    if address is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this address does not exist"
        )

    return address


@app.delete("/addresses/{address_id}")
def delete_address(address_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    _services.delete_address(db=db, address_id=address_id)
    return {"message": f"successfully deleted address with id: {address_id}"}


@app.put("/addresses/{address_id}", response_model=_schemas.Address)
def update_address(
    address_id: int,
    address: _schemas.AddressCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return _services.update_address(db=db, address=address, address_id=address_id)