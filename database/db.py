from pymongo import MongoClient
import asyncio

class Database:
    def __init__(self, mongodb_uri):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client["tide_security_bot"]
        self.configs = self.db["configs"]
        self.logs = self.db["logs"]
        self.reputation = self.db["reputation"]

    async def get_config(self, guild_id):
        return self.configs.find_one({"guild_id": str(guild_id)}) or {}

    async def update_config(self, guild_id, config):
        self.configs.update_one(
            {"guild_id": str(guild_id)},
            {"$set": config},
            upsert=True
        )

    async def log_action(self, guild_id, message):
        self.logs.insert_one({
            "guild_id": str(guild_id),
            "message": message,
            "timestamp": asyncio.get_event_loop().time()
        })

    async def get_spam_count(self, guild_id):
        return self.logs.count_documents({"guild_id": str(guild_id)})

    async def get_reputation(self, user_id, guild_id):
        return self.reputation.find_one({"user_id": str(user_id), "guild_id": str(guild_id)}) or {"score": 0}

    async def update_reputation(self, user_id, guild_id, score_change):
        self.reputation.update_one(
            {"user_id": str(user_id), "guild_id": str(guild_id)},
            {"$inc": {"score": score_change}},
            upsert=True
        )