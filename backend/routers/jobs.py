from typing import List

from fastapi import APIRouter, HTTPException


router = APIRouter()


# 목업 데이터: 3일차에 실제 CSV 데이터로 교체
MOCK_JOBS = [
    {
        "id": 1,
        "company": "네이버클라우드",
        "title": "AI 엔지니어",
        "required_skills": ["Python", "PyTorch", "머신러닝"],
        "preferred_skills": ["LLM", "RAG", "Docker"],
        "description": "생성형 AI 모델과 데이터 파이프라인을 개발하고, 실제 서비스에 적용할 수 있는 AI 기능을 구현합니다.",
        "deadline": "2026-08-31",
    },
    {
        "id": 2,
        "company": "현대오토에버",
        "title": "자율주행 소프트웨어 개발자",
        "required_skills": ["C++", "Python", "ROS2"],
        "preferred_skills": ["OpenCV", "Linux", "센서 융합"],
        "description": "카메라와 각종 차량 센서 데이터를 처리하고, 자율주행 판단 및 제어 소프트웨어를 개발합니다.",
        "deadline": "2026-08-31",
    },
    {
        "id": 3,
        "company": "한화시스템",
        "title": "임베디드 소프트웨어 엔지니어",
        "required_skills": ["C", "C++", "임베디드 시스템"],
        "preferred_skills": ["RTOS", "CAN 통신", "Git"],
        "description": "전자 장비에 탑재되는 임베디드 소프트웨어를 개발하고, 하드웨어 연동 및 통신 기능을 검증합니다.",
        "deadline": "2026-08-31",
    },
]

@router.get("/jobs", tags=["Jobs"])
def get_jobs():
    """
    취업 공고 목록을 반환합니다.

    현재는 목업 데이터를 반환하며,
    추후 실제 CSV 데이터로 교체합니다.
    """
    return {
        "count": len(MOCK_JOBS),
        "jobs": MOCK_JOBS,
    }


@router.get("/jobs/{job_id}", tags=["Jobs"])
def get_job_by_id(job_id: int):
    """
    특정 공고의 상세 정보를 반환합니다.
    """
    for job in MOCK_JOBS:
        if job["id"] == job_id:
            return job

    raise HTTPException(
        status_code=404,
        detail=f"공고 ID {job_id}를 찾을 수 없습니다.",
    )