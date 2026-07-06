function ResultCard({ answer }) {
    return (
      <div className="bg-white rounded-xl shadow-sm border-l-4 border-emerald-500 p-6">
        <h2 className="text-lg font-semibold text-slate-700 mb-3">
          📊 AI 분석 결과
        </h2>
  
        <p className="text-slate-600 text-sm leading-relaxed whitespace-pre-line">
          {answer}
        </p>
      </div>
    );
  }
  
  export default ResultCard;