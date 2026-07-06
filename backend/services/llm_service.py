# backend/services/llm_service.py
# RAG 연결 + LLM_MODEL 기반 provider 분기 + Ollama 통합 버전

import os
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
# 3. RAG 프롬프트 생성
# =========================

def build_rag_prompt(query: str, context_docs: list) -> str:
    """
    사용자 질문 + RAG 검색 문서 → LLM 프롬프트 구성
    """

    if context_docs:
        context_text = "\n".join(
            [
                f"""
[공고 {i + 1}]
{doc.get("text", "")}

출처: {doc.get("metadata", {}).get("company", "")} — {doc.get("metadata", {}).get("title", "")}
필요 역량: {doc.get("metadata", {}).get("required_skills", "")}
유사도 거리: {doc.get("distance", "")}
""".strip()
                for i, doc in enumerate(context_docs)
            ]
        )

        context_section = f"""
[참고 데이터 — 실제 취업·공모전 공고]
{context_text}

위 데이터를 반드시 근거로 사용해 답변하세요.
답변에서 어떤 공고를 참고했는지 명시하세요.
검색된 데이터에 없는 회사명, 조건, 공모전 정보는 지어내지 마세요.
"""
    else:
        context_section = """
[참고 데이터 없음]
제공된 자료만으로는 판단하기 어렵습니다.
일반적인 커리어 조언만 간단히 제공하세요.
"""

    return f"""당신은 취업·공모전 전문 커리어 코치입니다.
다음 지원자 정보와 참고 데이터를 바탕으로 맞춤형 조언을 한국어로 제공하세요.

[지원자 정보]
{query}

{context_section}

[답변 형식]
1. 현재 역량 평가 (2문장 이내)
2. 추천 공고 또는 공모전 (1~2개, 이유 포함)
3. 부족한 역량 및 준비 방향 (3가지 이내)

[중요 규칙]
- 반드시 한국어로 답변하세요.
- 참고 데이터가 있으면 반드시 그 데이터를 근거로 답변하세요.
- 참고 데이터가 부족하면 "제공된 자료만으로는 판단하기 어렵습니다"라고 말하세요.
- 간결하고 실용적으로 작성하세요.
""".strip()


# =========================
# 4. sources 응답 생성
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
                "job_type": metadata.get("job_type", ""),
                "distance": doc.get("distance", 0),
            }
        )

    return sources


# =========================
# 5. Gemini 호출
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
# 6. Mistral 호출
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
                "role": "user",
                "content": prompt,
            }
        ],
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
# 7. Ollama 호출
# =========================

def call_ollama(prompt: str) -> str:
    """
    Ollama 로컬 추론 서버를 호출합니다.
    """

    url = f"{OLLAMA_BASE_URL}/api/generate"

    payload = {
        "model": PROVIDER_MODEL,
        "prompt": prompt,
        "stream": False,
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
# 8. HuggingFace 호출
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
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=700,
    )

    message = response.choices[0].message

    if hasattr(message, "content"):
        return message.content

    return message["content"]


# =========================
# 9. provider에 따라 실제 LLM 호출
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
# 10. FastAPI 라우터에서 사용할 최종 함수
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