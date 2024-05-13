# scripts/initialize_db.py
from thoughtsculpt.data.models import Base, engine

def initialize_database():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    initialize_database()
