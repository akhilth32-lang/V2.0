import motor.motor_asyncio
import os

# MongoDB connection (use Render Environment Variable: MONGO_URI)
MONGO_URI = os.getenv("MONGO_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["clashperk"]

def get_collection(name: str):
    return db[name]
