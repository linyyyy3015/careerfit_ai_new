from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from services.llm_service import get_llm_response


router = APIRouter()


# 요청 본문(Request Body) 모델
# 사용자가 서버에 보내는 데이터 형식
class AnalyzeRequest(BaseModel):
    major: str
    skills: List[str]
    job_type: str


# 응답 본문(Response Body) 모델
# 서버가 사용자에게 돌려주는 데이터 형식
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
    사용자의 전공·스킬·관심 직무를 기반으로
    취업·공모전 맞춤 분석을 제공합니다.

    현재는 llm_service의 MOCK 응답을 사용하며,
    이후 Gemini API와 RAG 응답으로 교체합니다.
    """

    # 사용자 입력을 하나의 질문 문장으로 구성
    query = (
        f"전공: {request.major}, "
        f"보유 스킬: {', '.join(request.skills)}, "
        f"관심 직무: {request.job_type}"
    )

    # llm_service 호출
    result = get_llm_response(
        query=query,
        context_docs=[],
    )

    return AnalyzeResponse(
        answer=result["answer"],
        sources=result["sources"],
    )