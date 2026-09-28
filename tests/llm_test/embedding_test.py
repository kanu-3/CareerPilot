from ...backend.llm.embeddings import embedding_model


text = "CareerPilot helps analyze jobs and identify skill gaps."

embedding = embedding_model.embed_text(text)

print("Embedding dimension:", len(embedding))
print("First 5 values:", embedding[:5])