class MockRedisPipeline(object):
    """Imitate a redis-python pipeline object so unit tests can run on our Hudson
    CI server without needing a real Redis server."""

    def __init__(self, redis):
        """Initialize the object."""

        self.redis = redis

    def execute(self):
        """Emulate the execute method. All piped commands are executed immediately
        in this mock, so this is a no-op."""

        pass

    def delete(self, key):
        """Emulate a pipelined delete."""

        # Call the MockRedis' delete method
        self.redis.delete(key)
        return self

    def srem(self, key, member):
        """Emulate a pipelined simple srem."""

        self.redis.redis[key].discard(member)
        return self