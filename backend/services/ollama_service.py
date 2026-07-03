import requests


def get_ollama_response(
    prompt: str,
    model: str = "llama3.2:3b",
) -> str:
    """
    Ollama 로컬 추론 서버에 요청을 보냅니다.

    Args:
        prompt: 로컬 LLM에 전달할 질문
        model: 사용할 Ollama 모델 이름

    Returns:
        Ollama가 생성한 응답 문자열
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=60,
        )

        response.raise_for_status()

        return response.json()["response"]

    except requests.exceptions.ConnectionError:
        return (
            "[오류] Ollama 서버에 연결할 수 없습니다. "
            "Ollama 앱 또는 ollama serve 명령으로 서버를 실행하세요."
        )

    except requests.exceptions.Timeout:
        return (
            "[오류] 응답 시간이 초과되었습니다. "
            "잠시 후 다시 시도하거나 더 작은 모델을 사용하세요."
        )

    except requests.exceptions.RequestException as error:
        return f"[오류] Ollama 요청에 실패했습니다: {error}"