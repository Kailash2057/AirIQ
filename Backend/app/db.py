'''
Handles the MongoDB database connection.

Uses MongoDB with Beanie ODM.

Initializes database connection and document models.
'''

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import os
from .models import Sensor, Reading

# MongoDB connection string from environment
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("MONGODB_DATABASE", "airiq")

# Global client instance
client: AsyncIOMotorClient | None = None

async def init_db():
    """Initialize MongoDB connection and Beanie"""
    global client
    client = AsyncIOMotorClient(MONGODB_URL)
    await init_beanie(
        database=client[DATABASE_NAME],
        document_models=[Sensor, Reading]
    )

async def close_db():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
