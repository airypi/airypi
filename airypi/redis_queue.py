import redis
from flask import g, session
import device
import message_queue

import os

class RedisMQ(message_queue.MessageQueue):
    redis = None
    
    def push(self, data):
        RedisMQ.redis.lpush(self.queue_key, data)
        RedisMQ.redis.ltrim(self.queue_key, 0, self.max_size)

    def pop(self):
        return RedisMQ.redis.rpop(self.queue_key)

    def clear(self):
        RedisMQ.redis.delete(self.queue_key)