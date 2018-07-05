class a:
    def __init__(self, **kwargs):
        self.a(**kwargs)

    def a(self, **kwargs):
        print(kwargs.get('config'))

class b(a):
    def __init__(self, **kwargs):
        super(b, self).__init__(**kwargs)
        self.a(**kwargs)

bExtendsA = b(config="database-config.json")