from fastapi import APIRouter, HTTPException
from models import Users
from schemas import Status, User_Pydantic, UserIn_Pydantic

router = APIRouter()


@router.get("/users", response_model=list[User_Pydantic])
async def get_users():
    pass


@router.post("/users", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    pass


@router.get("/user/{user_id}", response_model=User_Pydantic)
async def get_user(user_id: int):
    pass


@router.put("/user/{user_id}", response_model=User_Pydantic)
async def update_user(user_id: int, user: UserIn_Pydantic):
    pass


@router.delete("/user/{user_id}", response_model=Status)
async def delete_user(user_id: int):
    pass


@router.get("/404")
async def get_404():
    pass


@router.get("/422")
async def get_422():
    pass
