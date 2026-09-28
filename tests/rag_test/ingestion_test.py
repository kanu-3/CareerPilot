from pathlib import Path

from backend.rag.ingestion import extract_text


file_path = input("Enter document path: ").strip()

path = Path(file_path)

if not path.exists():
    raise FileNotFoundError(
        f"File not found: {file_path}"
    )

text = extract_text(str(path))

print("\nExtracted characters:", len(text))

print("\n--- Extracted text preview ---\n")
print(text[:3000])