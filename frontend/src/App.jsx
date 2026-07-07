import { useState } from "react";
import InputForm from "./components/InputForm";
import ResultCard from "./components/ResultCard";
import SourceCard from "./components/SourceCard";
import { apiUrl } from "./lib/api";

// API Key는 절대 React 코드에 넣지 않습니다.
// 백엔드 주소는 frontend/.env.local 또는 Render 환경변수의 VITE_API_BASE_URL로 관리합니다.

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleAnalyze(formData) {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(apiUrl("/analyze"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          major: formData.major,
          skills: formData.skills,
          job_type: formData.job_type || formData.jobType,
        }),
      });

      if (!response.ok) {
        throw new Error(`서버 오류가 발생했습니다. 상태 코드: ${response.status}`);
      }

      const data = await response.json();

      setResult({
        answer: data.answer || "분석 결과가 없습니다.",
        sources: Array.isArray(data.sources) ? data.sources : [],
        matched_skills: data.matched_skills || [],
        missing_skills: data.missing_skills || [],
        recommended_projects: data.recommended_projects || [],
        confidence: data.confidence ?? null,
      });
    } catch (err) {
      if (err.message.includes("Failed to fetch")) {
        setError(
          "FastAPI 서버에 연결할 수 없습니다. 백엔드 서버가 실행 중인지 확인하세요."
        );
      } else {
        setError(err.message || "분석 요청 중 오류가 발생했습니다.");
      }
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 py-10 px-4">
      <main className="max-w-2xl mx-auto">
        <header className="mb-8">
          <p className="text-sm font-medium text-blue-500 mb-2">
            AI Portfolio Coach
          </p>

          <h1 className="text-2xl font-bold text-slate-800 mb-2">
            CareerFit AI
          </h1>

          <p className="text-sm text-slate-500">
            취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치
          </p>
        </header>

        <InputForm onSubmit={handleAnalyze} isLoading={isLoading} />

        {!result && !isLoading && !error && (
          <div className="mt-4 rounded-xl border border-slate-200 bg-white p-4 text-sm text-slate-500">
            전공, 보유 스킬, 관심 직무를 입력하면 AI가 관련 공고 데이터를 참고해
            역량 분석 결과를 제공합니다.
          </div>
        )}

        {error && (
          <div className="mt-4 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            <p className="font-semibold mb-1">요청 실패</p>
            <p>{error}</p>
          </div>
        )}

        {isLoading && (
          <div className="mt-8 rounded-xl border border-slate-200 bg-white p-6 text-center">
            <p className="text-sm font-medium text-slate-700">
              분석 중입니다...
            </p>
            <p className="mt-2 text-sm text-slate-500">
              입력한 정보와 공고 데이터를 비교하고 있어요.
            </p>
          </div>
        )}

        {result && !isLoading && (
          <section className="mt-8 space-y-4">
            <ResultCard
              answer={result.answer}
              matchedSkills={result.matched_skills}
              missingSkills={result.missing_skills}
              recommendedProjects={result.recommended_projects}
              confidence={result.confidence}
            />

            <SourceCard sources={result.sources} />
          </section>
        )}
      </main>
    </div>
  );
}

export default App;