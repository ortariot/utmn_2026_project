from fastapi import APIRouter

router = APIRouter()


@router.get("/helth")
def health():
    return {"status": "ok"}