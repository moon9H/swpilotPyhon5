# 과정 7 - (문제4) 알수없는 오류

from pydantic import BaseModel
from typing import List

class Todo(BaseModel):
    id: int
    item: str

class TodoItem(BaseModel):
    item: str

# 보너스 과제 - 결과를 돌려 줄 때 사용하는 응답 모델 작성
class TodoResponse(BaseModel):
    todos: List[Todo]
    message: str