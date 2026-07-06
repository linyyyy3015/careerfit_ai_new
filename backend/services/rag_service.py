# backend/services/rag_service.py

import json
from pathlib import Path

import chromadb


BASE_DIR = Path(__file__).parent.parent
CHROMA_PATH = str(BASE_DIR / "chroma_db")
RAG_JSON = str(BASE_DIR / "data" / "rag_documents.json")


client = chromadb.PersistentClient(path=CHROMA_PATH)


def get_or_create_collection() -> chromadb.Collection:
    """
    ChromaDB 컬렉션을 가져오거나, 비어있으면 RAG 문서를 로드합니다.
    """
    collection = client.get_or_create_collection(
        name="careerfit_jobs",
        metadata={
            "description": "CareerFit AI 취업·공모전 데이터"
        },
    )

    if collection.count() == 0:
        print("⚠️ ChromaDB가 비어있습니다. RAG 문서를 다시 저장합니다...")
        _load_documents(collection)

    return collection


def _load_documents(collection: chromadb.Collection) -> None:
    """
    rag_documents.json에서 문서를 읽어 ChromaDB에 저장합니다.
    """
    with open(RAG_JSON, "r", encoding="utf-8") as f:
        documents = json.load(f)

    collection.add(
        documents=[
            doc["text"]
            for doc in documents
        ],
        metadatas=[
            doc["metadata"]
            for doc in documents
        ],
        ids=[
            doc["doc_id"]
            for doc in documents
        ],
    )

    print(f"✅ {collection.count()}개 문서 저장 완료")


def search_documents(
    query: str,
    n_results: int = 3,
    job_type: str = None,
) -> list:
    """
    사용자 질문과 의미적으로 유사한 문서를 ChromaDB에서 검색합니다.

    Args:
        query: 사용자 질문 텍스트
        n_results: 반환할 문서 수
        job_type: 특정 직무유형으로 검색 결과를 제한할 때 사용

    Returns:
        [{"text": str, "metadata": dict, "distance": float}, ...]
    """
    collection = get_or_create_collection()

    where_filter = None

    if job_type:
        where_filter = {
            "job_type": job_type
        }

    query_kwargs = {
        "query_texts": [query],
        "n_results": min(n_results, collection.count()),
    }

    if where_filter:
        query_kwargs["where"] = where_filter

    results = collection.query(**query_kwargs)

    return [
        {
            "text": text,
            "metadata": metadata,
            "distance": round(distance, 4),
        }
        for text, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]