# backend/routers/analyze.py

from typing import List, Union

from fastapi import APIRouter
from pydantic import BaseModel

from services.rag_service import search_documents


router = APIRouter()


class AnalyzeRequest(BaseModel):
    major: str
    skills: Union[List[str], str]
    job_type: str


class AnalyzeResponse(BaseModel):
    answer: str
    sources: List[dict]
    needs_clarification: bool = False


def split_skills(skills_text: str) -> List[str]:
    """
    콤마로 구분된 스킬 문자열을 리스트로 변환합니다.
    """
    if not skills_text:
        return []

    return [
        skill.strip()
        for skill in skills_text.split(",")
        if skill.strip()
    ]


def normalize_request_skills(skills: Union[List[str], str]) -> List[str]:
    """
    프론트엔드 또는 Swagger에서 skills가 문자열/리스트 어느 형태로 들어와도
    내부에서는 List[str] 형태로 통일합니다.
    """
    if isinstance(skills, str):
        return split_skills(skills)

    if isinstance(skills, list):
        normalized_skills = []

        for skill in skills:
            if not isinstance(skill, str):
                continue

            if "," in skill:
                normalized_skills.extend(split_skills(skill))
            elif skill.strip():
                normalized_skills.append(skill.strip())

        return normalized_skills

    return []


def normalize_skill(skill: str) -> str:
    """
    스킬 비교용 정규화 함수입니다.
    대소문자와 공백 차이를 줄입니다.
    """
    return skill.strip().lower().replace(" ", "")


def build_sources(context_docs: list) -> List[dict]:
    """
    RAG 검색 문서를 프론트엔드 SourceCard에서 사용할 sources 형식으로 변환합니다.
    """
    sources = []

    for doc in context_docs:
        metadata = doc.get("metadata", {})

        sources.append(
            {
                "company": metadata.get("company", ""),
                "title": metadata.get("title", ""),
                "required_skills": metadata.get("required_skills", ""),
                "preferred_skills": metadata.get("preferred_skills", ""),
                "job_type": metadata.get("job_type", ""),
                "distance": doc.get("distance", 0),
            }
        )

    return sources


def compare_skills(user_skills: List[str], source: dict) -> dict:
    """
    사용자 보유 스킬과 공고의 필수/우대 스킬을 비교합니다.
    """
    user_skill_set = {
        normalize_skill(skill)
        for skill in user_skills
    }

    required_skills = split_skills(source.get("required_skills", ""))
    preferred_skills = split_skills(source.get("preferred_skills", ""))

    all_job_skills = required_skills + preferred_skills

    matched_skills = [
        skill
        for skill in all_job_skills
        if normalize_skill(skill) in user_skill_set
    ]

    missing_skills = [
        skill
        for skill in all_job_skills
        if normalize_skill(skill) not in user_skill_set
    ]

    return {
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }


def make_prepare_message(skill: str) -> str:
    """
    보완 역량별 준비 방향을 자연스러운 문장으로 변환합니다.
    """
    messages = {
        "Python": "시뮬레이션 결과 정리, 데이터 처리, 자동화 스크립트 작성에 활용할 수 있습니다.",
        "TCAD": "반도체 소자 구조와 전기적 특성을 시뮬레이션하는 역량을 보완할 수 있습니다.",
        "MATLAB": "회로 및 소자 시뮬레이션 결과를 분석하고 시각화하는 데 활용할 수 있습니다.",
        "C/C++": "임베디드 제어, 검증 자동화, 하드웨어 연동 프로그램 작성에 도움이 됩니다.",
        "Cadence Virtuoso": "아날로그 IC 설계 흐름과 회로 검증 역량을 보여주는 포트폴리오에 활용할 수 있습니다.",
        "Layout 검증": "회로 설계 이후 실제 칩 구현 단계의 검증 흐름을 이해하는 데 필요합니다.",
        "SystemVerilog": "디지털 회로 검증과 테스트벤치 작성 역량을 강화할 수 있습니다.",
        "FPGA": "RTL 설계 결과를 하드웨어 수준에서 검증하는 프로젝트에 활용할 수 있습니다.",
        "논리합성": "Verilog 설계가 실제 회로로 변환되는 과정을 이해하는 데 필요합니다.",
        "Timing Analysis": "디지털 회로의 동작 속도와 안정성을 검증하는 데 중요합니다.",
        "PCB 이해": "회로 설계 결과를 실제 보드로 구현하고 검증하는 과정에 도움이 됩니다.",
        "OrCAD": "회로도 작성과 PCB 설계 흐름을 경험하는 데 활용할 수 있습니다.",
        "전력전자": "전력반도체와 전력변환 회로 설계 방향으로 확장할 때 도움이 됩니다.",
    }

    return messages.get(
        skill,
        f"{skill} 관련 기초 개념과 간단한 실습 프로젝트를 준비하면 직무 적합도를 높일 수 있습니다.",
    )


def build_clarification_message(
    major: str,
    user_skills: List[str],
    job_type: str,
) -> str | None:
    """
    사용자의 입력이 너무 짧거나 애매하면 바로 분석하지 않고 추가 질문을 반환합니다.
    """
    major = (major or "").strip()
    job_type = (job_type or "").strip()

    vague_job_words = {
        "개발",
        "취업",
        "회사",
        "엔지니어",
        "아무거나",
        "잘 모르겠음",
        "모르겠음",
        "아직 잘 모르겠음",
        "아직 모름",
        "몰라",
        "미정",
        "없음",
    }

    vague_skill_words = {
        "개발",
        "코딩",
        "프로그래밍",
        "열심히",
        "없음",
        "잘 모르겠음",
        "모르겠음",
        "아직 모름",
    }

    normalized_job_type = normalize_skill(job_type)
    normalized_vague_jobs = {
        normalize_skill(word)
        for word in vague_job_words
    }

    normalized_user_skills = {
        normalize_skill(skill)
        for skill in user_skills
    }

    normalized_vague_skills = {
        normalize_skill(word)
        for word in vague_skill_words
    }

    if len(major) < 2:
        return (
            "전공 정보가 부족합니다. "
            "예: 전자전기컴퓨터공학부, 통계학과, 컴퓨터공학과처럼 입력해주세요."
        )

    if not user_skills:
        return (
            "보유 스킬 정보가 부족합니다. "
            "예: Python, C, 전자회로, SPICE처럼 현재 가지고 있는 역량을 입력해주세요."
        )

    if normalized_user_skills and normalized_user_skills.issubset(normalized_vague_skills):
        return (
            "보유 스킬이 아직 구체적이지 않습니다. "
            "프로그래밍 언어, 전공 과목, 실습 도구처럼 실제 역량을 입력해주세요. "
            "예: Python, C, 전자회로, SPICE"
        )

    if len(job_type) < 2 or normalized_job_type in normalized_vague_jobs:
        return (
            "관심 직무가 아직 구체적이지 않습니다. "
            "웹 개발, 임베디드, 반도체 설계, 데이터 분석 중 어떤 방향에 더 관심이 있나요?"
        )

    return None


def build_deterministic_answer(
    major: str,
    user_skills: List[str],
    job_type: str,
    sources: List[dict],
) -> str:
    """
    발표용으로 안정적인 분석 결과를 생성합니다.
    LLM이 보유 스킬을 착각하거나 이상한 외국어를 섞는 문제를 막기 위해
    핵심 분석 문장은 백엔드에서 직접 생성합니다.
    """
    user_skills_text = ", ".join(user_skills) if user_skills else "입력한 보유 스킬"

    if not sources:
        return (
            "1. 현재 역량 평가:\n"
            f"{major} 전공과 {user_skills_text} 역량은 {job_type} 방향과 연결될 수 있습니다. "
            "다만 현재 검색된 참고 공고가 없어 구체적인 공고 기준 비교는 어렵습니다.\n\n"
            "2. 추천 공고:\n"
            "제공된 자료만으로는 특정 공고를 추천하기 어렵습니다.\n\n"
            "3. 보완하면 좋은 역량:\n"
            "- 관심 직무와 관련된 기초 프로젝트를 추가로 준비하는 것이 좋습니다.\n\n"
            "4. 종합 의견:\n"
            "현재 입력 정보만으로는 제한적인 분석이 가능하므로, 관심 직무와 관련된 스킬을 더 구체적으로 입력하면 더 정확한 추천이 가능합니다."
        )

    first_source = sources[0]
    first_comparison = compare_skills(user_skills, first_source)

    matched_main = first_comparison["matched_skills"]

    if matched_main:
        matched_text = (
            f"참고 공고와 일치하는 핵심 역량은 {', '.join(matched_main)}입니다."
        )
    else:
        matched_text = (
            "직접적으로 일치하는 스킬은 많지 않지만, 전공 기반 역량과 연결될 수 있습니다."
        )

    # 보완 역량은 상위 source들의 missing skill에서 중복 없이 3개만 선택
    missing_candidates = []
    seen_missing_skills = set()
    normalized_user_skill_set = {
        normalize_skill(skill)
        for skill in user_skills
    }

    for source in sources:
        comparison = compare_skills(user_skills, source)

        for skill in comparison["missing_skills"]:
            normalized = normalize_skill(skill)

            if normalized in normalized_user_skill_set:
                continue

            if normalized in seen_missing_skills:
                continue

            missing_candidates.append(skill)
            seen_missing_skills.add(normalized)

    top_missing = missing_candidates[:3]

    # 추천 공고는 최대 2개
    recommended_sources = sources[:2]

    recommendation_lines = []

    for index, source in enumerate(recommended_sources, start=1):
        comparison = compare_skills(user_skills, source)
        matched = comparison["matched_skills"]
        missing = comparison["missing_skills"][:3]

        matched_part = (
            f"보유한 {', '.join(matched)} 역량이 공고 요구 역량과 겹칩니다."
            if matched
            else "보유 역량과 직접적으로 겹치는 항목은 적지만, 전공 기반 지식과 연결됩니다."
        )

        missing_part = (
            f"추가로 {', '.join(missing)} 역량을 보완하면 더 적합해질 수 있습니다."
            if missing
            else "현재 입력한 역량과의 연결성이 높은 편입니다."
        )

        recommendation_lines.append(
            f"{index}. {source.get('company', '정보 없음')} — {source.get('title', '정보 없음')}\n"
            f"추천 이유: {matched_part} {missing_part}"
        )

    if top_missing:
        missing_lines = []

        for index, skill in enumerate(top_missing, start=1):
            missing_lines.append(
                f"{index}. {skill}\n"
                f"- 필요한 이유: 참고 공고에서 요구하거나 우대하는 역량입니다.\n"
                f"- 준비 방향: {make_prepare_message(skill)}"
            )

        missing_section = "\n\n".join(missing_lines)
    else:
        missing_section = (
            "현재 입력한 역량과 참고 공고의 요구 역량이 비교적 잘 맞습니다. "
            "다음 단계에서는 관련 프로젝트 경험을 정리하는 것이 좋습니다."
        )

    answer = f"""
1. 현재 역량 평가:
{major} 전공과 {user_skills_text} 역량은 {job_type} 직무와 연결됩니다. {matched_text}

2. 추천 공고:
{chr(10).join(recommendation_lines)}

3. 보완하면 좋은 역량:
{missing_section}

4. 종합 의견:
현재 강점은 {user_skills_text}입니다. 이 강점을 {job_type} 직무와 연결해 보여줄 수 있는 작은 프로젝트나 실습 경험을 추가하면 포트폴리오 설득력이 높아집니다.
""".strip()

    return answer


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    tags=["Analyze"],
)
def analyze_career(request: AnalyzeRequest):
    """
    RAG 기반 역량 분석:
    사용자 입력 → 입력 구체성 확인 → ChromaDB 검색 → 스킬 비교 → 발표용 분석 결과 생성 → sources 반환
    """

    user_skills = normalize_request_skills(request.skills)

    clarification_message = build_clarification_message(
        major=request.major,
        user_skills=user_skills,
        job_type=request.job_type,
    )

    if clarification_message:
        return AnalyzeResponse(
            answer=clarification_message,
            sources=[],
            needs_clarification=True,
        )

    skills_text = ", ".join(user_skills)

    search_query = (
        f"전공: {request.major}, "
        f"보유 스킬: {skills_text}, "
        f"관심 직무: {request.job_type}"
    )

    context_docs = search_documents(
        search_query,
        n_results=3,
        job_type=request.job_type,
    )

    if not context_docs:
        context_docs = search_documents(
            search_query,
            n_results=3,
            job_type=None,
        )

    sources = build_sources(context_docs)

    answer = build_deterministic_answer(
        major=request.major,
        user_skills=user_skills,
        job_type=request.job_type,
        sources=sources,
    )

    return AnalyzeResponse(
        answer=answer,
        sources=sources,
        needs_clarification=False,
    )