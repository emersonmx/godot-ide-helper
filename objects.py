class Base(object):
    def load_from_xml_element(self, element):
        pass

class Constant(Base):
    def __init__(self):
        super(Constant, self).__init__()

    def load_from_xml_element(self, element):
        pass

class Signal(Base):
    def __init__(self):
        super(Signal, self).__init__()

    def load_from_xml_element(self, element):
        pass

class Member(Base):
    def __init__(self):
        super(Member, self).__init__()

    def load_from_xml_element(self, element):
        pass

class Variable(Base):
    def __init__(self):
        super(Variable, self).__init__()

    def load_from_xml_element(self, element):
        pass

class Argument(Base):
    def __init__(self):
        super(Argument, self).__init__()

    def load_from_xml_element(self, element):
        pass

class Function(Base):
    def __init__(self):
        super(Function, self).__init__()

    def load_from_xml_element(self, element):
        pass

class Class(object):
    def __init__(self):
        super(Class, self).__init__()

    def load_from_xml_element(self, element):
        pass
