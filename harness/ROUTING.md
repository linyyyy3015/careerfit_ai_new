# CareerFit AI Routing Guide

## 목적
사용자 요청을 보고 필요한 agent, skill, check 파일만 선택한다.

## 공통
모든 작업은 먼저 `harness/MAIN_HARNESS.md`의 절대 규칙을 따른다.

---

## 1. UI 디자인 개선

사용자 요청 예시:
- 화면을 더 예쁘게 만들고 싶어요.
- ResultCard를 발표용으로 개선하고 싶어요.
- SourceCard를 더 신뢰감 있게 보여주고 싶어요.
- loading/error 상태를 추가하고 싶어요.

참조 파일:
- `harness/agents/ui-designer.md`
- `harness/skills/design-skill.md`
- `harness/checks/security-check.md`

---

## 2. React 코드 리뷰

사용자 요청 예시:
- 이 코드가 맞는지 봐주세요.
- props 흐름이 이상한 것 같아요.
- useState를 잘 쓴 건가요?
- 조건 렌더링이 맞는지 확인해주세요.

참조 파일:
- `harness/agents/react-reviewer.md`
- `harness/checks/security-check.md`

---

## 3. API 연결

사용자 요청 예시:
- FastAPI와 React를 연결하고 싶어요.
- fetch가 안 돼요.
- /analyze 요청이 실패해요.
- 결과가 화면에 안 나와요.

참조 파일:
- `harness/agents/api-connector.md`
- `harness/checks/security-check.md`

---

## 4. RAG 결과 표시

사용자 요청 예시:
- sources를 카드로 보여주고 싶어요.
- confidence를 화면에 표시하고 싶어요.
- RAG 결과가 화면에 제대로 나오는지 보고 싶어요.

참조 파일:
- `harness/agents/api-connector.md`
- `harness/checks/security-check.md`

---

## 5. 오류 해결

사용자 요청 예시:
- 오류가 났어요.
- Failed to fetch가 나와요.
- CORS 오류가 나요.
- 화면이 빈 화면입니다.

참조 파일:
- 오류 종류에 따라 관련 agent 선택
- 공통으로 `harness/agents/ai-tutor-rules.md`
- 공통으로 `harness/checks/security-check.md`

---

## 6. 토큰 최적화

사용자 요청 예시:
- 프롬프트를 짧게 만들고 싶어요.
- AI가 너무 긴 답을 해요.
- 무료 API 한도를 아끼고 싶어요.

참조 파일:
- `harness/agents/token-optimizer.md`
- `harness/PROMPTS.md`