import { useState } from "react";

function InputForm({ onSubmit, isLoading }) {
  const [major, setMajor] = useState("");
  const [skillsInput, setSkillsInput] = useState("");
  const [jobType, setJobType] = useState("");

  const isDisabled =
    isLoading || !major.trim() || !skillsInput.trim() || !jobType.trim();

  function handleSubmit(e) {
    e.preventDefault();

    const trimmedMajor = major.trim();
    const trimmedJobType = jobType.trim();

    const skills = skillsInput
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);

    if (!trimmedMajor || skills.length === 0 || !trimmedJobType || isLoading) {
      return;
    }

    onSubmit({
      major: trimmedMajor,
      skills,
      job_type: trimmedJobType,
    });
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <h2 className="text-lg font-semibold text-slate-700 mb-1">
        내 정보 입력
      </h2>

      <p className="text-sm text-slate-500 mb-4">
        전공과 보유 스킬을 입력하면 관련 공고 데이터를 바탕으로 맞춤형 역량 분석을 제공합니다.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-600 mb-1">
            전공
          </label>
          <input
            type="text"
            value={major}
            onChange={(e) => setMajor(e.target.value)}
            placeholder="예: 통계학과"
            className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-600 mb-1">
            보유 스킬
          </label>
          <input
            type="text"
            value={skillsInput}
            onChange={(e) => setSkillsInput(e.target.value)}
            placeholder="예: Python, SQL, R"
            className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <p className="mt-1 text-xs text-slate-500">
            여러 개의 스킬은 쉼표로 구분해서 입력하세요.
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-600 mb-1">
            관심 직무
          </label>
          <input
            type="text"
            value={jobType}
            onChange={(e) => setJobType(e.target.value)}
            placeholder="예: 데이터 분석"
            className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <button
          type="submit"
          disabled={isDisabled}
          className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-medium py-2 px-4 rounded-lg transition-colors text-sm"
        >
          {isLoading ? "분석 중입니다..." : "역량 분석 요청"}
        </button>
      </form>
    </div>
  );
}

export default InputForm;