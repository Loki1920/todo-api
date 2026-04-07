from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Todo

router = APIRouter()

@router.get("/")
def list_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

@router.post("/")
def create_todo(title: str, description: str = None, db: Session = Depends(get_db)):
    todo = Todo(title=title, description=description)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@router.put("/{todo_id}/complete")
def complete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = True
    db.commit()
    return todo
