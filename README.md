# CareerFit AI

> 취업·공모전 데이터를 기반으로 사용자에게 맞춤형 커리어 준비 방향을 제안하는 AI 포트폴리오 코치

## 프로젝트 소개

CareerFit AI는 사용자의 전공, 보유 기술, 관심 직무를 입력받아 채용공고와 공모전 데이터를 분석하고 맞춤형 커리어 조언을 제공하는 서비스입니다.

FastAPI 기반 백엔드에서 채용공고 조회 API와 사용자 분석 API를 제공하며, Gemini API를 활용해 사용자별 답변을 생성합니다.

현재는 CSV 기반 채용공고·공모전 데이터를 사용하고 있으며, 이후 ChromaDB 기반 RAG 검색과 React 사용자 화면을 연결할 예정입니다.

---

## 주요 기능

- 서버 상태 확인
- 전체 채용공고 목록 조회
- 특정 채용공고 상세 조회
- 전공·보유 기술·관심 직무 기반 커리어 분석
- Gemini API 기반 맞춤형 답변 생성
- MOCK 모드를 활용한 API 키 없는 테스트
- Swagger UI 기반 API 테스트
- CSV 기반 취업·공모전 데이터 관리

---

## 기술 스택

| 영역 | 기술 |
|---|---|
| 백엔드 | Python, FastAPI |
| AI API | Gemini 2.5 Flash-Lite |
| 데이터 처리 | Pandas |
| 데이터 저장 | CSV |
| API 문서 | Swagger UI |
| 버전 관리 | Git, GitHub |
| 확장 예정 | ChromaDB, RAG, React, Vite, Docker |

---

## 프로젝트 구조

```text
careerfit_ai_new
├─ backend
│  ├─ data
│  │  ├─ jobs.csv
│  │  └─ competitions.csv
│  ├─ routers
│  │  ├─ analyze.py
│  │  └─ jobs.py
│  ├─ services
│  │  ├─ __init__.py
│  │  └─ llm_service.py
│  ├─ .env.example
│  ├─ main.py
│  └─ requirements.txt
├─ .gitignore
└─ README.md
```

> 실제 API 키가 포함된 `backend/.env` 파일과 로컬 가상환경 폴더 `venv`는 GitHub에 업로드하지 않습니다.

---

# 로컬 실행 방법

## 1. 사전 요구사항

다음 프로그램이 설치되어 있어야 합니다.

- Python 3.10 이상
- Git
- Cursor 또는 Visual Studio Code

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

이후 명령어는 기본적으로 `backend` 폴더에서 실행합니다.

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

PowerShell에서 스크립트 실행 오류가 발생하면 다음 명령어를 먼저 실행합니다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```

---

## 6. 필수 패키지 설치

```bash
python -m pip install -r requirements.txt
```

Gemini 라이브러리 설치 여부 확인:

```bash
python -c "import google.generativeai as genai; print('설치 확인:', genai.__version__)"
```

버전이 출력되면 정상적으로 설치된 것입니다.

---

## 7. 환경변수 파일 생성

`backend/.env.example` 파일을 복사해 `backend/.env` 파일을 만듭니다.

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### macOS / Linux

```bash
cp .env.example .env
```

생성된 `.env` 파일을 열고 환경변수를 설정합니다.

### Gemini API를 사용하는 경우

```env
MOCK_MODE=false
GEMINI_API_KEY=본인의_GEMINI_API_KEY
```

### API 키 없이 테스트하는 경우

```env
MOCK_MODE=true
GEMINI_API_KEY=
```

`MOCK_MODE=true`이면 Gemini API를 호출하지 않고 테스트용 응답을 반환합니다.

> 실제 Gemini API 키가 포함된 `.env` 파일은 GitHub에 업로드하지 않습니다.

---

## 8. 서버 실행

가상환경이 활성화된 `backend` 터미널에서 실행합니다.

```bash
uvicorn main:app --reload --port 8000
```

아래 문구가 출력되면 서버가 정상적으로 실행된 것입니다.

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

브라우저에서 다음 주소에 접속합니다.

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

현재 RAG 검색 연결 전에는 `sources`가 빈 배열로 표시될 수 있습니다.

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

## API 사용 예시

### 전체 채용공고 조회

```bash
curl http://localhost:8000/jobs
```

### 특정 채용공고 조회

```bash
curl http://localhost:8000/jobs/1
```

### 사용자 맞춤 분석

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "major": "전자전기컴퓨터공학부",
    "skills": ["전자회로", "Python", "SPICE"],
    "job_type": "반도체 회로 설계"
  }'
```

Windows에서는 Swagger UI를 이용한 테스트를 권장합니다.

---

## 데이터 구성

### `jobs.csv`

채용공고 데이터는 다음 컬럼으로 구성됩니다.

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

사용자의 관심 분야를 반영해 다음 반도체·회로 설계 공고를 추가했습니다.

- 아날로그 IC 설계 엔지니어
- 디지털 RTL 설계 엔지니어
- 반도체 소자·회로 시뮬레이션 엔지니어

프로젝트에 포함된 기업명과 공고 내용은 실습용 가상 데이터입니다.

### `competitions.csv`

공모전명, 분야, 요구 역량, 설명, 마감일 등의 공모전 데이터를 관리합니다.

---

## MOCK 모드

Gemini API 키가 없거나 API 요청 한도를 초과한 경우 `backend/.env`에서 다음 값을 설정합니다.

```env
MOCK_MODE=true
```

서버를 재시작한 뒤 `/analyze`를 호출하면 `[MOCK 응답]`이 포함된 테스트 결과가 반환됩니다.

실제 Gemini API를 다시 사용하려면 다음과 같이 변경합니다.

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

## 자주 발생하는 오류

### PowerShell에서 가상환경 활성화 오류

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```

### `No module named 'services'` 오류

서버를 `backend` 폴더에서 실행해야 합니다.

```powershell
cd backend
uvicorn main:app --reload --port 8000
```

### 8000번 포트 충돌

Windows에서 8000번 포트를 사용하는 프로세스를 확인합니다.

```cmd
netstat -ano | findstr 8000
```

출력 결과 맨 오른쪽의 PID를 확인한 뒤 종료합니다.

```cmd
taskkill /F /PID 실제_PID번호
```

macOS 또는 Linux:

```bash
lsof -i :8000
kill -9 실제_PID번호
```

그다음 서버를 다시 실행합니다.

```bash
uvicorn main:app --reload --port 8000
```

### Gemini 패키지를 찾지 못하는 경우

```bash
python -m pip install google-generativeai
```

### 계속 MOCK 응답이 나오는 경우

`backend/.env` 파일을 확인합니다.

```env
MOCK_MODE=false
GEMINI_API_KEY=실제_API_KEY
```

API 키가 비어 있거나 `MOCK_MODE=true`이면 실제 Gemini API가 호출되지 않습니다.

---

## 진행 현황

- [x] 프로젝트 기획 및 개발 환경 설정
- [x] FastAPI 서버 구축
- [x] 서버 상태 확인 API 구현
- [x] 채용공고 목록 및 상세 조회 API 구현
- [x] 사용자 맞춤 분석 API 구현
- [x] Gemini API 연결
- [x] MOCK 모드 구현
- [x] CSV 기반 취업·공모전 데이터 등록
- [x] 반도체·회로 설계 직무 데이터 추가
- [ ] ChromaDB 기반 데이터 저장
- [ ] RAG 검색 기능 구현
- [ ] React 사용자 화면 구현
- [ ] Docker 실행 환경 구성
- [ ] 최종 포트폴리오 문서화

---

## 재현 가능성 체크리스트

다른 사용자는 다음 과정으로 프로젝트를 실행할 수 있습니다.

1. GitHub 저장소 복제
2. `backend` 폴더 이동
3. 가상환경 생성 및 활성화
4. `requirements.txt`를 이용한 패키지 설치
5. `.env.example`을 복사해 `.env` 생성
6. FastAPI 서버 실행
7. `/health`와 `/docs` 접속
8. `/analyze` API 테스트

---

## 주의사항

- 실제 API 키는 GitHub에 업로드하지 않습니다.
- `.env`, `venv`, `__pycache__`는 버전 관리에서 제외합니다.
- 프로젝트에 포함된 기업과 채용공고는 실습용 가상 데이터입니다.
- Gemini API 한도 초과 시 MOCK 모드로 테스트할 수 있습니다.
- 현재 RAG 연결 전이므로 분석 결과의 `sources`가 비어 있을 수 있습니다.