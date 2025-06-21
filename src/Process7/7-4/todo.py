# 과정 7 - (문제4) 알수없는 오류

from fastapi import FastAPI, APIRouter, HTTPException, status
from typing import List
from model import Todo, TodoItem, TodoResponse  # model.py에서 모델을 가져옴

app = FastAPI()
router = APIRouter()

todo_list: List[Todo] = []

# 새로운 Todo 항목을 추가하는 엔드포인트
@router.post("/add_todo", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def add_todo(todo: Todo):
    # 예외 상황: 항목이 비어 있을 때 (400 Bad Request)
    if not todo.item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Item cannot be empty"
        )
    todo_list.append(todo)
    return todo

# 모든 Todo 항목을 조회하는 엔드포인트
@router.get("/retrieve_todo", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def retrieve_todo():
    # 예외 상황: Todo 목록이 비어 있을 때 (404 Not Found)
    if not todo_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No todos found"
        )

    # 보너스 과제 - 응답 모델을 사용하는 방식으로 수정
    return TodoResponse(todos=todo_list, message="Todos retrieved successfully")

# 특정 Todo 항목을 조회하는 엔드포인트
@router.get("/get_single_todo/{todo_id}", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def get_single_todo(todo_id: int):
    for todo in todo_list:
        if todo.id == todo_id:
            return todo
    
    # 예외 상황: 요청한 ID의 Todo 항목이 없을 때 (404 Not Found)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Todo not found"
    )

# 특정 Todo 항목을 업데이트하는 엔드포인트
@router.put("/update_todo/{todo_id}", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def update_todo(todo_id: int, updated_todo: TodoItem):
    for todo in todo_list:
        if todo.id == todo_id:
            # 예외 상황: 업데이트할 항목이 비어 있을 때 (400 Bad Request)
            if not updated_todo.item:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Updated item cannot be empty"
                )
            
            todo.item = updated_todo.item
            return todo
    
    # 예외 상황: 요청한 ID의 Todo 항목이 없을 때 (404 Not Found)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Todo not found"
    )

# 특정 Todo 항목을 삭제하는 엔드포인트
@router.delete("/delete_single_todo/{todo_id}", status_code=status.HTTP_201_CREATED)
async def delete_single_todo(todo_id: int):
    for todo in todo_list:
        if todo.id == todo_id:
            todo_list.remove(todo)
            return {"message": "Todo deleted successfully"}
    
    # 예외 상황: 요청한 ID의 Todo 항목이 없을 때 (404 Not Found)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Todo not found"
    )

app.include_router(router)
