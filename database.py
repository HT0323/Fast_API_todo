from decouple import config
from typing import Union
import motor.motor_asyncio

MONGO_API_KEY = config('MONGO_API_KEY')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
database = client.API_DB
collection_todo = database.todo
collection_user = database.user


def todo_serializer(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo["description"]
    }


async def db_create_todo(data: dict) -> Union[dict, bool]:
    print(data)
    todo = await collection_todo.insert_one(data)
    new_todo = await collection_todo.find_one({"_id": todo.inserted_id})
    if new_todo:
        return todo_serializer(new_todo)
    return False
