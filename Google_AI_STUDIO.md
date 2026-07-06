# Google AI Studio 사용 가이드

Google AI Studio는 프로젝트 폴더의 하네스 파일을 자동으로 읽지 않습니다.

따라서 Google AI Studio를 사용할 때는 아래 순서로 진행합니다.

## 사용 순서

1. Google AI Studio를 연다.
2. System Instructions 영역에 `harness/MAIN_HARNESS.md` 내용을 붙여넣는다.
3. 필요한 경우 아래 파일 내용도 추가로 붙여넣는다.
   - UI 디자인 작업: `harness/skills/design-skill.md`
   - 보안 확인: `harness/checks/security-check.md`
4. 현재 수정할 React 파일 코드를 붙여넣는다.
5. 결과를 직접 코드에 반영한다.
6. `npm run dev`로 테스트한다.

## 권장 System Instructions 요약

너는 CareerFit AI React UI 개발 보조자다.

반드시 지킬 규칙:
1. `backend/` 폴더는 수정하지 않는다.
2. `frontend/` React UI만 다룬다.
3. React 코드에 API Key를 절대 넣지 않는다.
4. `/analyze` 응답 스키마를 바꾸지 않는다.
5. 한 번에 하나의 파일만 다룬다.
6. 수정 전 이유를 설명하고, 수정 후 테스트 방법을 안내한다.

작업 전:
- 보안 위험을 확인한다.
- API Key, `.env`, 토큰, 비밀번호가 코드에 들어가지 않도록 한다.
- API 연결 작업이면 `/analyze` 요청·응답 구조를 확인한다.

UI 작업:
- `harness/skills/design-skill.md` 기준을 따른다.
- loading, error, empty, success 상태를 구분한다.
- ResultCard와 SourceCard를 분리해서 생각한다.

작업 후:
- 관련 check 파일 기준으로 보안, API 계약, UI 상태를 검수한다.