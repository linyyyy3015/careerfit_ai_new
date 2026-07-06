# backend/routers/analyze.py

from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from services.llm_service import get_llm_response
from services.rag_service import search_documents


router = APIRouter()


class AnalyzeRequest(BaseModel):
    major: str
    skills: List[str]
    job_type: str


class AnalyzeResponse(BaseModel):
    answer: str
    sources: List[dict]


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    tags=["Analyze"],
)
def analyze_career(request: AnalyzeRequest):
    """
    RAG 기반 역량 분석:
    ChromaDB 검색 → Gemini 답변 → sources 반환
    """
    query = (
        f"전공: {request.major}, "
        f"보유 스킬: {', '.join(request.skills)}, "
        f"관심 직무: {request.job_type}"
    )

    context_docs = search_documents(
        query,
        n_results=3,
        job_type=request.job_type,
    )

    result = get_llm_response(
        query=query,
        context_docs=context_docs,
    )

    return AnalyzeResponse(
        answer=result["answer"],
        sources=result["sources"],
    )