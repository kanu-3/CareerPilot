from backend.llm.qwen import qwen_model
from backend.rag.retriever import retrieve_knowledge


SYSTEM_PROMPT = """
You are CareerPilot, a personal career assistant.

Answer questions using ONLY the knowledge provided in the context.

Rules:
1. Do not invent skills, projects, experience, education, or achievements.
2. If the context does not contain enough information, explicitly say that
   the information is unavailable.
3. Distinguish between direct evidence and uncertain information.
4. Keep answers concise and factual.
"""


def answer_from_knowledge(
    query: str,
    user_id: int,
    limit: int = 5,
) -> dict:

    knowledge = retrieve_knowledge(
        query=query,
        user_id=user_id,
        limit=limit,
    )

    if not knowledge:
        return {
            "answer": "I could not find relevant information in your knowledge base.",
            "sources": [],
        }

    context_parts = []

    for index, item in enumerate(knowledge, start=1):

        context_parts.append(
            f"""
SOURCE {index}
Document ID: {item["document_id"]}
Section: {item["section"]}
Project: {item["project"]}
Source type: {item["source_type"]}

Content:
{item["content"]}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
Answer the following question using ONLY the supplied sources.

QUESTION:
{query}

SOURCES:
{context}

If the sources do not provide enough evidence, say so explicitly.
"""

    answer = qwen_model.generate(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
    )

    return {
        "answer": answer,
        "sources": knowledge,
    }