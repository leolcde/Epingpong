import redis

class RedisMatchQueue:
    def __init__(self, redis_client: redis.Redis, queue_name: str ="match_queue"):
        self.redis_client = redis_client
        self.queue_name = queue_name

    def push(self, user_id: int):
        self.redis_client.rpush(self.queue_name, user_id)

    def pop(self) -> int | None:
        return self.redis_client.lpop(self.queue_name) # type: ignore

    def get_all(self) -> list[int]:
        """Get all items in the queue."""
        if not self.redis_client.exists(self.queue_name):
            return []
        items = self.redis_client.lrange(self.queue_name, 0, -1) # type: ignore
        return [int(item) for item in items] # type: ignore
    def clear(self):
        """Clear the queue."""
        self.redis_client.delete(self.queue_name)
    def contains(self, user_id: int) -> bool:
        """Check if a user is in the queue."""
        return self.redis_client.lrem(self.queue_name, 0, user_id) > 0 # type: ignore
