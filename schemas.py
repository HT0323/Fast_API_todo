from pydantic import BaseModel


class Todo(BaseModel):
    id: str
    title: str
    description: str


class TodoBody(BaseModel):
    title: str
    description: str


class SuccessMsg(BaseModel):
    message: str
