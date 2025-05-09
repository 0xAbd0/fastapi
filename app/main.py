from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import redis
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

r = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True)

# --- SQLAlchemy Model ---
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "FastAPI with PostgreSQL, Redis, and NGINX is working!"}

@app.get("/cache/{key}")
def get_cache(key: str):
    value = r.get(key)
    if value:
        return {"key": key, "value": value}
    else:
        raise HTTPException(status_code=404, detail="Key not found")

@app.post("/cache/{key}")
def set_cache(key: str, value: str):
    r.set(key, value)
    return {"key": key, "value": value}

@app.post("/items/{name}")
def create_item(name: str, db: Session = Depends(get_db)):
    item = Item(name=name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get("/items")
def list_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

@app.get("/health")
def health_check():
    try:
        with engine.connect() as conn:
            db_ok = conn.execute(text("SELECT 1")).scalar() == 1
    except Exception:
        db_ok = False

    try:
        redis_ok = r.ping()
    except Exception:
        redis_ok = False

    return {
        "postgresql": "ok" if db_ok else "unreachable",
        "redis": "ok" if redis_ok else "unreachable"
    }
