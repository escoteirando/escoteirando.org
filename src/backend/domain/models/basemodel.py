import bson


class BaseModel:

    METADATA = {'_id': bson.ObjectId}

    def __init__(self, fromDict=None):
        self.METADATA.update({'_id': bson.ObjectId})
        self._id = self.NewId()
        if not isinstance(fromDict, dict):
            return

        for k in self.__dict__:
            if k in fromDict:
                if k in self.METADATA:
                    self.__dict__[k] = self.METADATA[k](fromDict[k])
                else:
                    self.__dict__[k] = fromDict[k]

    def __repr__(self):
        return str(self.__dict__)

    def toDict(self):
        ret = {}
        for k in self.__dict__:
            if k in self.METADATA:
                ret[k] = str(self.__dict__[k])
            else:
                ret[k] = self.__dict__[k]

        return ret

    @staticmethod
    def NewId():
        return bson.objectid.ObjectId()
