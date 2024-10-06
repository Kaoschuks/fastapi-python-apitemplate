from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=300)  # Example cache with 5 minutes TTL

def query_cache(cache_key: str = None):
    if cache_key in cache:
        return cache[cache_key]
    return None

def save_cache(cache_key: str = None, data = []):
    cache[cache_key] = data

def sqlalchemy_model_to_dict(model_instance):
    return {column.name: getattr(model_instance, column.name) for column in model_instance.__table__.columns}
