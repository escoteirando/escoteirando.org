import glob
import re
import time
from datetime import datetime, timedelta
from hashlib import md5
from os import path

import simplejson as json
from dateutil.tz import tzutc
from infra.log import getLogger
from pymongo import MongoClient

UTC = tzutc()
logger = getLogger("CachedRepository")


class CacheRepository:
    """ Cache persistence """

    CACHE_FILE = 1
    CACHE_MONGO = 2

    D0 = time.mktime(datetime(2019, 1, 1).timetuple())

    def __init__(self, source, time_to_live=60):
        """
        Source: path = File cache
                mongodb://localhost:27017/db/collection
        """
        self.source = source
        self.time_to_live = time_to_live
        self.ok = False
        self.cache_type = 0

        if path.isdir(source):
            self.cache_type = self.CACHE_FILE
            self.ok = True
        else:            

            regex = r"mongodb:\/\/(.*):(\d{4,5})\/(.*)\/(.*)"
            matches = re.finditer(regex, source, re.MULTILINE)

            for matchNum, match in enumerate(matches, start=1):
                if len(match.groups()) == 4:
                    mongouri = "mongodb://" + \
                        match.group(1)+":"+match.group(2)
                    mongodb = match.group(3)
                    mongocol = match.group(4)

                    try:
                        self.client = MongoClient(mongouri)
                        self.collection = self.client[mongodb][mongocol]
                        self.ok = True
                        self.cache_type = self.CACHE_MONGO
                        self.purgeCache()
                    except:
                        self.ok = False

        if self.ok:
            logger.info(f"CachedRepository: {source}")
        else:
            logger.error(f"CachedRepository: {source} UNIDENTIFIED")

    def _errorMethod(self):        
        return None

    def readCache(self, key):
        """Reads contents from cache. Returns None if not exists or expired"""
        if self.cache_type==self.CACHE_FILE:
            return self._fileReadCache(key)
        elif self.cache_type==self.CACHE_MONGO:
            return self._mongoReadCache(key)
        return self._errorMethod()

    def writeCache(self, key, content):
        if self.cache_type==self.CACHE_FILE:
            return self._fileWriteCache(key,content)
        elif self.cache_type==self.CACHE_MONGO:
            return self._mongoWriteCache(key,content)
        return self._errorMethod()

    def purgeCache(self):
        if self.cache_type==self.CACHE_FILE:
            return self._filePurgeCache()
        elif self.cache_type==self.CACHE_MONGO:
            return self._mongoPurgeCache()
        return self._errorMethod()

    def parseKey(self, key):
        if isinstance(key, dict):
            key = str(key)
        elif isinstance(key, str):
            pass
        else:
            key = str(key.__dict__)

        return md5(key.encode('utf-8')).hexdigest()

    def now_minutes(self):
        dn = time.mktime(datetime.now().timetuple())
        return int((dn-self.D0)/60)

    def ttl_limit(self):
        td = timedelta(minutes=self.time_to_live)
        dn = datetime.now() - td
        return time.mktime(dn.timetuple())

    def _filePurgeCache(self):
        for f in glob.iglob(path.join(self.source, "*.cache")):
            mtime = path.getmtime(f)
            life = int((mtime-self.D0)/60)
            if life > self.time_to_live:
                try:
                    unlink(f)
                except:
                    pass

    def _mongoPurgeCache(self):
        try:
            self.collection.delete_many(
                {"creationTime": {"$lt": self.ttl_limit()}})
        except Exception as e:
            print(str(e))

    def _fileReadCache(self, key):
        if path.isdir(self.source):
            key = self.parseKey(key)
            fcache = path.join(self.source, key+'.cache')
            if path.isfile(fcache):
                mtime = path.getmtime(fcache)
                life = int((time.mktime(datetime.now().timetuple())-mtime)/60)
                if life < self.time_to_live:
                    try:
                        return CachedItem(fcache)                        
                    except:
                        pass
                else:
                    try:
                        unlink(fcache)
                    except:
                        pass
        return None

    def _mongoReadCache(self, key):
        try:
            cached = self.collection.find_one({'_id': self.parseKey(key)})
            if cached:
                cached = CachedItem(cached)
                return cached

        except Exception as e:
            print(str(e))

        return None

    def _fileWriteCache(self, key, content):
        if path.isdir(self.source):
            fcache = path.join(self.source, self.parseKey(key)+'.cache')
            try:
                with open(fcache, 'w') as f:
                    f.write(content if isinstance(content, str)
                            else json.dumps(content, default=serialize_date))

                return True
            except Exception as e:
                print(str(e))
        return False

    def _mongoWriteCache(self, key, content):
        try:
            cached = CachedItem(self.parseKey(key), content)
            self.collection.update(spec={"_id": cached.key},
                                   document={
                "_id": cached.key,
                "content": cached.content,
                "creationTime": cached.creationTime
            }, upsert=True)
        except Exception as e:
            print(str(e))


class CachedItem:

    def __init__(self, key_or_file, content=None, creationTime=None):
        if isinstance(key_or_file, str):
            if path.isfile(key_or_file):
                # CachedItem from file
                self.key = path.basename(key_or_file)
                with open(key_or_file, 'r') as f:
                    self.content = f.read()
                    try:
                        j = json.loads(self.content)
                        self.content = j
                    except:
                        pass

                self.creationTime = path.getmtime(key_or_file)
                return
            elif content:
                # CachedItem from content
                self.key = key_or_file
                self.content = content
                if not isinstance(creationTime, float):
                    creationTime = time.mktime(datetime.now().timetuple())
                self.creationTime = creationTime
                return
            else:
                # Try parse json string
                pass
        elif isinstance(key_or_file, dict):
            # Get data from mongo
            if '_id' in key_or_file and 'content' in key_or_file and 'creationTime' in key_or_file:
                self.key = key_or_file['_id']
                self.content = key_or_file['content']
                self.creationTime = key_or_file['creationTime']
                try:
                    j = json.loads(self.content)
                    self.content = j
                except:
                    pass
                return

        self.key = key_or_file
        self.content = content
        self.creationTime = creationTime

    def __repr__(self):
        return str(self.__class__)+" "+str(self.__dict__)


def serialize_date(dt):
    if dt.tzinfo:
        dt = dt.astimezone(UTC).replace(tzinfo=None)
    return dt.isoformat()+"Z"
