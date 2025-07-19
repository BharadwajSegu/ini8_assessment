import redis
from flask import current_app
import json

def get_redis_client():
    return redis.Redis(
        host=current_app.config["REDIS_HOST"],
        port=current_app.config["REDIS_PORT"],
        decode_responses=True
    )

def get_cached_documents():
    client = get_redis_client()
    cached = client.get("document_list")
    return json.loads(cached) if cached else None

def set_cached_documents(data):
    client = get_redis_client()
    client.setex("document_list", current_app.config["CACHE_TTL"], json.dumps(data))

def clear_document_cache():
    client = get_redis_client()
    client.delete("document_list")
