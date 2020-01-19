from mappa.repositories import CachedItem, CacheRepository
from datetime import datetime

cr = CacheRepository("mongodb://localhost:27017/escoteirando/cache")
content = {"nome": "Guionardo", "idade": 42, "hora": datetime.now()}
cr.writeCache("12345", content)

c2 = cr.readCache("12345")
print(c2)

cf = CacheRepository("./")
cf.writeCache("12345", content)
c2 = cf.readCache("12345")
print(c2)
