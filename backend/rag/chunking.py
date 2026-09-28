import re
from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass
class Chunk:
    content: str
    section: str | None = None
    project: str | None = None
    chunk_index: int = 0
    source_type: str | None = None


SECTION_NAMES = {
    "summary",
    "profile",
    "objective",
    "education",
    "skills",
    "technical skills",
    "experience",
    "work experience",
    "projects",
    "certifications",
    "achievements",
    "responsibilities",
    "technologies",
    "publications",
    "internships",
    "coursework",
}


fallback_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1600,
    chunk_overlap=200,
    length_function=len,
)


def normalize_heading(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def is_section_heading(line: str) -> bool:
    normalized = normalize_heading(line)

    if normalized in SECTION_NAMES:
        return True

    if (
        len(line.strip()) <= 60
        and line.strip()
        and line.strip().upper() == line.strip()
        and any(char.isalpha() for char in line)
    ):
        return True

    return False


def split_into_sections(text: str) -> list[tuple[str | None, str]]:
    lines = text.splitlines()

    sections = []
    current_section = None
    current_lines = []

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        if is_section_heading(stripped):
            if current_lines:
                sections.append(
                    (
                        current_section,
                        "\n".join(current_lines).strip(),
                    )
                )

            current_section = stripped
            current_lines = []
        else:
            current_lines.append(stripped)

    if current_lines:
        sections.append(
            (
                current_section,
                "\n".join(current_lines).strip(),
            )
        )

    return sections


def detect_project(section: str | None, text: str) -> str | None:
    if not section:
        return None

    if normalize_heading(section) != "projects":
        return None

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if not lines:
        return None
    
    for line in lines:
        if len(line) <= 100 and not line.endswith("."):
            return line

    return None


def split_text(
    text: str,
    source_type: str | None = None,
) -> list[Chunk]:
    if not text or not text.strip():
        return []

    sections = split_into_sections(text)

    chunks = []

    for section, section_text in sections:
        if not section_text.strip():
            continue

        project = detect_project(section, section_text)

        contextual_text = section_text

        if section:
            contextual_text = f"Section: {section}\n{contextual_text}"

        if project:
            contextual_text = f"Project: {project}\n{contextual_text}"

        if len(contextual_text) <= 1600:
            chunks.append(
                Chunk(
                    content=contextual_text,
                    section=section,
                    project=project,
                    source_type=source_type,
                )
            )
            continue

        smaller_chunks = fallback_splitter.split_text(
            contextual_text
        )

        for smaller_chunk in smaller_chunks:
            chunks.append(
                Chunk(
                    content=smaller_chunk,
                    section=section,
                    project=project,
                    source_type=source_type,
                )
            )

    for index, chunk in enumerate(chunks):
        chunk.chunk_index = index

    return chunks