from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
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
