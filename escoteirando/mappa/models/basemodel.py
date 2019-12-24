class BaseModel:

    def __init__(self, fromDict=None):
        if not isinstance(fromDict, dict):
            return

        for prop in self.__dict__:
            if prop in fromDict:
                self.__dict__[prop] = fromDict[prop]
