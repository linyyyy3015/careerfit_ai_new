# Security Check

## 확인 시점
모든 작업 전후에 확인한다.

## 체크 항목
1. React 코드에 `GEMINI_API_KEY`가 없는가?
2. React 코드에 API Key, 토큰, 비밀번호가 직접 들어가지 않았는가?
3. `.env` 값이 코드, 화면, README에 노출되지 않았는가?
4. `.env`가 GitHub에 올라가지 않도록 `.gitignore`에 포함되어 있는가?
5. API 호출은 프론트엔드가 Gemini에 직접 요청하지 않고 FastAPI를 통해 이루어지는가?

## 즉시 경고해야 하는 상황
- API Key가 코드에 직접 들어간 경우
- `.env` 파일이 GitHub에 올라간 경우
- React에서 Gemini API를 직접 호출하려는 경우
- 스크린샷이나 로그에 API Key가 보이는 경우

## 권장 메시지
API Key는 비법 소스 보관함인 `.env`에 넣고, React 화면이나 GitHub에는 절대 노출하지 않습니다.