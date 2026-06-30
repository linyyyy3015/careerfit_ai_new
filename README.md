# CareerFit AI

> 취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치

## 프로젝트 개요

취업을 준비하는 대학생은 수많은 채용 공고와 공모전 속에서 자신에게 맞는 기회를 찾고, 어떤 역량을 더 준비해야 하는지 판단하기 어렵다. CareerFit AI는 사용자의 전공, 보유 스킬, 관심 직무를 바탕으로 관련 데이터를 검색하고, 현재 역량과 필요한 역량을 비교해 취업 준비의 방향을 제시하는 AI 코치이다.

## 기술 스택

| 영역     | 기술                       |
| ------ | ------------------------ |
| 백엔드    | Python, FastAPI          |
| AI API | Gemini 2.5 Flash-Lite    |
| 데이터    | Pandas, SQLite, ChromaDB |
| 프론트엔드  | React, Vite              |
| 실행 환경  | Docker                   |

## 진행 현황

* [x] 1일차: 프로젝트 기획 및 개발 환경 세팅
* [x] 2일차: FastAPI 서버 구축 및 Gemini API 연결
* [ ] 3일차: 데이터 파이프라인 구축
* [ ] 4일차: RAG 기반 서비스 + React UI
* [ ] 5일차: Docker + 포트폴리오 완성

### 2일차 구현 내용

- FastAPI 서버와 CORS 설정을 구성했습니다.
- `/health`, `/jobs`, `/analyze` 엔드포인트를 구현했습니다.
- `/jobs`에서 실습용 채용공고 목업 데이터를 반환하도록 구성했습니다.
- `/analyze`에서 사용자 입력을 받는 요청·응답 구조와 목업 분석 기능을 구현했습니다.
- Gemini·Mistral·Hugging Face API 키와 mock mode 환경변수 설정을 추가했습니다.