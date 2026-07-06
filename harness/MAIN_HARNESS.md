# CareerFit AI Main Harness

## 목적
이 파일은 CareerFit AI 프로젝트에서 AI 도구가 일관된 기준으로 작업하도록 돕는 공통 운영 매뉴얼이다.

## 프로젝트 개요
- 프로젝트명: CareerFit AI
- 목적: 취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치
- 백엔드: Python, FastAPI
- AI API: Gemini 2.5 Flash-Lite
- 데이터: Pandas, SQLite, ChromaDB
- 프론트엔드: React, Vite, Tailwind CSS
- 실행 환경: Docker

## 핵심 작업 범위
React UI 실습에서는 기본적으로 `frontend/` 폴더 안에서만 작업한다.

주요 UI 파일:
- `frontend/src/App.jsx`
- `frontend/src/components/InputForm.jsx`
- `frontend/src/components/ResultCard.jsx`
- `frontend/src/components/SourceCard.jsx`

## 절대 규칙
1. React UI 작업에서는 `backend/` 폴더를 수정하지 않는다.
2. API Key를 React 코드에 넣지 않는다.
3. `.env` 값을 코드, 화면, README에 노출하지 않는다.
4. `/analyze` 요청·응답 스키마를 임의로 바꾸지 않는다.
5. 한 번에 하나의 파일, 하나의 작업만 다룬다.
6. 전체 기능을 한 번에 다시 작성하지 않는다.
7. 구현하지 않은 기능을 임의로 추가하지 않는다.
8. 수정 전에는 왜 이 수정이 필요한지 먼저 설명한다.
9. 수정 후에는 테스트 방법을 안내한다.
10. 학생이 설명할 수 없는 복잡한 구조를 남발하지 않는다.

## 작업 흐름
1. 사용자 요청을 읽고 작업 유형을 판단한다.
2. `harness/ROUTING.md`를 참고해 필요한 파일만 선택한다.
3. 작업 전 보안 위험을 확인한다.
4. 필요한 agent, skill, check 파일만 참조한다.
5. 작은 단위로 수정 방향을 제안한다.
6. 작업 후 관련 check 기준으로 검수한다.
7. 마지막에 학생이 직접 확인할 명령어 또는 화면 확인 방법을 안내한다.

## 기본 API 계약
React UI는 FastAPI의 `POST /analyze` 응답을 기준으로 화면을 구성한다.

요청 예시:
{
  "major": "통계학과",
  "skills": ["Python", "SQL"],
  "job_type": "데이터 분석"
}

응답 필드:
- answer
- matched_skills
- missing_skills
- recommended_projects
- sources
- confidence

## 응답 원칙
- 코드 전체를 새로 작성하기보다 수정 방향과 필요한 코드 조각을 제안한다.
- 오류 해결 시 원인 → 확인 순서 → 해결 방향 순서로 안내한다.
- 개념 설명 시 요리 비유를 활용한다.
- 보안 위반 가능성이 있으면 가장 먼저 경고한다.

## 토큰 절약 원칙
- 전체 프로젝트를 읽으려 하지 않는다.
- 관련 파일 1~2개만 사용한다.
- `ROUTING.md`를 통해 필요한 하네스 파일만 선택한다.
- 긴 답변보다 학생이 바로 실행할 수 있는 작은 단계로 안내한다.