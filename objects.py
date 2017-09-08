class Constant(object):
    def __init__(self):
        super(Constant, self).__init__()

        self.name = ''
        self.value = ''
        self.description = ''

class Signal(object):
    def __init__(self):
        super(Signal, self).__init__()

        self.name = ''
        self.arguments = []
        self.description = ''

class Member(object):
    def __init__(self):
        super(Member, self).__init__()

        self.name = ''
        self.type = ''
        self.description = ''

class Argument(object):
    def __init__(self):
        super(Argument, self).__init__()

        self.name = ''
        self.index = ''
        self.type = ''

class Method(object):
    def __init__(self):
        super(Method, self).__init__()

        self.name = ''
        self.return_type = ''
        self.argurments = []
        self.description = ''

class Class(object):
    def __init__(self):
        super(Class, self).__init__()

        self.name = ''
        self.inherits = ''
        self.brief_description = ''
        self.descriptions = ''
