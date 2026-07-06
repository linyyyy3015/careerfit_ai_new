function SourceCard({ sources }) {
    if (!sources || sources.length === 0) {
      return (
        <div className="bg-slate-50 rounded-xl border border-slate-200 p-4 text-sm text-slate-500">
          참고한 공고 데이터가 없습니다.
        </div>
      );
    }
  
    return (
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h2 className="text-lg font-semibold text-slate-700 mb-3">
          📄 참고한 공고 출처
        </h2>
  
        <div className="space-y-3">
          {sources.map((source, index) => (
            <div
              key={index}
              className="border-b border-slate-100 pb-3 last:border-0 last:pb-0"
            >
              <p className="text-sm font-medium text-slate-700">
                {source.company} — {source.title}
              </p>
  
              <p className="text-xs text-slate-500 mt-1">
                필수 스킬: {source.required_skills || "정보 없음"}
              </p>
            </div>
          ))}
        </div>
      </div>
    );
  }
  
  export default SourceCard;