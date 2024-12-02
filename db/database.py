from motor.motor_asyncio import AsyncIOMotorClient,AsyncIOMotorCollection
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
from fastapi.encoders import jsonable_encoder
from settings import db_url,seceret_key

client = AsyncIOMotorClient(db_url)
database = client.todo 

users = database.get_collection("users")
tasks = database.get_collection("tasks")
roles = database.get_collection("roles")
actions = database.get_collection("actions")
resources = database.get_collection("resources")
roles_actions = database.get_collection("role_action")
roles_users = database.get_collection("role_user")

async def create(collection ,data : dict) -> dict:
    document = await collection.insert_one(data)
    new_document = await collection.find_one({"_id" : ObjectId(document.inserted_id)})
    return new_document

async def retrieve_filter(collection,data : dict) -> dict:
    document = await collection.find(data).to_list(None)
    if document:
        return list(document)
    return None

async def retrieve_all(collection) -> dict:
    collections = []
    async for c in collection.find():
        collections.append(c)
    return collections

async def update(collection,id : ObjectId,data : dict) -> dict:
    document = await collection.update_one({"_id" : id},{"$set" : data})
    if document:
        document = await collection.find_one({"_id" : id})
        return document
    else:
        return None
    
async def delete(collection,id : ObjectId) -> bool:
    if collection.delete_one({"_id" : id}):
        return True
    else:
        return False

