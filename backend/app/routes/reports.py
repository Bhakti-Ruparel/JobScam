from fastapi import APIRouter


router = APIRouter() # ✅ THIS LINE WAS MISSING OR MISNAMED


@router.get("/")
def get_reports():
    return {"message": "Reports endpoint working"}