# 데이터 전처리 파이프라인
# 실행 위치: backend 폴더
# 실행 명령: python data/preprocess.py

import json
import os
import sqlite3

import pandas as pd


# ─── 1. 파일 경로 설정 ────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JOBS_CSV = os.path.join(BASE_DIR, "jobs.csv")
DB_PATH = os.path.join(BASE_DIR, "careerfit.db")
RAG_JSON = os.path.join(BASE_DIR, "rag_documents.json")


# ─── 2. 스킬 표준화 사전 ───────────────────────────────

SKILL_NORMALIZATION = {
    "python": "Python",
    "sql": "SQL",
    "ai": "AI",
    "ml": "머신러닝",
    "machine learning": "머신러닝",
    "deep learning": "딥러닝",
    "r": "R",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "tableau": "Tableau",
    "powerbi": "Power BI",
    "power bi": "Power BI",
}


# ─── 3. CSV 읽기 ──────────────────────────────────────

def load_data(filepath: str) -> pd.DataFrame:
    """
    CSV 파일을 읽어 DataFrame으로 반환합니다.

    UTF-8 인코딩으로 먼저 읽고,
    인코딩 오류가 발생하면 CP949로 다시 읽습니다.
    """
    try:
        df = pd.read_csv(filepath, encoding="utf-8")
        print(f"✅ 파일 읽기 성공 (UTF-8): {filepath}")

    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="cp949")
        print(f"✅ 파일 읽기 성공 (CP949): {filepath}")

    print(f"   행 수: {len(df)}")
    print(f"   열 수: {len(df.columns)}")
    print(f"   컬럼: {df.columns.tolist()}")

    return df


# ─── 4. 결측치 확인 ────────────────────────────────────

def check_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    각 컬럼의 결측치 수와 비율을 확인합니다.
    """
    print("\n=== 결측치 확인 ===")

    missing = df.isnull().sum()
    missing_pct = (
        df.isnull().sum() / len(df) * 100
    ).round(1)

    result = pd.DataFrame(
        {
            "결측치 수": missing,
            "결측치 비율(%)": missing_pct,
        }
    )

    print(result[result["결측치 수"] > 0])

    if missing.sum() == 0:
        print("   ✅ 결측치 없음")
    else:
        print(f"   ⚠️ 총 {missing.sum()}개 결측치 발견")

    return df


# ─── 5. 결측치 처리 ────────────────────────────────────

def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    결측치를 처리합니다.

    - title 또는 required_skills가 비어 있는 행은 제거합니다.
    - 나머지 텍스트 컬럼은 빈 문자열로 채웁니다.
    """
    print("\n=== 결측치 처리 ===")

    before = len(df)

    df = df.dropna(
        subset=["title", "required_skills"]
    ).copy()

    text_cols = [
        "preferred_skills",
        "description",
        "company",
        "job_type",
    ]

    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("")

    after = len(df)

    print(f"   처리 전: {before}행 → 처리 후: {after}행")
    print(f"   제거된 행: {before - after}행")

    return df


# ─── 6. 중복 확인 및 제거 ──────────────────────────────

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    company와 title 조합을 기준으로
    중복 행을 확인하고 제거합니다.
    """
    print("\n=== 중복 확인 ===")

    before = len(df)

    duplicated = df.duplicated(
        subset=["company", "title"],
        keep=False,
    )

    if duplicated.sum() > 0:
        print(f"   ⚠️ 중복 발견: {duplicated.sum()}행")
        print(
            df.loc[
                duplicated,
                ["company", "title"],
            ].to_string(index=False)
        )
    else:
        print("   ✅ 중복 없음")

    df = df.drop_duplicates(
        subset=["company", "title"],
        keep="first",
    ).copy()

    after = len(df)

    print(f"   제거 후: {after}행 (제거: {before - after}행)")

    return df


# ─── 7. 개별 스킬 문자열 표준화 ────────────────────────

def normalize_skills(skills_str: str) -> str:
    """
    스킬 키워드 문자열을 표준화합니다.

    입력:
        python, sql, Machine Learning

    출력:
        Python, SQL, 머신러닝
    """
    if not isinstance(skills_str, str) or not skills_str.strip():
        return ""

    skills = [
        skill.strip()
        for skill in skills_str.split(",")
    ]

    normalized = []

    for skill in skills:
        lower = skill.lower()
        normalized.append(
            SKILL_NORMALIZATION.get(lower, skill)
        )

    return ", ".join(normalized)


# ─── 8. 스킬 컬럼 전체 표준화 ──────────────────────────

def standardize_skills(df: pd.DataFrame) -> pd.DataFrame:
    """
    required_skills와 preferred_skills 컬럼에
    스킬 키워드 표준화를 적용합니다.
    """
    print("\n=== 스킬 키워드 표준화 ===")

    df = df.copy()

    for col in [
        "required_skills",
        "preferred_skills",
    ]:
        if col in df.columns:
            df[col] = df[col].apply(normalize_skills)

    print("   ✅ 표준화 완료")

    print("\n   [표준화 결과 샘플]")
    print(
        df[
            ["title", "required_skills"]
        ].head(3).to_string(index=False)
    )

    return df


# ─── 9. SQLite 저장 ───────────────────────────────────

def save_to_sqlite(
    df: pd.DataFrame,
    db_path: str,
) -> None:
    """
    전처리된 DataFrame을 SQLite 데이터베이스에 저장합니다.
    """
    print("\n=== SQLite 저장 ===")

    conn = sqlite3.connect(db_path)

    try:
        df.to_sql(
            "jobs",
            conn,
            if_exists="replace",
            index=False,
        )

        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM jobs")
        count = cursor.fetchone()[0]

        print(f"   ✅ 저장 완료: jobs 테이블에 {count}행 저장됨")
        print(f"   파일 위치: {db_path}")

    finally:
        conn.close()


# ─── 10. SQLite 조회 테스트 ───────────────────────────

def query_sqlite(db_path: str) -> None:
    """
    SQLite에서 데이터를 조회해 저장 결과를 확인합니다.
    """
    print("\n=== SQLite 조회 테스트 ===")

    conn = sqlite3.connect(db_path)

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM jobs")
        print(f"   전체 공고 수: {cursor.fetchone()[0]}개")

        print("\n   [직무 분류별 공고 수]")

        cursor.execute(
            """
            SELECT job_type, COUNT(*) AS count
            FROM jobs
            GROUP BY job_type
            ORDER BY count DESC
            """
        )

        for row in cursor.fetchall():
            print(f"   - {row[0]}: {row[1]}개")

        print("\n   [Python이 필요한 공고]")

        cursor.execute(
            """
            SELECT company, title, required_skills
            FROM jobs
            WHERE required_skills LIKE '%Python%'
            LIMIT 3
            """
        )

        for row in cursor.fetchall():
            print(f"   - {row[0]} | {row[1]}")
            print(f"     스킬: {row[2]}")

    finally:
        conn.close()


# ─── 11. RAG 문서 변환 ────────────────────────────────

def convert_to_rag_documents(df: pd.DataFrame) -> list:
    """
    DataFrame의 각 행을 RAG 검색에 적합한
    자연어 문서 형태로 변환합니다.
    """
    print("\n=== RAG 문서 변환 ===")

    documents = []

    for _, row in df.iterrows():
        doc_text = (
            f"{row.get('company', '')}에서 "
            f"{row.get('title', '')}를 채용합니다. "
            f"필수 스킬은 "
            f"{row.get('required_skills', '정보 없음')}입니다. "
            f"우대 스킬: "
            f"{row.get('preferred_skills', '없음')}. "
            f"업무 내용: "
            f"{row.get('description', '정보 없음')}"
        )

        deadline = str(row.get("deadline", ""))
        company = str(row.get("company", ""))

        metadata = {
            "id": str(row.get("id", "")),
            "company": company,
            "title": str(row.get("title", "")),
            "job_type": str(row.get("job_type", "")),
            "deadline": deadline,
            "source": "jobs.csv",

            # 새로 추가한 metadata
            "deadline_month": deadline[5:7] if len(deadline) >= 7 and deadline[4] == "-" else "",
            "is_startup": "true" if "스타트업" in company else "false",
            "first_saved_date": pd.Timestamp.today().strftime("%Y-%m-%d"),
        }

        documents.append(
            {
                "text": doc_text,
                "metadata": metadata,
                "doc_id": f"job_{row.get('id', '')}",
            }
        )

    print(f"   ✅ {len(documents)}개 문서 변환 완료")

    if documents:
        print("\n   [첫 번째 문서 미리보기]")
        print(f"   ID: {documents[0]['doc_id']}")
        print(f"   텍스트: {documents[0]['text'][:100]}...")
        print(f"   메타데이터: {documents[0]['metadata']}")

    return documents

# ─── 12. RAG JSON 저장 ────────────────────────────────

def save_rag_documents(
    documents: list,
    json_path: str,
) -> None:
    """
    RAG 문서를 JSON 파일로 저장합니다.

    ChromaDB에 저장하기 전 중간 결과 파일로 사용합니다.
    """
    with open(
        json_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            documents,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(f"\n   ✅ RAG 문서 JSON 저장: {json_path}")


# ─── 실행 블록 ────────────────────────────────────────

if __name__ == "__main__":
    # 1. CSV 읽기
    df_jobs = load_data(JOBS_CSV)

    # 2. 결측치 확인
    df_jobs = check_missing(df_jobs)

    # 3. 결측치 처리
    df_jobs = handle_missing(df_jobs)

    # 4. 중복 제거
    df_jobs = remove_duplicates(df_jobs)

    # 5. 스킬 표준화
    df_jobs = standardize_skills(df_jobs)

    # 6. SQLite 저장
    save_to_sqlite(df_jobs, DB_PATH)

    # 7. SQLite 조회 테스트
    query_sqlite(DB_PATH)

    # 8. RAG 문서 변환
    rag_docs = convert_to_rag_documents(df_jobs)

    # 9. RAG JSON 저장
    save_rag_documents(rag_docs, RAG_JSON)

    print(
        f"\n✅ 전처리 완료: 최종 {len(df_jobs)}행, "
        f"RAG 문서 {len(rag_docs)}개"
    )