import glob
import os
import time
from datetime import datetime
from hashlib import md5
from app import getLogger

logger = getLogger("Cache")


class Cache:

    def __init__(self, path=None, time_to_live=60):
        if not path:
            path = os.path.join(os.path.dirname(__file__), ".cache")
        self.path = path
        self.ok = False
        self.time_to_live = time_to_live

        if not os.path.isdir(self.path):
            try:
                os.makedirs(self.path)
            except:
                pass

        self.ok = os.path.isdir(self.path)
        if self.ok:
            notbefore = self.now_minutes()-self.time_to_live
            for f in glob.iglob(os.path.join(self.path, "*.cache")):
                nb = os.path.basename(f)[0:10]
                if f.endswith(".cache") and int(nb) < notbefore:
                    os.unlink(f)

    def now_minutes(self):
        dn = time.mktime(datetime.now().timetuple())
        d0 = time.mktime(datetime(2019, 1, 1).timetuple())
        return int((dn-d0)/60)

    def expiredFile(self, fileName):
        notbefore = self.now_minutes()-self.time_to_live
        return os.path.isfile(fileName) and fileName.endswith(".cache") and int(os.path.basename(fileName)[0:10]) < notbefore

    def hashnumber(self, url: str, headers: dict = None):
        if headers is None:
            headers = {}
        return md5((url+str(headers)).encode('utf-8')).hexdigest()

    def readCache(self, url: str, headers: dict = None):
        if not self.ok:
            return False
        hashnumber = self.hashnumber(url, headers)
        cacheFile = None
        for f in glob.iglob(os.path.join(self.path, "??????????."+hashnumber+".cache")):
            if self.expiredFile(f):
                os.unlink(f)
                continue
            cacheFile = f
            break

        if cacheFile and os.path.isfile(cacheFile):
            with open(cacheFile, "r") as f:
                cacheFile = f.read()

        else:
            cacheFile = None

        return cacheFile

    def writeCache(self, url: str, content: str, headers: dict = None):
        if not self.ok:
            return False
        cacheFile = os.path.join(self.path, "{:010d}".format(
            self.now_minutes())+"."+self.hashnumber(url, headers)+".cache")
        try:
            with open(cacheFile, "x") as f:
                f.write(content)

            return cacheFile
        except Exception as write_exception:
            logger.exception("WRITE CACHE ERROR: %s", write_exception)

        return False
