from fastapi import FastAPI
from app.routes import todos
from app.database import init_db

app = FastAPI(title="Todo API", version="1.0.0")
app.include_router(todos.router, prefix="/todos", tags=["todos"])

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}
