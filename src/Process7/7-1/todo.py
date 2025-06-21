# 과정 7 - (문제1) 또 새로운 프로젝트

from fastapi import FastAPI, APIRouter, HTTPException, Request
from typing import Dict, List

app = FastAPI()
router = APIRouter()

todo_list: List[Dict] = []

@router.post("/add_todo")
async def add_todo(request: Request):
    data = await request.json()
    if not data or 'task' not in data or not data['task']:          # 보너스 과제 - 입력되는 Dict 타입이 빈값이면 경고
        raise HTTPException(status_code=400, detail="Task cannot be empty")
    todo_list.append(data)
    return {"message": "Successfully Added To Todo_List!"}

@router.get("/retrieve_todo")
async def retrieve_todo():
    return {"todo_list": todo_list}

app.include_router(router)