from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_upload():
    return {"message": "Upload route is working"}
