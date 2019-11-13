class BaseModel:

    def __init__(self, content):
        if isinstance(content, dict):
            self.content = content
        else:
            self.content = None
        self.error = None

    def get(self, names):
        if not isinstance(self.content, dict):
            self.error = "Invalid content: not a dict"
            return None
        ret = []
        for name in names:
            if name not in self.content:
                self.error = f"Invalid content: property '{name}' not found"
                return None
            ret.append(self.content[name])
        self.content = None
        return ret

    def __repr__(self):
        return str(self.__dict__)

    @property
    def ok(self):
        return self.content is None
