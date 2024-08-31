
from redis55 import Redis

r = Redis()

r.set('k2',3)

print(r.get('k2'))
