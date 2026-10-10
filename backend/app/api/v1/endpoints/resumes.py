from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.schemas.resume import ResumeCreateRequest

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_resume(payload: ResumeCreateRequest) -> dict[str, str]:
    return {"message": "resume stored", "name": payload.file_name}


@router.get("")
def list_resumes() -> list[dict[str, str]]:
    return []


@router.put("", status_code=status.HTTP_200_OK)
def replace_resume(payload: ResumeCreateRequest) -> dict[str, str]:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no existing resume to replace")
