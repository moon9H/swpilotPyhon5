# 과정 7 - (문제3) 완전히 작동하는 To-Do

from fastapi import FastAPI, APIRouter, HTTPException
from typing import List
from model import Todo, TodoItem  # model.py에서 모델을 가져옴

app = FastAPI()
router = APIRouter()

todo_list: List[Todo] = []

# 과제 1, 2에서 완성한 기능
@router.post("/add_todo", response_model=Todo)
async def add_todo(todo: Todo):
    if not todo.item:
        raise HTTPException(status_code=400, detail="Item cannot be empty")
    todo_list.append(todo)
    return todo

@router.get("/retrieve_todo", response_model=List[Todo])
async def retrieve_todo():
    return todo_list

# 과제 3 구현 기능
@router.get("/get_single_todo/{todo_id}", response_model=Todo)
async def get_single_todo(todo_id: int):
    for todo in todo_list:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@router.put("/update_todo/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, updated_todo: TodoItem):
    print(f"Received update request for todo_id: {todo_id} with data: {updated_todo}")
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = updated_todo.item
            print(f"Updated todo: {todo}")
            return todo
    print("Todo not found")
    raise HTTPException(status_code=404, detail="Todo not found")

@router.delete("/delete_single_todo/{todo_id}")
async def delete_single_todo(todo_id: int):
    for todo in todo_list:
        if todo.id == todo_id:
            todo_list.remove(todo)
            return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")

app.include_router(router)