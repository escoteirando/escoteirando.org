import glob
import re
import time
from datetime import datetime, timedelta
from hashlib import md5
from os import path, unlink

import simplejson as json
from dateutil.tz import tzutc
from pymongo import MongoClient

from infra.log import getLogger

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
        if self.cache_type == self.CACHE_FILE:
            return self._fileReadCache(key)
        elif self.cache_type == self.CACHE_MONGO:
            return self._mongoReadCache(key)
        return self._errorMethod()

    def writeCache(self, key, content):
        if self.cache_type == self.CACHE_FILE:
            return self._fileWriteCache(key, content)
        elif self.cache_type == self.CACHE_MONGO:
            return self._mongoWriteCache(key, content)
        return self._errorMethod()

    def purgeCache(self):
        if self.cache_type == self.CACHE_FILE:
            return self._filePurgeCache()
        elif self.cache_type == self.CACHE_MONGO:
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
                except OSError:
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
                    return CachedItem(file=fcache)

                else:
                    try:
                        unlink(fcache)
                    except OSError:
                        pass
        return None

    def _mongoReadCache(self, key):
        try:
            cached = self.collection.find_one({'_id': self.parseKey(key)})
            if cached:
                cached = CachedItem(fromObject=cached)
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
            cached = CachedItem(key=self.parseKey(key), content=content)
            ret = self.collection.update(spec={"_id": cached.key},
                                         document={
                "_id": cached.key,
                "content": cached.content,
                "creationTime": cached.creationTime
            }, upsert=True)
            return ret['nModified'] > 0 or ret['upserted']
        except Exception as e:
            print(str(e))
        return False


class CachedItem:

    key: str = None
    content: object = None
    creationTime: float = None

    def __init__(self, **kvargs):
        """ file (str)= File name

        content (serializable object)

        creationTime (DateTime or float timestamp)

        fromObject (from another CacheItem or dict)
        """

        if 'fromObject' in kvargs:
            # Get data from mongo
            keys = ['_id', 'content', 'creationTime']
            obj = kvargs['fromObject']
            if len([k for k in obj if k in keys]) == 3:
                self.key = obj['_id']
                self.content = obj['content']
                self.creationTime = obj['creationTime']
                try:
                    j = json.loads(self.content)
                    self.content = j
                except:
                    pass
                return

        if 'file' in kvargs and isinstance(kvargs['file'], str):
            # CachedItem from file
            file = kvargs['file']
            if path.isfile(file):
                self.key = path.basename(file)
                with open(file, 'r') as f:
                    self.content = f.read()
                    try:
                        j = json.loads(self.content)
                        self.content = j
                    except:
                        pass
                self.creationTime = path.getmtime(file)
                return

        if 'key' in kvargs and kvargs['key']:
            self.key = str(kvargs['key'])

        if 'content' in kvargs and kvargs['content']:
            self.content = kvargs['content']

        if 'creationTime' in kvargs:
            creationTime = kvargs['creationTime']
            if isinstance(creationTime, datetime):
                self.creationTime = time.mktime(creationTime.timetuple())
            elif isinstance(creationTime, float):
                self.creationTime = creationTime

        else:
            self.creationTime = time.mktime(datetime.now().timetuple())

    def __dict__(self):
        return {
            'key': self.key,
            'content': self.content,
            'creationTime': self.creationTime
        }

    def __repr__(self):
        return str(self.__class__)+" "+str(self.__dict__)

    def __str__(self):
        return repr(self)


def serialize_date(dt):
    if dt.tzinfo:
        dt = dt.astimezone(UTC).replace(tzinfo=None)
    return dt.isoformat()+"Z"
