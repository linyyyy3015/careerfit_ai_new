function SourceCard({ sources = [] }) {
  if (!Array.isArray(sources) || sources.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <p className="text-sm font-medium text-slate-700 mb-1">
          참고한 공고 출처
        </p>

        <div className="rounded-lg border border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
          아직 참고한 공고 데이터가 없습니다.
        </div>
      </div>
    );
  }

  function getValue(value, fallback = "정보 없음") {
    if (value === null || value === undefined || value === "") {
      return fallback;
    }

    return value;
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <div className="mb-4">
        <p className="text-sm font-medium text-blue-500 mb-1">
          RAG Sources
        </p>

        <h2 className="text-lg font-semibold text-slate-700">
          참고한 공고 출처
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          AI가 분석에 참고한 공고 데이터입니다. 발표 시 분석 근거로 설명할 수 있습니다.
        </p>
      </div>

      <div className="space-y-3">
        {sources.map((source, index) => {
          const company = getValue(source.company);
          const title = getValue(source.title);
          const jobType = getValue(source.job_type || source.type);
          const requiredSkills = getValue(source.required_skills);
          const matchedReason = source.matched_reason;

          return (
            <article
              key={`${company}-${title}-${index}`}
              className="rounded-lg border border-slate-200 bg-slate-50 p-4"
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-xs font-semibold text-blue-500 mb-1">
                    Source {index + 1}
                  </p>

                  <h3 className="text-sm font-semibold text-slate-800">
                    {company} — {title}
                  </h3>
                </div>

                <span className="shrink-0 rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700">
                  {jobType}
                </span>
              </div>

              <div className="mt-3 space-y-2">
                <p className="text-xs text-slate-500">
                  <span className="font-semibold text-slate-600">
                    필수 스킬:
                  </span>{" "}
                  {requiredSkills}
                </p>

                {matchedReason && (
                  <p className="text-xs leading-relaxed text-slate-500">
                    <span className="font-semibold text-slate-600">
                      참고 이유:
                    </span>{" "}
                    {matchedReason}
                  </p>
                )}
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
}

export default SourceCard;