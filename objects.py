import urllib.parse

_GODOT_ONLINE_API_URL = 'http://docs.godotengine.org/en/stable/classes'

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
    _URL_TEMPLATE = '{0}/class_{1}.html#class-{2}-{3}'

    def __init__(self):
        super(Method, self).__init__()

        self.name = ''
        self.return_type = ''
        self.arguments = []
        self.description = ''
        self.class_object = None

    def get_doc_link(self):
        klass_name = self.class_object.name.lower()
        klass_anchor_name = klass_name.strip('@').replace('_', '-')
        method_name = self.name.lower().replace('_', '-')
        return self._URL_TEMPLATE.format(_GODOT_ONLINE_API_URL,
                                         urllib.parse.quote(klass_name),
                                         urllib.parse.quote(klass_anchor_name),
                                         urllib.parse.quote(method_name))

class Class(object):
    _URL_TEMPLATE = '{0}/class_{1}.html'

    def __init__(self):
        super(Class, self).__init__()

        self.name = ''
        self.inherits = ''
        self.brief_description = ''
        self.description = ''

        self.constants = []
        self.signals = []
        self.members = []
        self.methods = []

    def get_doc_link(self):
        return self._URL_TEMPLATE.format(_GODOT_ONLINE_API_URL,
                                         urllib.parse.quote(self.name.lower()))

    def __repr__(self):
        result = 'class {}'.format(self.name)
        if self.inherits:
            result += ' extends {}'.format(self.inherits)

        return result
