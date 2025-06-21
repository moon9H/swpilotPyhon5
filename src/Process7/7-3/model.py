# 과정 7 - (문제3) 완전히 작동하는 To-Do

from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    item: str

class TodoItem(BaseModel):
    item: str