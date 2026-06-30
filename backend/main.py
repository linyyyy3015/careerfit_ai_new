from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import health, jobs, analyze


# FastAPI 앱 객체 생성
# title과 version은 /docs 페이지에 표시된다
app = FastAPI(
    title="CareerFit AI",
    description="취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치",
    version="0.1.0",
)


# CORS 설정
# React 프론트엔드(localhost:5173)의 요청을 허용한다
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(jobs.router)
app.include_router(analyze.router)

@app.get("/")
def root():
    return {
        "message": "CareerFit AI 서버가 실행 중입니다."
    }