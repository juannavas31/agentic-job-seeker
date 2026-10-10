from fastapi import APIRouter

from app.api.v1.endpoints.resumes import router as resumes_router

router = APIRouter()
router.include_router(resumes_router)


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
