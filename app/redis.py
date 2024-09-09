import redis
r = redis.StrictRedis(host='redis', port=6379, decode_responses=True)