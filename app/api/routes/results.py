from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_results():
    return {"message": "Results route is working"}
