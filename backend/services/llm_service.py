# backend/services/llm_service.py
# RAG 연결 + LLM_MODEL 기반 provider 분기 + Ollama 통합 버전

import os
import re
import requests
from dotenv import load_dotenv


# =========================
# 1. 환경변수 로드
# =========================

load_dotenv()

MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash-lite")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


# =========================
# 2. LLM_MODEL → provider/model 분리
# =========================

def get_provider_and_model(model_name: str) -> tuple[str, str]:
    """
    LLM_MODEL 값을 보고 어떤 LLM provider를 사용할지 결정합니다.
    """

    if model_name.startswith("ollama:"):
        return "ollama", model_name.replace("ollama:", "", 1)

    if model_name.startswith("huggingface:"):
        return "huggingface", model_name.replace("huggingface:", "", 1)

    if model_name.startswith("mistral"):
        return "mistral", model_name

    return "gemini", model_name


PROVIDER, PROVIDER_MODEL = get_provider_and_model(LLM_MODEL)


# =========================
# 3. 시스템 지시문
# =========================

SYSTEM_INSTRUCTION = """
당신은 대학생을 위한 취업·공모전 전문 커리어 코치입니다.

반드시 지켜야 할 원칙:
- 답변은 자연스러운 한국어로 작성합니다.
- Python, SQL, Verilog, SPICE, TCAD, MATLAB, C/C++ 같은 기술명은 영어 표기를 허용합니다.
- 그 외 설명 문장은 영어 단어를 과하게 섞지 말고 한국어로 작성합니다.
- 실제 참고 데이터에 없는 회사명, 공고명, 조건, 공모전 정보는 만들지 않습니다.
- 공고를 "스킬을 배울 수 있는 기회"처럼 표현하지 않습니다.
- 공고는 사용자의 현재 역량과 비교할 기준 데이터로만 사용합니다.
- 입력한 보유 스킬은 이미 갖춘 역량으로 분류합니다.
- 입력하지 않은 스킬 중 참고 공고의 필수 스킬 또는 우대 스킬에 있는 것만 보완 역량으로 제시합니다.
- 사용자를 과도하게 평가하지 말고, 현재 입력한 전공과 스킬을 기준으로 실용적인 준비 방향을 제안합니다.
- 발표 화면에 바로 보여도 어색하지 않게 간결하고 명확하게 작성합니다.
- 마크다운 문법을 사용하지 않습니다. 별표, 샵, 백틱을 쓰지 않습니다.
""".strip()


# =========================
# 4. RAG 프롬프트 생성
# =========================

def build_rag_prompt(query: str, context_docs: list) -> str:
    """
    사용자 질문 + RAG 검색 문서 → LLM 프롬프트 구성
    """

    if context_docs:
        context_text = "\n\n".join(
            [
                f"""
[Source {i + 1}]
공고명: {doc.get("metadata", {}).get("title", "")}
회사명: {doc.get("metadata", {}).get("company", "")}
직무 유형: {doc.get("metadata", {}).get("job_type", "")}
필수 역량: {doc.get("metadata", {}).get("required_skills", "")}
우대 역량: {doc.get("metadata", {}).get("preferred_skills", "")}
공고 내용: {doc.get("text", "")}
유사도 거리: {doc.get("distance", "")}
""".strip()
                for i, doc in enumerate(context_docs)
            ]
        )

        context_section = f"""
[참고 데이터 — RAG 검색 결과]
{context_text}

위 참고 데이터는 프로젝트 내부 jobs.csv에서 검색된 공고입니다.
반드시 위 Source 데이터만 근거로 사용하세요.
회사명과 공고명은 Source에 있는 이름만 사용하세요.
검색된 데이터에 없는 회사명, 공고명, 조건, 공모전 정보는 절대 지어내지 마세요.
"""
    else:
        context_section = """
[참고 데이터 없음]
현재 검색된 공고 데이터가 없습니다.
제공된 자료만으로는 판단하기 어렵다고 말하고, 일반적인 준비 방향만 짧게 제안하세요.
"""

    return f"""
{SYSTEM_INSTRUCTION}

[사용자 정보]
{query}

{context_section}

[답변 형식]
아래 형식을 그대로 지켜서 작성하세요.
별표, 샵, 백틱 같은 마크다운 문법은 사용하지 마세요.

1. 현재 역량 평가:
- 입력된 전공과 보유 스킬이 관심 직무와 어떻게 연결되는지 2문장 이내로 설명하세요.
- 이미 보유한 스킬은 부족한 역량으로 다시 말하지 마세요.
- "부족하다"보다는 "보완하면 좋은 부분"처럼 부드럽게 표현하세요.

2. 추천 공고:
- 참고 데이터가 있으면 Source 1, Source 2 순서에 맞춰 관련 공고 1~2개를 추천하세요.
- 회사명과 공고명을 정확히 적으세요.
- 추천 이유는 보유 스킬과 공고 요구 역량이 어떻게 겹치는지 중심으로 설명하세요.
- 공고를 통해 스킬을 배울 수 있다고 말하지 마세요.
- 대신 이 공고가 현재 역량과 비교했을 때 어떤 준비가 필요한지 보여주는 기준이라고 설명하세요.

3. 보완하면 좋은 역량:
- 참고 공고의 필수 역량 또는 우대 역량 중 사용자가 입력하지 않은 항목만 고르세요.
- 3가지 이내로 작성하세요.
- 각 항목은 "필요한 이유"와 "준비 방향"을 짧게 제시하세요.
- 사용자가 이미 입력한 보유 스킬은 절대 다시 제시하지 마세요.

4. 종합 의견:
- 사용자의 현재 강점과 다음 준비 방향을 2문장 이내로 정리하세요.

[출력 규칙]
- 반드시 한국어로 답변하세요.
- 단, 기술명은 Python, SQL, Verilog, SPICE, TCAD, MATLAB, C/C++처럼 표기해도 됩니다.
- acquired, gain, opportunity, additional education, course, internship 같은 영어 단어를 섞지 마세요.
- "gân", "yetto", "l-course"처럼 깨진 표현을 절대 쓰지 마세요.
- 마크다운 굵게 표시인 **기호를 사용하지 마세요.
- 제목이나 항목명에 별표, 샵, 백틱 같은 마크다운 문법을 사용하지 마세요.
- 입력한 보유 스킬은 부족한 역량으로 다시 제시하지 마세요.
- 부족한 역량은 참고 공고의 필수 역량 또는 우대 역량 중 입력하지 않은 항목에서만 고르세요.
- 추천 공고는 참고 출처 순서와 일치하게 작성하세요.
- 가장 먼저 추천하는 공고는 Source 1에 해당하는 공고로 작성하세요.
- 공고를 "배울 수 있는 기회"라고 표현하지 마세요.
- 문장은 짧고 발표 화면에서 읽기 쉽게 작성하세요.
- 전체 답변은 700자에서 1000자 사이로 작성하세요.
- "공고를 통해 배울 수 있습니다"라는 표현을 사용하지 마세요.
- "배울 수 있는 기회"라는 표현을 사용하지 마세요.
- 사용자가 입력하지 않은 스킬을 보유 스킬이라고 말하지 마세요.
- 사용자와 겹치는 역량에 명시된 항목만 보유 스킬과 연결된다고 말하세요.
""".strip()


# =========================
# 5. sources 응답 생성
# =========================

def build_sources(context_docs: list) -> list:
    """
    RAG 검색 문서를 API 응답용 sources 형식으로 변환합니다.
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


# =========================
# 6. 답변 후처리
# =========================

def clean_answer(answer: str) -> str:
    """
    로컬 LLM이 간혹 섞는 어색한 표현과 마크다운 문법을 발표용으로 보정합니다.
    """

    if not answer:
        return "분석 결과가 없습니다."

    replacements = {
        "**": "",
        "`": "",
        "###": "",
        "##": "",
        "#": "",
        "acquired": "습득",
        "acquire": "습득",
        "gain": "쌓기",
        "gaining": "쌓기",
        "opportunity": "기회",
        "additional education": "추가 학습",
        "course": "강의",
        "internship": "인턴십",
        "l-course": "강의",
        "yetto": "",
        "gân": "관련",
        "배울 수면": "배우면",
        "배울 수 있는 기회가 있습니다": "준비가 필요한 항목입니다",
        "스킬을 배울 수 있습니다": "역량을 보완할 수 있습니다",
        "공고 또는 공모전": "추천 공고",
        "추천 공고 또는 공모전": "추천 공고",
        "공고를 통해": "해당 공고는",
        "배울 수 있습니다": "보완할 수 있습니다",
        "배울 수 있는 기회": "보완이 필요한 기준",
    }

    cleaned = answer

    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)

    # 공백 줄이기
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned.strip()


# =========================
# 7. Gemini 호출
# =========================

def call_gemini(prompt: str) -> str:
    """
    Gemini API를 호출합니다.
    """

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY가 .env에 없습니다.")

    import google.generativeai as genai

    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel(PROVIDER_MODEL)

    response = model.generate_content(prompt)

    return response.text


# =========================
# 8. Mistral 호출
# =========================

def call_mistral(prompt: str) -> str:
    """
    Mistral API를 호출합니다.
    """

    if not MISTRAL_API_KEY:
        raise ValueError("MISTRAL_API_KEY가 .env에 없습니다.")

    url = "https://api.mistral.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": PROVIDER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_INSTRUCTION,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.2,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]


# =========================
# 9. Ollama 호출
# =========================

def call_ollama(prompt: str) -> str:
    """
    Ollama 로컬 추론 서버를 호출합니다.
    """

    url = f"{OLLAMA_BASE_URL}/api/generate"

    payload = {
        "model": PROVIDER_MODEL,
        "prompt": prompt,
        "system": SYSTEM_INSTRUCTION,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 900,
        },
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]

    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Ollama 서버에 연결할 수 없습니다. "
            "`ollama serve` 또는 `ollama run llama3.2:3b`를 실행했는지 확인하세요."
        )

    except requests.exceptions.Timeout:
        raise TimeoutError(
            "Ollama 응답 시간이 초과되었습니다. "
            "더 작은 모델을 사용하거나 timeout 값을 늘려보세요."
        )


# =========================
# 10. HuggingFace 호출
# =========================

def call_huggingface(prompt: str) -> str:
    """
    HuggingFace InferenceClient를 호출합니다.
    """

    if not HUGGINGFACE_TOKEN:
        raise ValueError("HUGGINGFACE_TOKEN이 .env에 없습니다.")

    from huggingface_hub import InferenceClient

    client = InferenceClient(
        model=PROVIDER_MODEL,
        token=HUGGINGFACE_TOKEN,
    )

    response = client.chat_completion(
        messages=[
            {
                "role": "system",
                "content": SYSTEM_INSTRUCTION,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=900,
        temperature=0.2,
    )

    message = response.choices[0].message

    if hasattr(message, "content"):
        return message.content

    return message["content"]


# =========================
# 11. provider에 따라 실제 LLM 호출
# =========================

def call_llm(prompt: str) -> str:
    """
    PROVIDER 값에 따라 실제 호출할 LLM을 선택합니다.
    """

    if PROVIDER == "gemini":
        return call_gemini(prompt)

    if PROVIDER == "mistral":
        return call_mistral(prompt)

    if PROVIDER == "ollama":
        return call_ollama(prompt)

    if PROVIDER == "huggingface":
        return call_huggingface(prompt)

    raise ValueError(f"지원하지 않는 LLM provider입니다: {PROVIDER}")


# =========================
# 12. FastAPI 라우터에서 사용할 최종 함수
# =========================

def get_llm_response(query: str, context_docs: list) -> dict:
    """
    RAG 문서와 함께 LLM 응답을 생성합니다.
    """

    sources = build_sources(context_docs)

    if MOCK_MODE:
        return {
            "answer": (
                f"[MOCK 응답] 질문: '{query}', 참고 문서 수: {len(context_docs)}개. "
                f"현재 설정 모델: {LLM_MODEL}, provider: {PROVIDER}. "
                "MOCK_MODE=false 설정 시 실제 응답을 받습니다."
            ),
            "sources": sources,
        }

    try:
        prompt = build_rag_prompt(query, context_docs)

        answer = call_llm(prompt)
        answer = clean_answer(answer)

        return {
            "answer": answer,
            "sources": sources,
        }

    except Exception as e:
        error_msg = str(e)

        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return {
                "answer": (
                    "[API 한도 초과] 현재 선택된 LLM API 한도에 도달했습니다. "
                    ".env에서 MOCK_MODE=true로 전환하거나 "
                    "LLM_MODEL을 다른 모델로 바꿔보세요."
                ),
                "sources": sources,
            }

        if PROVIDER == "ollama" and (
            "Ollama 서버에 연결할 수 없습니다" in error_msg
            or "Connection" in error_msg
            or "Connection refused" in error_msg
            or "Max retries exceeded" in error_msg
        ):
            return {
                "answer": (
                    "[Ollama 연결 오류] Ollama 로컬 서버에 연결할 수 없습니다. "
                    "터미널에서 `ollama serve` 또는 `ollama run llama3.2:3b`를 실행했는지 확인하세요."
                ),
                "sources": sources,
            }

        if PROVIDER == "ollama" and "응답 시간이 초과" in error_msg:
            return {
                "answer": (
                    "[Ollama 시간 초과] 로컬 모델 응답이 너무 오래 걸립니다. "
                    "더 작은 모델을 사용하거나 잠시 후 다시 시도하세요."
                ),
                "sources": sources,
            }

        return {
            "answer": (
                f"[오류] 현재 모델: {LLM_MODEL}, provider: {PROVIDER}. "
                f"오류 내용: {error_msg}"
            ),
            "sources": sources,
        }