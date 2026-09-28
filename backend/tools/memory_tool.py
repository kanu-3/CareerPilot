from sqlalchemy import select

from backend.database.connection import SessionLocal
from backend.database.model import Memory


VALID_MEMORY_TYPES = {
    "preference",
    "goal",
    "skill_gap",
    "learning",
    "application",
    "interview",
    "career_context",
    "decision",
}

VALID_IMPORTANCE = {
    "low",
    "medium",
    "high",
}


def save_memory(
    user_id: int,
    memory_type: str,
    content: str,
    importance: str = "medium",
) -> dict:

    if memory_type not in VALID_MEMORY_TYPES:
        raise ValueError(
            f"Invalid memory type '{memory_type}'. "
            f"Valid types: {sorted(VALID_MEMORY_TYPES)}"
        )

    if importance not in VALID_IMPORTANCE:
        raise ValueError(
            f"Invalid importance '{importance}'. "
            f"Valid values: {sorted(VALID_IMPORTANCE)}"
        )

    db = SessionLocal()

    try:
        memory = Memory(
            user_id=user_id,
            memory_type=memory_type,
            content=content,
            importance=importance,
        )

        db.add(memory)
        db.commit()
        db.refresh(memory)

        return {
            "success": True,
            "memory_id": memory.id,
            "memory_type": memory.memory_type,
            "content": memory.content,
            "importance": memory.importance,
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_memories(
    user_id: int,
    memory_type: str | None = None,
) -> list[dict]:

    if memory_type is not None and memory_type not in VALID_MEMORY_TYPES:
        raise ValueError(
            f"Invalid memory type '{memory_type}'. "
            f"Valid types: {sorted(VALID_MEMORY_TYPES)}"
        )

    db = SessionLocal()

    try:
        statement = (
            select(Memory)
            .where(Memory.user_id == user_id)
            .order_by(Memory.updated_at.desc())
        )

        if memory_type is not None:
            statement = statement.where(
                Memory.memory_type == memory_type
            )

        memories = db.execute(statement).scalars().all()

        return [
            {
                "memory_id": memory.id,
                "memory_type": memory.memory_type,
                "content": memory.content,
                "importance": memory.importance,
                "created_at": memory.created_at,
                "updated_at": memory.updated_at,
            }
            for memory in memories
        ]

    finally:
        db.close()


def get_memory(
    user_id: int,
    memory_id: int,
) -> dict | None:

    db = SessionLocal()

    try:
        memory = db.execute(
            select(Memory).where(
                Memory.id == memory_id,
                Memory.user_id == user_id,
            )
        ).scalar_one_or_none()

        if memory is None:
            return None

        return {
            "memory_id": memory.id,
            "memory_type": memory.memory_type,
            "content": memory.content,
            "importance": memory.importance,
            "created_at": memory.created_at,
            "updated_at": memory.updated_at,
        }

    finally:
        db.close()


def update_memory(
    user_id: int,
    memory_id: int,
    content: str | None = None,
    importance: str | None = None,
) -> dict:

    if importance is not None and importance not in VALID_IMPORTANCE:
        raise ValueError(
            f"Invalid importance '{importance}'. "
            f"Valid values: {sorted(VALID_IMPORTANCE)}"
        )

    db = SessionLocal()

    try:
        memory = db.execute(
            select(Memory).where(
                Memory.id == memory_id,
                Memory.user_id == user_id,
            )
        ).scalar_one_or_none()

        if memory is None:
            raise ValueError(
                f"Memory {memory_id} not found."
            )

        if content is not None:
            memory.content = content

        if importance is not None:
            memory.importance = importance

        db.commit()
        db.refresh(memory)

        return {
            "success": True,
            "memory_id": memory.id,
            "memory_type": memory.memory_type,
            "content": memory.content,
            "importance": memory.importance,
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()