from fastapi import APIRouter


router = APIRouter()


@router.post("/login")
def login(username: str, password: str):
# dummy auth for now
    if username == "admin" and password == "admin":
        return {"token": "fake-jwt-token"}
    return {"error": "Invalid credentials"}