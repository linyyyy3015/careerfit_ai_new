# CareerFit AI

> 전자전기컴퓨터공학부 학생의 전공, 보유 스킬, 희망 직무를 분석해 맞춤형 기업·직무와 준비 방향을 추천하는 AI 커리어 코치

---

## 📌 프로젝트 소개

CareerFit AI는 사용자의 전공, 보유 기술, 관심 직무를 입력받아 채용공고의 요구 역량과 비교하고, 적합한 기업·직무와 보완하면 좋은 스킬을 안내하는 서비스입니다.

단순히 AI가 일반적인 조언을 생성하는 것이 아니라, `jobs.csv`에 저장된 채용공고 데이터를 전처리하고, ChromaDB 기반 RAG 검색을 통해 관련 공고를 찾은 뒤, 사용자의 보유 스킬과 공고의 필수·우대 역량을 비교합니다.

현재는 FastAPI 기반 백엔드, ChromaDB 검색, Gemini API, React + Vite 프론트엔드, Tailwind CSS 기반 UI를 연결해 사용자가 한 화면에서 분석 결과와 참고한 공고 출처를 확인할 수 있도록 구현했습니다.

> 실제 합격 확률을 예측하는 서비스가 아니라, 사용자의 보유 역량과 채용공고 요구사항을 비교해 직무 적합도와 준비 방향을 제안하는 서비스입니다.

---

## ✨ 주요 기능

- 서버 상태 확인 API 제공
- 전체 채용공고 목록 조회
- 특정 채용공고 상세 조회
- 전공·보유 기술·관심 직무 기반 커리어 분석
- CSV 기반 채용공고 데이터 관리
- 결측치와 중복 채용공고 제거
- 스킬 키워드 표준화
- 전처리 데이터 SQLite 저장 및 조회
- 채용공고의 RAG 검색용 자연어 문서 변환
- ChromaDB 기반 관련 공고 검색
- 사용자 보유 스킬과 공고 필수·우대 역량 비교
- Gemini API 기반 분석 결과 생성
- React UI에서 분석 결과 카드 표시
- 참고한 공고 출처 카드 표시
- 입력이 애매할 경우 바로 분석하지 않고 추가 질문 반환
- MOCK 모드를 이용한 API Key 없는 테스트
- Swagger UI 기반 API 테스트
- Docker 기반 백엔드 실행 및 Render 배포

---

## 🛠 기술 스택

| 영역 | 기술 |
|---|---|
| 백엔드 | Python 3.11, FastAPI |
| AI API | Gemini 2.5 Flash-Lite |
| 데이터 처리 | Pandas |
| 데이터 저장 | SQLite |
| RAG 검색 | ChromaDB |
| 프론트엔드 | React, Vite |
| 스타일링 | Tailwind CSS |
| 실행 환경 | Docker |
| 배포 | Render |

---

## 🏗 서비스 동작 흐름

```text
사용자 전공·스킬·희망 직무 입력
              ↓
React InputForm에서 /analyze API 요청
              ↓
FastAPI 백엔드에서 사용자 입력 수신
              ↓
입력값이 너무 애매한 경우 추가 질문 반환
              ↓
ChromaDB에서 관련 채용공고 검색
              ↓
사용자 보유 스킬과 공고 필수·우대 역량 비교
              ↓
Gemini API를 통해 분석 결과 생성
              ↓
React ResultCard에 AI 분석 결과 표시
              ↓
React SourceCard에 참고한 공고 출처 표시
```

---

## 🧠 RAG 구조

CareerFit AI는 RAG 구조를 활용해 AI 답변의 근거를 명확히 합니다.

```text
jobs.csv
  ↓
Pandas 전처리
  ↓
SQLite 저장
  ↓
RAG 문서 변환
  ↓
ChromaDB 저장
  ↓
사용자 입력 기반 관련 공고 검색
  ↓
Gemini API 답변 생성
  ↓
AI 분석 결과 + Sources 반환
```

RAG를 사용하지 않으면 AI가 실제 공고 데이터와 무관한 일반적인 조언을 생성할 수 있습니다.  
이 프로젝트는 관련 공고를 먼저 검색한 뒤, 그 결과를 AI 프롬프트에 함께 전달하여 분석 결과의 근거를 강화했습니다.

---

## 📁 프로젝트 구조

```text
careerfit_ai_new/
├── backend/
│   ├── main.py
│   ├── routers/
│   │   ├── analyze.py
│   │   ├── health.py
│   │   └── jobs.py
│   ├── services/
│   ├── data/
│   │   └── preprocess.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .dockerignore
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── lib/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── .env.example
│
├── docs/
│   ├── CHECKLIST.md
│   ├── EVAL_QUESTIONS.md
│   ├── PROJECT_PLAN.md
│   └── ...
│
├── README.md
└── .gitignore
```

---

## 🔐 환경변수 설정

실제 API Key는 GitHub에 올리지 않습니다.

로컬에서는 `backend/.env` 파일을 사용하고, Render 배포 환경에서는 Render의 Environment Variables에 직접 입력합니다.

### Backend `.env.example`

```env
GEMINI_API_KEY=your_gemini_api_key_here
MOCK_MODE=false
LLM_MODEL=gemini-2.5-flash-lite
FRONTEND_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Frontend `.env.example`

```env
VITE_API_BASE_URL=http://localhost:8000
```

Render 백엔드를 로컬 프론트엔드에서 사용할 경우 `frontend/.env.local`에 다음과 같이 설정합니다.

```env
VITE_API_BASE_URL=https://careerfit-ai-b46g.onrender.com
```

`.env`, `.env.local` 파일은 GitHub에 올리지 않습니다.

---

## 🚀 실행 방법

### 1. Backend 로컬 실행

```bash
cd backend
python -m venv venv
```

Windows 기준 가상환경 활성화:

```bash
venv\Scripts\activate
```

패키지 설치:

```bash
pip install -r requirements.txt
```

FastAPI 서버 실행:

```bash
uvicorn main:app --reload --port 8000
```

Health Check:

```text
http://localhost:8000/health
```

API 문서:

```text
http://localhost:8000/docs
```

---

### 2. Frontend 로컬 실행

```bash
cd frontend
npm install
npm run dev
```

접속 주소:

```text
http://localhost:5173
```

로컬 백엔드를 사용할 경우:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Render 백엔드를 사용할 경우:

```env
VITE_API_BASE_URL=https://careerfit-ai-b46g.onrender.com
```

---

### 3. Docker로 Backend 실행

프로젝트 최상위 폴더에서 실행합니다.

```bash
docker build -t careerfit-ai ./backend
```

```bash
docker run -p 8000:8000 --env-file backend/.env careerfit-ai
```

정상 실행 확인:

```text
http://localhost:8000/health
```

API 문서:

```text
http://localhost:8000/docs
```

---

## 🌐 배포

Backend는 Render Web Service를 통해 Docker 기반으로 배포했습니다.

### Backend Render URL

```text
https://careerfit-ai-b46g.onrender.com
```

### API 문서

```text
https://careerfit-ai-b46g.onrender.com/docs
```

### Render 환경변수

Render 백엔드 서비스에는 다음 환경변수를 설정합니다.

```env
GEMINI_API_KEY=your_real_gemini_api_key
MOCK_MODE=false
LLM_MODEL=gemini-2.5-flash-lite
FRONTEND_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

프론트엔드 배포 주소가 생기면 `FRONTEND_ORIGINS`에 해당 주소를 추가합니다.

---

## 🔌 주요 API

### GET `/health`

서버 상태 확인용 API입니다.

```json
{
  "status": "ok"
}
```

### GET `/jobs`

전체 채용공고 목록을 조회합니다.

### GET `/jobs/{job_id}`

특정 채용공고 상세 정보를 조회합니다.

### POST `/analyze`

사용자의 전공, 보유 스킬, 관심 직무를 바탕으로 커리어 분석 결과를 생성합니다.

요청 예시:

```json
{
  "major": "전자전기컴퓨터공학부",
  "skills": ["Python", "C", "전자회로", "SPICE"],
  "job_type": "반도체 회로 설계"
}
```

응답에는 AI 분석 결과와 RAG Sources가 함께 포함됩니다.

입력이 너무 애매한 경우에는 바로 분석하지 않고 추가 질문을 반환합니다.

예시 입력:

```json
{
  "major": "전자전기컴퓨터공학부",
  "skills": ["프로그래밍"],
  "job_type": "미정"
}
```

예상 응답:

```text
보유 스킬이 아직 구체적이지 않습니다. 프로그래밍 언어, 전공 과목, 실습 도구처럼 실제 역량을 입력해주세요.
예: Python, C, 전자회로, SPICE
```

---

## 📊 테스트 예시

### 1. 정상 분석 입력

```text
전공: 전자전기컴퓨터공학부
보유 스킬: Python, C, 전자회로, SPICE
관심 직무: 반도체 회로 설계
```

출력 예시:

```text
1. 현재 역량 평가
2. 추천 공고
3. 보완하면 좋은 역량
4. 종합 의견
```

RAG Sources 예시:

```text
Source 1. 미래소자연구소 — 반도체 소자·회로 시뮬레이션 엔지니어
Source 2. 한빛세미콘 — 아날로그 IC 설계 엔지니어
Source 3. 관련 공고 후보
```

AI는 관련 공고 후보를 RAG Sources로 참고하고, 그중 적합도가 높은 공고를 최종 추천합니다.

### 2. 애매한 입력 되묻기 데모

```text
전공: 전자전기컴퓨터공학부
보유 스킬: 프로그래밍
관심 직무: 미정
```

출력 예시:

```text
보유 스킬이 아직 구체적이지 않습니다. 프로그래밍 언어, 전공 과목, 실습 도구처럼 실제 역량을 입력해주세요.
예: Python, C, 전자회로, SPICE
```

---

## ✅ 검증한 내용

- FastAPI `/health` 정상 응답 확인
- FastAPI `/docs` 정상 접속 확인
- `/jobs` API 응답 확인
- `/analyze` API 응답 확인
- AI 분석 결과 출력 확인
- RAG Sources 출력 확인
- 애매한 입력에 대한 추가 질문 반환 확인
- React UI 결과 카드 출력 확인
- React UI 출처 카드 출력 확인
- Docker build 성공
- Docker run 후 `/health` 응답 확인
- Render 백엔드 배포 성공
- 로컬 React 프론트엔드에서 Render 백엔드 호출 성공
- `.env` 및 `.env.local` GitHub 미포함 확인

---

## 🔒 보안 관리

- 실제 Gemini API Key는 GitHub에 올리지 않습니다.
- `.env`는 로컬 실행용 파일입니다.
- `.env.example`은 예시 파일이며 실제 Key를 포함하지 않습니다.
- Render 배포 시 API Key는 Render Environment Variables에 입력합니다.
- 프론트엔드 코드에는 Gemini API Key를 절대 포함하지 않습니다.

---

## 🔮 향후 개선

- [ ] 이력서 PDF 업로드 후 자동 역량 추출
- [ ] 공모전 마감일 기반 추천 기능
- [ ] 사용자별 포트폴리오 프로젝트 추천 기능 강화
- [ ] RAG 검색 품질 평가 지표 추가
- [ ] 추천 공고와 보완 역량의 중복 제거 로직 개선
- [ ] 프론트엔드 Render 배포 자동화
- [ ] 실제 채용 플랫폼 데이터 연동

---

## 📝 개발 과정에서 어려웠던 점

가장 어려웠던 부분은 FastAPI 백엔드, ChromaDB 기반 RAG 검색, Gemini API, React 프론트엔드를 하나의 흐름으로 연결하는 과정이었습니다.

특히 Docker와 Render 배포 과정에서 환경변수와 API Key를 안전하게 관리하는 점이 중요했습니다.  
이를 해결하기 위해 실제 API Key는 `.env`와 Render Environment Variables에서만 관리하고, GitHub에는 `.env.example`만 올리도록 구성했습니다.

또한 프론트엔드가 로컬 백엔드와 Render 백엔드를 모두 사용할 수 있도록 `VITE_API_BASE_URL` 환경변수 기반으로 API 주소를 분리했습니다.

마지막 고도화 단계에서는 사용자가 “프로그래밍”, “미정”처럼 애매하게 입력했을 때 바로 분석을 생성하지 않고, 더 구체적인 입력을 요청하도록 개선했습니다. 이를 통해 부정확한 분석을 줄이고 사용자 경험을 높일 수 있었습니다.

---

## Developer

- Name: Dino
- Role: Backend / AI Service Development
- GitHub: @linyyyy3015