import random

from collections import defaultdict
from mockredis.lock import MockRedisLock


class MockRedis(object):
    """Imitate a Redis object so unit tests can run on our Hudson CI server
    without needing a real Redis server."""

    # The 'Redis' store
    redis = defaultdict(dict)
    # The pipeline
    pipe = None

    def __init__(self):
        """Initialize the object."""
        pass

    def type(self, key):
        _type = type(self.redis[key])
        if _type == dict:
            return 'hash'
        elif _type == str:
            return 'string'
        elif _type == set:
            return 'set'
        elif _type == list:
            return 'list'
        return None

    def get(self, key):  # pylint: disable=R0201
        """Emulate get."""

        # Override the default dict
        result = '' if key not in self.redis else self.redis[key]
        return result

    def keys(self, pattern):  # pylint: disable=R0201
        """Emulate keys."""
        import re

        # Make a regex out of pattern. The only special matching character we look for is '*'
        regex = '^' + pattern.replace('*', '.*') + '$'

        # Find every key that matches the pattern
        result = [key for key in self.redis.keys() if re.match(regex, key)]

        return result

    def lock(self, key, timeout=0, sleep=0):  # pylint: disable=W0613
        """Emulate lock."""

        return MockRedisLock(self, key)

    def pipeline(self):
        """Emulate a redis-python pipeline."""
        # Prevent a circular import
        from mockredis.pipeline import MockRedisPipeline

        if self.pipe == None:
            self.pipe = MockRedisPipeline(self.redis)
        return self.pipe

    def delete(self, key):  # pylint: disable=R0201
        """Emulate delete."""

        if key in self.redis:
            del self.redis[key]

    def exists(self, key):  # pylint: disable=R0201
        """Emulate get."""

        return key in self.redis

    def execute(self):
        """Emulate the execute method. All piped commands are executed immediately
        in this mock, so this is a no-op."""

        pass

    def hget(self, hashkey, attribute):  # pylint: disable=R0201
        """Emulate hget."""

        # Return '' if the attribute does not exist
        result = self.redis[hashkey][attribute] if attribute in self.redis[hashkey] \
                 else ''
        return result

    def hgetall(self, hashkey):  # pylint: disable=R0201
        """Emulate hgetall."""

        return self.redis[hashkey]

    def hlen(self, hashkey):  # pylint: disable=R0201
        """Emulate hlen."""

        return len(self.redis[hashkey])

    def hmset(self, hashkey, value):  # pylint: disable=R0201
        """Emulate hmset."""

        # Iterate over every key:value in the value argument.
        for attributekey, attributevalue in value.items():
            self.redis[hashkey][attributekey] = attributevalue

    def hset(self, hashkey, attribute, value):  # pylint: disable=R0201
        """Emulate hset."""

        self.redis[hashkey][attribute] = value

    def lrange(self, key, start, stop):
        """Emulate lrange."""

        # Does the set at this key already exist?
        if key in self.redis:
            # Yes, add this to the list
            return self.redis[key][start:stop + 1]
        else:
            # No, override the defaultdict's default and create the list
            self.redis[key] = list([])

    def rpush(self, key, *args):
        """Emulate rpush."""

        # Does the set at this key already exist?
        if not key in self.redis:
            self.redis[key] = list([])
        for arg in args:
            self.redis[key].append(arg)

    def sadd(self, key, value):  # pylint: disable=R0201
        """Emulate sadd."""

        # Does the set at this key already exist?
        if key in self.redis:
            # Yes, add this to the set
            self.redis[key].add(value)
        else:
            # No, override the defaultdict's default and create the set
            self.redis[key] = set([value])

    def srem(self, key, member):
        """Emulate a srem."""

        self.redis[key].discard(member)
        return self

    def srandmember(self, key):
        """Emulate a srandmember."""
        length = len(self.redis[key])
        rand_index = random.randint(0, length - 1)

        i = 0
        for set_item in self.redis[key]:
            if i == rand_index:
                return set_item

    def smembers(self, key):  # pylint: disable=R0201
        """Emulate smembers."""

        return self.redis[key]

    def flushdb(self):
        self.redis.clear()


def mock_redis_client():
    """Mock common.util.redis_client so we can return a MockRedis object
    instead of a Redis object."""
    return MockRedis()
