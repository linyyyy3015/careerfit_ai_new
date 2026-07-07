# CareerFit AI — 일차별 체크리스트

## 1일차

- [x] careerfit_ai_new/ 폴더 구조 생성 완료
- [x] .gitignore에 .env 포함 확인
- [x] .env.example 파일 생성 완료
- [x] .cursor/rules/project-rules.mdc 작성 완료
- [x] docs/AI_TA_RULES.md 작성 완료
- [x] docs/PROMPTS.md 바이브코딩 규칙 작성 완료
- [x] docs/CHECKLIST.md 작성 완료
- [x] docs/EVAL_QUESTIONS.md 작성 완료
- [x] docs/PROJECT_PLAN.md 작성 완료
- [x] GitHub Repository 생성 및 초기 커밋 완료
- [ ] 피어그룹 멤버 이름·GitHub URL 기록 완료

## 2일차

- [x] Python 가상환경(venv) 생성 및 활성화 확인
- [x] requirements.txt 생성 및 패키지 설치 완료
- [x] .env 파일 생성 및 GEMINI_API_KEY 입력 완료
- [x] FastAPI /health 실행 확인 (localhost:8000/health)
- [x] FastAPI /docs 접속 확인 (localhost:8000/docs)
- [x] /jobs API 목업 응답 확인
- [x] /analyze API 기본 구조 작성 완료
- [x] Gemini API 최초 응답 확인
- [x] README.md 골격 작성 완료
- [x] GitHub 커밋 완료 (.env 미포함 확인)

## 3일차

- [x] 강사 제공 CSV 데이터 확인 완료
- [x] Pandas로 CSV 읽기 성공
- [x] 결측치·중복 확인 완료
- [x] 스킬 키워드 표준화 완료
- [x] SQLite DB 생성 및 저장 확인
- [x] SQLite 조회 확인
- [x] RAG 문서 구조로 변환 완료
- [x] ChromaDB 컬렉션 생성 및 문서 저장 확인
- [x] metadata 설계 완료
- [x] deadline_month metadata 추가 완료
- [x] is_startup metadata 추가 완료
- [x] first_saved_date metadata 추가 완료
- [x] python data/preprocess.py 실행 성공
- [x] RAG 문서 15개 생성 확인
- [x] GitHub 커밋 완료

## 4일차

- [x] ChromaDB 질문 기반 검색 확인
- [x] 검색 결과 품질 점검 완료
- [x] /analyze API RAG 응답으로 변경 완료
- [x] React 프로젝트 생성 및 실행 확인 (localhost:5173)
- [x] /analyze API 연결 완료
- [x] 결과 카드 화면 출력 확인
- [x] 출처 카드 화면 출력 확인
- [x] 로컬 통합 테스트 완료
- [x] 전자전기컴퓨터공학부 기준 반도체 회로 설계 입력 테스트 완료
- [x] RAG Sources 3개 출력 확인
- [x] GitHub 커밋 완료

## 5일차

- [x] Docker 설치 확인
- [x] WSL 설치 및 Docker Desktop 실행 확인
- [x] backend/requirements.txt 최종 확인
- [x] 불필요한 PyTorch/HuggingFace 패키지 주석 처리
- [x] backend/Dockerfile 작성 완료
- [x] backend/.dockerignore 작성 완료
- [x] Docker build 성공
- [x] Docker run 후 /health 접속 확인
- [x] Docker run 후 /docs 접속 확인
- [x] .env 미포함 보안 확인
- [x] backend/.env가 Git에서 무시되는지 확인
- [x] Render 백엔드 Web Service 생성 완료
- [x] Render 환경변수 GEMINI_API_KEY 설정 완료
- [x] Render 환경변수 MOCK_MODE=false 설정 완료
- [x] Render 환경변수 LLM_MODEL=gemini-2.5-flash-lite 설정 완료
- [x] Render 백엔드 /health 확인
- [x] Render 백엔드 /docs 확인
- [x] 로컬 React 프론트엔드에서 Render 백엔드 연결 확인
- [x] VITE_API_BASE_URL 기반 프론트엔드 API 주소 분리 완료
- [x] AI 분석 결과 출력 확인
- [x] RAG Sources 출력 확인
- [ ] README 최종화 완료 (문제정의·데이터·구현·검증 4단계)
- [x] 최종 하네스 파일 업데이트 완료
- [ ] GitHub 최종 커밋 완료
- [ ] 팀 리플렉션 발표 준비 완료

---

## 제출 전 최종 점검

### GitHub Repository

- [ ] Repository가 Public으로 설정되어 있는가?
- [ ] README.md가 GitHub에서 정상 렌더링되는가?
- [ ] backend/, frontend/, docs/ 폴더가 모두 있는가?
- [ ] .env 파일이 Repository에 없는가?
- [ ] frontend/.env.local 파일이 Repository에 없는가?
- [ ] chroma_db/가 Repository에 없는가?
- [ ] Dockerfile이 backend/ 폴더 안에 있는가?
- [ ] .env.example 파일이 있는가?

### 코드 동작

- [x] uvicorn으로 FastAPI 실행 후 /health 응답 확인
- [x] /analyze가 sources 포함 응답을 반환하는가?
- [x] React UI에서 결과 카드가 출력되는가?
- [x] React UI에서 출처 카드가 출력되는가?
- [x] Docker build가 성공하는가?
- [x] Docker run 후 /health 응답이 오는가?
- [x] Render 백엔드 /docs가 정상 출력되는가?
- [x] 로컬 프론트엔드에서 Render 백엔드로 분석 요청이 성공하는가?

### 문서

- [ ] README에 실행 방법이 있는가?
- [x] docs/ 폴더에 하네스 파일 4개 이상이 있는가?
- [ ] 구현하지 않은 기능이 “향후 개선”으로 분리되어 있는가?
- [x] EVAL_QUESTIONS.md에 자기 평가 답변이 작성되어 있는가?
- [x] CHECKLIST.md가 최신 상태로 업데이트되어 있는가?

### 보안

- [x] .gitignore에 .env가 있는가?
- [x] backend/.env가 Git에서 무시되는가?
- [x] frontend/.env.local이 Git에서 무시되는가?
- [x] 코드 어디에도 API Key가 직접 포함되어 있지 않은가?
- [x] .env.example에는 실제 Key가 아닌 예시값만 있는가?