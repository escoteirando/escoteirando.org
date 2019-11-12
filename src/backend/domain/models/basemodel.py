class BaseModel:

    def __init__(self, fromDict=None):
        if not isinstance(fromDict,dict):
            return
        
        for k in self.__dict__:
            if k in fromDict:
                self.__dict__[k]=fromDict[k]
                

    def __repr__(self):
        return str(self.__dict__)
