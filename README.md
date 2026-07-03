# CareerFit AI

> 전자전기컴퓨터공학부 학생의 스펙과 희망 직무를 분석해 맞춤형 기업과 준비 방향을 추천하는 AI 커리어 코치

## 프로젝트 소개

CareerFit AI는 사용자의 전공, 보유 기술, 프로젝트 경험과 희망 직무를 입력받아 채용공고의 요구 역량과 비교하고, 적합한 기업·직무와 부족한 스킬을 안내하는 서비스입니다.

현재 FastAPI 기반 백엔드와 Gemini API를 이용한 맞춤형 분석 기능을 구현했으며, 채용공고 CSV 데이터를 전처리해 SQLite 데이터베이스와 RAG 검색용 문서로 변환하고 있습니다.

최종적으로는 다음 정보를 한 화면에서 제공하는 것을 목표로 합니다.

- 사용자 스펙과 잘 맞는 기업·직무 추천
- 기업별 직무 적합도 및 추천 이유
- 현재 부족한 기술과 경험 분석
- 부족한 역량을 보완하기 위한 학습·프로젝트 방향
- 기업 위치, 연봉, 규모, 주요 업무 등의 상세 정보

> 실제 합격 확률을 예측하는 것이 아니라, 사용자의 보유 역량과 채용공고 요구사항을 비교한 직무 적합도를 제공합니다.

---

## 주요 기능

- 서버 상태 확인
- 전체 채용공고 목록 조회
- 특정 채용공고 상세 조회
- 전공·보유 기술·관심 직무 기반 커리어 분석
- Gemini API 기반 맞춤형 답변 생성
- MOCK 모드를 이용한 API 키 없는 테스트
- Ollama 기반 로컬 LLM 호출 모듈
- CSV 기반 채용공고 및 공모전 데이터 관리
- 결측치와 중복 채용공고 제거
- 스킬 키워드 표준화
- 전처리 데이터 SQLite 저장 및 조회
- 채용공고의 RAG 검색용 자연어 문서 변환
- Swagger UI 기반 API 테스트

---

## 서비스 동작 흐름

```text
사용자 전공·스킬·희망 직무 입력
              ↓
관련 채용공고 데이터 검색
              ↓
사용자 역량과 필수·우대 스킬 비교
              ↓
적합한 기업·직무 및 부족한 역량 분석
              ↓
Gemini 또는 로컬 LLM을 통한 맞춤형 설명 생성
```

---

## 기술 스택

| 영역 | 기술 |
|---|---|
| 백엔드 | Python, FastAPI |
| 외부 AI API | Gemini 2.5 Flash-Lite |
| 로컬 LLM | Ollama, Llama 3.2 3B |
| 데이터 전처리 | Pandas |
| 데이터 저장 | CSV, SQLite |
| RAG 데이터 | JSON |
| API 문서 | Swagger UI |
| 버전 관리 | Git, GitHub |
| 확장 예정 | ChromaDB, React, Vite, Docker |

---

## 프로젝트 구조

```text
careerfit_ai_new
├─ .cursor
│  └─ rules
│     └─ project-rules.mdc
├─ backend
│  ├─ data
│  │  ├─ jobs.csv
│  │  ├─ competitions.csv
│  │  ├─ preprocess.py
│  │  ├─ careerfit.db
│  │  └─ rag_documents.json
│  ├─ routers
│  │  ├─ analyze.py
│  │  └─ jobs.py
│  ├─ services
│  │  ├─ __init__.py
│  │  ├─ llm_service.py
│  │  └─ ollama_service.py
│  ├─ main.py
│  ├─ requirements.txt
│  └─ .env
├─ .env.example
├─ .gitignore
└─ README.md
```

- `careerfit.db`와 `rag_documents.json`은 전처리 코드 실행 시 생성됩니다.
- 실제 API 키가 포함된 `backend/.env`와 가상환경 폴더 `backend/venv`는 GitHub에 업로드하지 않습니다.

---

# 로컬 실행 방법

## 1. 사전 요구사항

다음 프로그램이 설치되어 있어야 합니다.

- Python 3.10 이상
- Git
- Cursor 또는 Visual Studio Code
- Ollama는 로컬 LLM을 사용할 경우에만 필요

설치 여부 확인:

```bash
python --version
git --version
```

---

## 2. 프로젝트 복제

```bash
git clone <REPOSITORY_URL>
cd careerfit_ai_new
```

`<REPOSITORY_URL>`에는 실제 GitHub 저장소 주소를 입력합니다.

이미 프로젝트를 내려받았다면 이 단계는 생략합니다.

---

## 3. 백엔드 폴더 이동

```bash
cd backend
```

이후 백엔드 관련 명령어는 `backend` 폴더에서 실행합니다.

---

## 4. 가상환경 생성

### Windows PowerShell

```powershell
python -m venv venv
```

### macOS / Linux

```bash
python3 -m venv venv
```

---

## 5. 가상환경 활성화

### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
venv\Scripts\activate.bat
```

### macOS / Linux

```bash
source venv/bin/activate
```

정상적으로 활성화되면 터미널 앞에 `(venv)`가 표시됩니다.

```text
(venv) PS C:\...\careerfit_ai_new\backend>
```

PowerShell에서 실행 정책 오류가 발생하면 다음 명령어를 먼저 실행합니다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```

---

## 6. 필수 패키지 설치

```bash
python -m pip install -r requirements.txt
```

Pandas 설치 확인:

```bash
python -c "import pandas as pd; print('pandas:', pd.__version__)"
```

Gemini 라이브러리 설치 확인:

```bash
python -c "import google.generativeai as genai; print('Gemini SDK:', genai.__version__)"
```

---

## 7. 환경변수 파일 생성

프로젝트 최상위의 `.env.example`을 복사해 `backend/.env` 파일을 생성합니다.

현재 터미널이 `backend` 폴더인 경우:

### Windows PowerShell

```powershell
Copy-Item ..\.env.example .env
```

### macOS / Linux

```bash
cp ../.env.example .env
```

생성된 `backend/.env`를 열고 환경변수를 설정합니다.

### Gemini API 사용

```env
MOCK_MODE=false
GEMINI_API_KEY=본인의_GEMINI_API_KEY
LLM_MODEL=gemini-2.5-flash-lite
```

### API 키 없이 테스트

```env
MOCK_MODE=true
GEMINI_API_KEY=
LLM_MODEL=gemini-2.5-flash-lite
```

`MOCK_MODE=true`이면 Gemini API를 호출하지 않고 테스트용 응답을 반환합니다.

> 실제 Gemini API 키가 포함된 `.env` 파일은 GitHub에 업로드하지 않습니다.

---

## 8. 서버 실행

가상환경이 활성화된 `backend` 터미널에서 실행합니다.

```bash
uvicorn main:app --reload --port 8000
```

정상 실행 문구:

```text
Uvicorn running on http://127.0.0.1:8000
```

서버를 종료하려면 터미널에서 `Ctrl + C`를 누릅니다.

---

# 실행 확인

## 1. 서버 상태 확인

브라우저에서 다음 주소에 접속합니다.

```text
http://localhost:8000/health
```

정상 응답:

```json
{
  "status": "ok"
}
```

---

## 2. Swagger UI 확인

```text
http://localhost:8000/docs
```

Swagger UI에서 각 API를 직접 실행할 수 있습니다.

---

## 3. 분석 API 테스트

Swagger UI에서 `POST /analyze`를 선택하고 `Try it out`을 누른 뒤 다음 데이터를 입력합니다.

```json
{
  "major": "전자전기컴퓨터공학부",
  "skills": [
    "전자회로",
    "Python",
    "SPICE"
  ],
  "job_type": "반도체 회로 설계"
}
```

`Execute`를 누른 뒤 응답 코드가 `200`이고 `answer`에 맞춤형 커리어 조언이 포함되면 정상입니다.

예상 응답 구조:

```json
{
  "answer": "사용자 정보에 기반한 분석 결과",
  "sources": []
}
```

현재 ChromaDB 검색 연결 전에는 `sources`가 빈 배열로 표시될 수 있습니다.

---

## 구현된 API

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/` | 서버 기본 응답 확인 |
| GET | `/health` | 서버 상태 확인 |
| GET | `/jobs` | 전체 채용공고 목록 조회 |
| GET | `/jobs/{job_id}` | 특정 채용공고 상세 조회 |
| POST | `/analyze` | 사용자 정보 기반 맞춤 분석 |
| GET | `/docs` | Swagger API 문서 |

---

# 데이터 전처리

## 전처리 기능

`backend/data/preprocess.py`는 채용공고 데이터를 AI 검색에 활용할 수 있도록 다음 순서로 처리합니다.

```text
jobs.csv 불러오기
→ 결측치 확인
→ 핵심 정보가 없는 행 제거
→ 중복 채용공고 제거
→ 스킬 키워드 표준화
→ SQLite 저장
→ SQLite 조회 테스트
→ RAG 문서 변환
→ JSON 파일 저장
```

구현된 처리 기능:

- UTF-8 및 CP949 CSV 인코딩 처리
- 결측치 수와 비율 확인
- `title`, `required_skills` 결측 행 제거
- `company + title` 기준 중복 제거
- Python, SQL 등 스킬 표기 통일
- SQLite `jobs` 테이블 저장
- 직무 분류별 공고 수 조회
- Python 필수 공고 조회
- RAG 검색용 자연어 문서 생성
- 문서별 메타데이터 및 고유 ID 생성

---

## 전처리 실행

가상환경이 활성화된 `backend` 폴더에서 실행합니다.

```bash
python data/preprocess.py
```

현재 기본 데이터에서는 다음 결과가 생성됩니다.

```text
원본 채용공고: 18행
결측치 행 제거: 2행
중복 공고 제거: 1행
최종 채용공고: 15행
RAG 문서: 15개
```

실행 후 다음 파일이 생성됩니다.

```text
backend/data/careerfit.db
backend/data/rag_documents.json
```

---

## SQLite 저장 결과

전처리된 채용공고는 `careerfit.db`의 `jobs` 테이블에 저장됩니다.

저장 결과 확인:

```bash
python -c "import sqlite3; conn=sqlite3.connect('data/careerfit.db'); cursor=conn.cursor(); cursor.execute('SELECT COUNT(*) FROM jobs'); print(cursor.fetchone()[0]); conn.close()"
```

정상 결과:

```text
15
```

---

## RAG 문서 구조

각 채용공고는 다음 구조의 문서로 변환됩니다.

```json
{
  "text": "테크스타트업A에서 데이터 분석가를 채용합니다. 필수 스킬은 Python, SQL, 통계입니다.",
  "metadata": {
    "id": "1",
    "company": "테크스타트업A",
    "title": "데이터 분석가",
    "job_type": "데이터 분석",
    "deadline": "2026-08-31",
    "source": "jobs.csv"
  },
  "doc_id": "job_1"
}
```

이 데이터는 이후 ChromaDB에 저장해 관련 채용공고를 검색하는 데 사용할 예정입니다.

---

# 데이터 구성

## `jobs.csv`

| 컬럼 | 설명 |
|---|---|
| `id` | 채용공고 식별 번호 |
| `company` | 기업명 |
| `title` | 채용 직무명 |
| `required_skills` | 필수 역량 |
| `preferred_skills` | 우대 역량 |
| `description` | 주요 업무 |
| `job_type` | 직무 분야 |
| `deadline` | 지원 마감일 |

전자전기컴퓨터공학부 학생의 관심 분야를 반영해 다음 공고를 추가했습니다.

- 아날로그 IC 설계 엔지니어
- 디지털 RTL 설계 엔지니어
- 반도체 소자·회로 시뮬레이션 엔지니어

프로젝트에 포함된 기업명과 채용공고는 실습용 가상 데이터입니다.

## `competitions.csv`

공모전명, 분야, 요구 역량, 설명, 마감일 등의 공모전 데이터를 관리합니다.

---

# Ollama 로컬 LLM

Gemini API를 사용할 수 없는 환경에서도 테스트할 수 있도록 Ollama 기반 로컬 LLM 호출 모듈을 구성했습니다.

## 1. 모델 다운로드

```bash
ollama pull llama3.2:3b
```

## 2. 모델 실행 테스트

```bash
ollama run llama3.2:3b
```

종료:

```text
/bye
```

## 3. Ollama 서버 확인

### Windows PowerShell

```powershell
Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing
```

또는:

```powershell
curl.exe http://localhost:11434/api/tags
```

## 4. 프로젝트 모듈 테스트

가상환경이 활성화된 `backend` 폴더에서 실행합니다.

```bash
python -c "from services.ollama_service import get_ollama_response; print(get_ollama_response('한국어로 한 문장으로 자기소개해줘.'))"
```

한국어 답변이 출력되면 로컬 LLM 연결이 정상입니다.

> 현재 `ollama_service.py`를 통한 개별 호출을 구현했으며, Gemini와 Ollama의 자동 선택 연결은 이후 확장할 예정입니다.

---

# MOCK 모드

Gemini API 키가 없거나 요청 한도를 초과한 경우 `backend/.env`에서 다음과 같이 설정합니다.

```env
MOCK_MODE=true
```

서버를 재시작한 뒤 `/analyze`를 호출하면 `[MOCK 응답]`이 포함된 테스트 결과가 반환됩니다.

실제 Gemini API를 다시 사용하려면:

```env
MOCK_MODE=false
```

환경변수 변경 후에는 서버를 다시 시작해야 합니다.

```text
Ctrl + C
```

```bash
uvicorn main:app --reload --port 8000
```

---

# 자주 발생하는 오류

## `ModuleNotFoundError: No module named 'pandas'`

가상환경이 활성화되었는지 확인합니다.

```powershell
venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

---

## PowerShell에서 가상환경 활성화 오류

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```

---

## `No module named 'services'` 오류

서버와 Python 테스트는 `backend` 폴더에서 실행해야 합니다.

```powershell
cd backend
uvicorn main:app --reload --port 8000
```

---

## 8000번 포트 충돌

Windows:

```cmd
netstat -ano | findstr 8000
```

출력 결과의 PID를 확인한 뒤 종료합니다.

```cmd
taskkill /F /PID 실제_PID번호
```

macOS 또는 Linux:

```bash
lsof -i :8000
kill -9 실제_PID번호
```

서버 재실행:

```bash
uvicorn main:app --reload --port 8000
```

---

## Ollama 서버 연결 오류

Windows에서 Ollama는 일반적으로 자동으로 실행됩니다.

자동 실행이 되지 않을 경우 별도 터미널에서 실행합니다.

```bash
ollama serve
```

해당 터미널은 서버 전용으로 유지하고 다른 터미널에서 프로젝트를 실행합니다.

---

## 계속 MOCK 응답이 나오는 경우

`backend/.env`를 확인합니다.

```env
MOCK_MODE=false
GEMINI_API_KEY=실제_API_KEY
```

API 키가 비어 있거나 `MOCK_MODE=true`이면 실제 Gemini API가 호출되지 않습니다.

---

# 진행 현황

- [x] 프로젝트 기획 및 개발 환경 설정
- [x] FastAPI 서버 구축
- [x] 서버 상태 확인 API 구현
- [x] 채용공고 목록 및 상세 조회 API 구현
- [x] 사용자 맞춤 분석 API 구현
- [x] Gemini API 연결
- [x] MOCK 모드 구현
- [x] Ollama 로컬 LLM 실행 환경 구성
- [x] CSV 기반 취업·공모전 데이터 등록
- [x] 반도체·회로 설계 직무 데이터 추가
- [x] 결측치 확인 및 처리
- [x] 중복 채용공고 제거
- [x] 스킬 키워드 표준화
- [x] 전처리 데이터 SQLite 저장
- [x] SQLite 데이터 조회
- [x] 채용공고의 RAG 문서 변환
- [x] RAG 문서 JSON 저장
- [ ] ChromaDB 벡터 검색 연결
- [ ] 사용자와 기업 간 직무 적합도 계산
- [ ] 기업 위치·연봉·규모 정보 연결
- [ ] React 사용자 화면 구현
- [ ] Docker 실행 환경 구성
- [ ] 최종 포트폴리오 문서화

---

# 재현 가능성 체크리스트

다른 사용자는 다음 과정으로 프로젝트를 실행할 수 있습니다.

1. GitHub 저장소 복제
2. `backend` 폴더 이동
3. 가상환경 생성 및 활성화
4. `requirements.txt`를 이용한 패키지 설치
5. `.env.example`을 복사해 `backend/.env` 생성
6. 데이터 전처리 코드 실행
7. FastAPI 서버 실행
8. `/health`와 `/docs` 접속
9. `/analyze` API 테스트

---

# 주의사항

- 실제 API 키는 GitHub에 업로드하지 않습니다.
- `.env`, `venv`, `__pycache__`는 버전 관리에서 제외합니다.
- 프로젝트에 포함된 기업과 채용공고는 실습용 가상 데이터입니다.
- Gemini API 한도 초과 시 MOCK 모드로 테스트할 수 있습니다.
- Ollama 로컬 모델의 첫 응답은 컴퓨터 성능에 따라 시간이 걸릴 수 있습니다.
- 현재 ChromaDB 검색 연결 전이므로 분석 결과의 `sources`가 비어 있을 수 있습니다.