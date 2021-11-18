from uuid import uuid4, UUID
from fastapi import FastAPI, HTTPException
from models import Gender, User, Role, us
from typing import List

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("54857017-84f4-4f33-bf4b-245b6fc806fd"),
        first_name="scofield",
        last_name="idehen",
        gender=Gender.female,
        roles=[Role.student]
    ),
    User(
        id=UUID("77698ee3-e837-46e2-90fc-f7373960a4b8"),
        first_name="ken",
        last_name="ndubisi",
        gender=Gender.male,
        roles=[Role.student, Role.admin]
    )
]


@app.get("/")
async def root():
    return {"Hello": "scofield"}


@app.get("/api/v1/users")
async def fetch_users():
    return db;


@app.post("/api/v1/users")
async def register_users(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users")
async def delete_users(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return "delete"
    raise HTTPException(status_code=404,
                        detail=f"user with id: {user_id} does not exist"
                        )


@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: us, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name

            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exist"
    )
