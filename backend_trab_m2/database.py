from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql://postgres:123456@localhost:5432/backend_trab_m2")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  
Base = declarative_base()

def get_db():     
    db = SessionLocal()     
    try:         
        yield db     
    finally:
        db.close()
        