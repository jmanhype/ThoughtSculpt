from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from thoughtsculpt.config import settings

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    solution = Column(Text, nullable=True)

# Setup the database connection and session
engine = create_engine(settings.database_url)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()
