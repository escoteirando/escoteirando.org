class A:
    static = 1

    @classmethod
    def cm(cls):
        return cls.static


class B(A):

    def test(self):
        return self.cm()


b = B()
print(b.test())
c = B()
c.static = 2
print(b.test())
print(c.test())
