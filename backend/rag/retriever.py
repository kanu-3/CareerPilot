from backend.rag.vectorstore import search_similar_chunks


def retrieve_knowledge(
    query: str,
    user_id: int,
    limit: int = 5,
    source_type: str | None = None,
):
    results = search_similar_chunks(
        query=query,
        user_id=user_id,
        limit=limit,
    )

    knowledge = []

    for chunk, distance in results:

        if source_type and chunk.source_type != source_type:
            continue

        knowledge.append(
            {
                "content": chunk.content,
                "section": chunk.section,
                "project": chunk.project,
                "source_type": chunk.source_type,
                "distance": float(distance),
                "document_id": chunk.document_id,
                "chunk_id": chunk.id,
            }
        )

    return knowledge