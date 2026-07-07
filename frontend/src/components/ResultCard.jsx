function ResultCard({
  answer,
  matchedSkills = [],
  missingSkills = [],
  recommendedProjects = [],
  confidence = null,
}) {
  const hasMatchedSkills =
    Array.isArray(matchedSkills) && matchedSkills.length > 0;

  const hasMissingSkills =
    Array.isArray(missingSkills) && missingSkills.length > 0;

  const hasRecommendedProjects =
    Array.isArray(recommendedProjects) && recommendedProjects.length > 0;

  const hasConfidence = confidence !== null && confidence !== undefined;

  function formatConfidence(value) {
    if (typeof value === "number") {
      if (value <= 1) {
        return `${Math.round(value * 100)}%`;
      }

      return `${Math.round(value)}%`;
    }

    return String(value);
  }

  function getConfidenceStyle(value) {
    if (typeof value === "number") {
      const score = value <= 1 ? value * 100 : value;

      if (score >= 70) {
        return "bg-emerald-50 text-emerald-700 border-emerald-200";
      }

      if (score >= 40) {
        return "bg-amber-50 text-amber-700 border-amber-200";
      }

      return "bg-red-50 text-red-700 border-red-200";
    }

    return "bg-slate-50 text-slate-600 border-slate-200";
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <div className="flex items-start justify-between gap-4 mb-4">
        <div>
          <p className="text-sm font-medium text-emerald-600 mb-1">
            AI Analysis
          </p>

          <h2 className="text-lg font-semibold text-slate-700">
            AI 분석 결과
          </h2>
        </div>

        {hasConfidence && (
          <div
            className={`shrink-0 rounded-full border px-3 py-1 text-xs font-semibold ${getConfidenceStyle(
              confidence
            )}`}
          >
            신뢰도 {formatConfidence(confidence)}
          </div>
        )}
      </div>

      <div className="rounded-lg border-l-4 border-emerald-500 bg-emerald-50/40 p-4">
        <p className="text-sm leading-relaxed text-slate-700 whitespace-pre-line">
          {answer || "분석 결과가 없습니다."}
        </p>
      </div>

      <div className="mt-5 grid gap-4">
        {hasMatchedSkills && (
          <section className="rounded-lg border border-emerald-200 bg-emerald-50 p-4">
            <h3 className="text-sm font-semibold text-emerald-700 mb-2">
              잘 맞는 역량
            </h3>

            <div className="flex flex-wrap gap-2">
              {matchedSkills.map((skill, index) => (
                <span
                  key={`${skill}-${index}`}
                  className="rounded-full bg-white border border-emerald-200 px-3 py-1 text-xs font-medium text-emerald-700"
                >
                  {skill}
                </span>
              ))}
            </div>
          </section>
        )}

        {hasMissingSkills && (
          <section className="rounded-lg border border-amber-200 bg-amber-50 p-4">
            <h3 className="text-sm font-semibold text-amber-700 mb-2">
              보완하면 좋은 역량
            </h3>

            <div className="flex flex-wrap gap-2">
              {missingSkills.map((skill, index) => (
                <span
                  key={`${skill}-${index}`}
                  className="rounded-full bg-white border border-amber-200 px-3 py-1 text-xs font-medium text-amber-700"
                >
                  {skill}
                </span>
              ))}
            </div>
          </section>
        )}

        {hasRecommendedProjects && (
          <section className="rounded-lg border border-blue-200 bg-blue-50 p-4">
            <h3 className="text-sm font-semibold text-blue-700 mb-2">
              추천 포트폴리오 방향
            </h3>

            <ul className="space-y-2">
              {recommendedProjects.map((project, index) => (
                <li
                  key={`${project}-${index}`}
                  className="text-sm text-slate-700 leading-relaxed"
                >
                  <span className="font-semibold text-blue-600">
                    {index + 1}.
                  </span>{" "}
                  {project}
                </li>
              ))}
            </ul>
          </section>
        )}
      </div>
    </div>
  );
}

export default ResultCard;