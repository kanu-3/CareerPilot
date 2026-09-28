# from .connection import engine
# from .model import Base

# Base.metadata.create_all(bind=engine)

# print("Database tables created successfully.")

from ...backend.database.connection import engine
from ...backend.database.model import Base

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")