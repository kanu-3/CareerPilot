from backend.rag.chunking import split_text


text = """
SUMMARY

AI/ML enthusiast building practical applications with Python and FastAPI.

SKILLS

Python
Machine Learning
Deep Learning
FastAPI
LangChain
LangGraph
PostgreSQL

PROJECTS

CareerPilot
Personal AI career agent using LangGraph, RAG, PostgreSQL and pgvector.

KrishiVani
Farmer assistance application with plant disease detection and market forecasting.

EDUCATION

B.Tech Computer Science and Engineering
AKGEC
"""


chunks = split_text(
    text,
    source_type="resume",
)

print("Total chunks:", len(chunks))

for chunk in chunks:
    print("\n--------------------")
    print("Index:", chunk.chunk_index)
    print("Section:", chunk.section)
    print("Project:", chunk.project)
    print("Source:", chunk.source_type)
    print("Content:")
    print(chunk.content)