from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()
router = APIRouter()

todo_list: List[BaseModel] = []

class Todo(BaseModel):
    id: int
    item: str

@router.post("/add_todo", response_model=Todo)
async def add_todo(todo: Todo):
    if not todo.item:
        raise HTTPException(status_code=400, detail="Item cannot be empty")
    todo_list.append(todo)
    return todo

@router.get("/retrieve_todo", response_model=List[Todo])
async def retrieve_todo():
    return todo_list

app.include_router(router)