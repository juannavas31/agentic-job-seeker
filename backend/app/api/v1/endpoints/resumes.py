from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.api.deps import get_resume_store
from app.exceptions import invalid_request
from app.schemas.resume import ResumeCreateRequest, ResumeResponse
from app.services.resume_service import ResumeStore

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(
    payload: ResumeCreateRequest,
    store: ResumeStore = Depends(get_resume_store),
) -> ResumeResponse:
    try:
        record = await store.create_resume(payload.file_name, payload.file_content)
    except ValueError as exc:
        raise invalid_request(str(exc)) from exc
    return ResumeResponse(name=record.name, content=record.content)


@router.get("", response_model=list[ResumeResponse])
async def list_resumes(store: ResumeStore = Depends(get_resume_store)) -> list[ResumeResponse]:
    records = await store.list_resumes()
    return [ResumeResponse(name=record.name, content=record.content) for record in records]


@router.put("", response_model=ResumeResponse, status_code=status.HTTP_200_OK)
async def replace_resume(
    payload: ResumeCreateRequest,
    store: ResumeStore = Depends(get_resume_store),
) -> ResumeResponse:
    try:
        record = await store.replace_resume(payload.file_name, payload.file_content)
    except ValueError as exc:
        raise invalid_request(str(exc)) from exc
    return ResumeResponse(name=record.name, content=record.content)
