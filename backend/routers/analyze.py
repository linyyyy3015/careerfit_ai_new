from typing import List

from fastapi import APIRouter
from pydantic import BaseModel


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

    현재는 목업 응답을 반환하며,
    이후 Gemini API와 RAG 응답으로 교체합니다.
    """

    mock_answer = (
        f"{request.major} 학생으로서 "
        f"{request.job_type} 직무에 지원하려면, "
        f"현재 보유하신 {', '.join(request.skills)} 역량을 바탕으로 "
        f"다음과 같은 준비를 추천드립니다. "
        f"(목업 응답 — 추후 Gemini로 교체)"
    )

    mock_sources = [
        {
            "title": "목업 데이터 — 테크스타트업A 데이터 분석가",
            "content": "요구 스킬: Python, SQL, 통계",
        }
    ]

    return AnalyzeResponse(
        answer=mock_answer,
        sources=mock_sources,
    )