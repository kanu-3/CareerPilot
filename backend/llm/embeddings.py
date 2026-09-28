import requests


OLLAMA_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"


class EmbeddingModel:

    def embed_text(self, text: str) -> list[float]:
        response = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={
                "model": EMBEDDING_MODEL,
                "prompt": text,
            },
            timeout=120,
        )

        response.raise_for_status()

        return response.json()["embedding"]

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return [
            self.embed_text(text)
            for text in texts
        ]


embedding_model = EmbeddingModel()