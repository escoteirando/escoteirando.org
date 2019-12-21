import datetime
import json
import os
import time


class CacheItem:
    """ Item cached, saved in file """

    DATE_FORMAT = ''

    def __init__(self, filename, just_validate: bool = False):
        max_age = -1
        payload = None
        old = False
        self.valid = False
        if os.path.isfile(filename):
            with open(filename) as f:
                max_age = float(f.readline())
                if max_age > time.time():
                    payload = f.read()
                    self.valid = True
                    if just_validate:
                        return
                else:
                    old = True
        if old:
            os.unlink(filename)
            if just_validate:
                return

        self.max_age = max_age
        self.payload = self.parse_payload(payload)
        self.filename = filename

    def set(self, payload, max_age: int):
        """ Defines payload and max age of item.

        :param payload: cached object
        :param max_age: timestamp 
        :returns: self object
        :rtype: CacheItem"""

        self.payload = payload
        self.max_age = max_age
        return self

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(str(self.max_age)+'\n')
            f.write(json.dumps(self.payload, default=self._encoder))

    def parse_payload(self, payload):
        if type(payload) in [str, bytes, bytearray]:
            return json.loads(payload, object_hook=self._decoder)
        return None

    def _encoder(self, obj):
        if isinstance(obj, datetime.datetime):            
            return {'__datetime__': obj.strftime('%Y-%m-%dT%H:%M:%S.%f')}
        return str(obj)

    def _decoder(self, obj):
        if '__datetime__' in obj:
            return datetime.datetime.strptime(obj['__datetime__'], '%Y-%m-%dT%H:%M:%S.%f')
        return obj
