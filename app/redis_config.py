import redis
from rq import Queue
r = redis.StrictRedis(host='cosmosbackend-redis-1', port=6379, decode_responses=True)
queue = Queue(connection=r)