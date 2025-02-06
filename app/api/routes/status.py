from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_status():
    return {"message": "Status route is working"}
