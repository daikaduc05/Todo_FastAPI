from motor.motor_asyncio import AsyncIOMotorClient,AsyncIOMotorCollection
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
from fastapi.encoders import jsonable_encoder
url = os.getenv("DB_URL")
client = AsyncIOMotorClient(url)
database = client.todo 
users = database.get_collection("users")
tasks = database.get_collection("tasks")

def turn_to_json(document):
    document = {key : (value if key == "password" or key == "share_with" else str(value)) for key, value in document.items()}
    return document
def filter_json(data):
    return {key: value for key, value in data.items() if value is not None}
async def create(collection ,data : dict) -> dict:
    document = await collection.insert_one(data)
    new_document = await collection.find_one({"_id" : document.inserted_id})
    new_document = turn_to_json(new_document)
    return new_document

async def retrieve_filter(collection,data : dict) -> dict:
    document = await collection.find_one(data)
    if document:
        document = turn_to_json(document)
        return document
    return None
async def retrieve_all(collection) -> dict:
    collections = []
    async for c in collection.find():
        collections.append(turn_to_json(c))
    return collections
async def update(collection,id : str,data : dict) -> dict:
    data = filter_json(data)
    document = await collection.update_one({"_id" : ObjectId(id)},{"$set" : data})
    if document:
        document = await collection.find_one({"_id" : ObjectId(id)})
        document = turn_to_json(document)
        return document
    else:
        return None
async def delete(collection,id : str) -> bool:
    if collection.delete_one({"_id" : ObjectId(id)}):
        return True
    else:
        return False

