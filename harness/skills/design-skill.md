# CareerFit AI Design Skill

## 목적
CareerFit AI React UI를 취업·공모전 데이터 기반 AI 포트폴리오 코치처럼 보이게 만든다.

## 디자인 목표
- 신뢰감 있는 AI 코치 서비스
- 발표 화면에서 한눈에 이해되는 구조
- 입력, 분석 결과, 출처, 신뢰도가 분리된 화면
- 과도하게 화려하기보다 설명 가능한 디자인

## 화면 구조
1. Header
   - 서비스명: CareerFit AI
   - 한 줄 설명: 취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치

2. InputForm
   - 전공 입력
   - 보유 스킬 입력
   - 관심 직무 입력
   - 분석 버튼

3. ResultCard
   - answer
   - matched_skills
   - missing_skills
   - recommended_projects
   - confidence

4. SourceCard
   - sources 목록
   - title
   - type
   - matched_reason

## 색상 규칙
- 기본 색상: blue, slate
- 배경: 밝고 단순하게
- 강조: matched_skills, confidence, sources
- 경고: error 상태는 red 계열
- low confidence는 yellow 또는 amber 계열

## UI 상태
반드시 구분해야 하는 상태:
- empty: 아직 분석 전
- loading: 분석 요청 중
- success: 결과 표시
- error: 요청 실패
- no sources: sources가 비어 있음

## 금지
- sources를 숨기지 않는다.
- confidence를 완전히 생략하지 않는다.
- 과도한 애니메이션을 넣지 않는다.
- 실제 없는 채용 정보처럼 보이게 꾸미지 않는다.
- React 코드에 API Key를 넣지 않는다.

## 발표용 기준
발표자가 화면을 보며 다음을 설명할 수 있어야 한다.
1. 사용자가 무엇을 입력하는가?
2. AI가 어떤 분석 결과를 주는가?
3. 어떤 공고 또는 데이터가 근거인가?
4. 신뢰도가 높거나 낮은 이유는 무엇인가?