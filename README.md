# CareerFit AI

> 취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치

---

## 프로젝트 개요

CareerFit AI는 사용자의 전공, 보유 기술, 관심 직무를 기반으로  
취업 공고와 공모전 데이터를 분석해 맞춤형 준비 방향을 제안하는 서비스입니다.

현재는 FastAPI 기반 백엔드와 목업 데이터를 활용해  
채용공고 조회 및 사용자 맞춤 분석 API를 구현한 상태입니다.

---

## 주요 기능

- 서버 상태 확인 API
- 채용공고 목록 및 상세 조회
- 사용자 전공·기술·관심 직무 기반 분석 요청
- Swagger UI를 활용한 API 테스트
- 환경변수를 활용한 API 키 관리

---

## 기술 스택

| 영역 | 기술 |
|---|---|
| 백엔드 | Python, FastAPI |
| API 문서 | Swagger UI |
| AI API | Gemini 2.5 Flash-Lite, Mistral AI |
| AI 라이브러리 | Hugging Face Transformers |
| 데이터 | Pandas, SQLite, ChromaDB |
| 프론트엔드 | React, Vite |
| 실행 환경 | Docker |
| 버전 관리 | Git, GitHub |

---

## 구현된 API

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/` | 서버 기본 응답 확인 |
| GET | `/health` | 서버 상태 확인 |
| GET | `/jobs` | 전체 채용공고 목록 조회 |
| GET | `/jobs/{job_id}` | 특정 채용공고 상세 조회 |
| POST | `/analyze` | 사용자 정보 기반 맞춤 분석 요청 |

---

## 현재 진행 현황

- [x] 1일차: 프로젝트 기획 및 개발 환경 세팅
- [x] 2일차: FastAPI 서버 및 기본 API 구현
- [ ] 3일차: 실제 CSV 기반 데이터 파이프라인 구축
- [ ] 4일차: RAG 기반 서비스 및 React UI 구현
- [ ] 5일차: Docker 적용 및 포트폴리오 완성

---

## 2일차 구현 내용

- FastAPI 서버와 CORS 설정을 구성했습니다.
- `/health`, `/jobs`, `/analyze` 엔드포인트를 구현했습니다.
- `/jobs`에서 실습용 채용공고 목업 데이터를 반환하도록 구성했습니다.
- `/analyze`에서 사용자 입력을 받는 요청·응답 구조와 목업 분석 기능을 구현했습니다.
- Gemini, Mistral, Hugging Face API 키와 mock mode 환경변수를 설정했습니다.

---

## 로컬 실행 방법

### 1. 백엔드 폴더로 이동

```bash
cd backend