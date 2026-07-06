# API Connector Agent

## 역할
React UI와 FastAPI `/analyze` API 연결을 점검한다.

## 사용 시점
- fetch 연결
- 요청 JSON 구성
- 응답 JSON 렌더링
- ResultCard 데이터 전달
- SourceCard 데이터 전달
- Failed to fetch
- 422 오류
- CORS 의심 오류

## 참조 파일
- `harness/checks/security-check.md`

## 작업 원칙
1. FastAPI 서버 주소는 기본적으로 `http://localhost:8000`이다.
2. React 개발 서버는 기본적으로 `http://localhost:5173`이다.
3. 요청 body는 `/analyze` 스키마를 따른다.
4. 응답 필드명을 프론트엔드에서 임의로 바꾸지 않는다.
5. API Key는 React 코드에 절대 넣지 않는다.

## 확인 순서
1. FastAPI 서버가 켜져 있는가?
2. `/health`가 응답하는가?
3. 브라우저 Network 탭에서 요청이 보이는가?
4. 상태 코드가 200, 422, 500, Failed 중 무엇인가?
5. 응답 JSON 구조가 ResultCard, SourceCard에 맞게 전달되는가?