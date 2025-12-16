from fastapi import FastAPI,HTTPException
from pydantic  import BaseModel 
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
print(f"URI Loaded: {MONGO_URI is not None}") 

# Do NOT print the actual URI to console for security
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db=client["ahmed's_db"]
ahmed_data = db["ahmed's_coll"]

app = FastAPI()
class ahmed(BaseModel):
    name: str
    phone: int
    city: str
    course: str

@app.post("/ahmed/insert")
async def ahmed_helper(data:ahmed):
    result = await ahmed_data.insert_one(data.dict())
    return str(result.inserted_id)

def ahmed_helper(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


@app.get("/ahmed/getdata")  
async def get_mongo_data():
    items = []  # Empty List variable
    cursor = ahmed_data.find({}) # {}  means Find all documents in collection in mongoDBdatabase. we can define specific parameters.
    async for document in cursor:
        
        items.append(ahmed_helper(document))
    return items