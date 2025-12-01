from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.supabase import supabase

router = APIRouter()

class UserCredentials(BaseModel):
    email: str
    password: str
    name: str = None

@router.post("/register")
def register(user: UserCredentials):
    try:
        # Supabase Auth Sign Up
        res = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "name": user.name
                }
            }
        })
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(user: UserCredentials):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
