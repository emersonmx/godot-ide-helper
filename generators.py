#!/usr/bin/env python
# encoding: utf-8

from reader import XmlReader
from writer import GDScriptWriter


class Generator(object):

    def __init__(self):
        super(Generator, self).__init__()

    def make_reader(self):
        pass

    def make_writer(self):
        pass

    def run(self):
        reader = self.make_reader()
        for klass in reader.read():
            writer = self.make_writer()
            writer.write(klass)


class GDScriptGenerator(Generator):

    def __init__(self):
        super(GDScriptGenerator, self).__init__()

    def make_reader(self):
        return XmlReader()

    def make_writer(self):
        return GDScriptWriter()
