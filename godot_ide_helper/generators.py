#!/usr/bin/env python
# encoding: utf-8

from godot_ide_helper.reader import ClassXmlReader
from godot_ide_helper.reader import ClassesXmlReader
from godot_ide_helper.writer import GDScriptWriter


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

    def __init__(self, inputfile, output_path, merged_classes=True):
        super(GDScriptGenerator, self).__init__()

        self._inputfile = inputfile
        self._output_path = output_path
        self._merged_classes = merged_classes

    def make_reader(self):
        if self._merged_classes:
            return ClassesXmlReader(self._inputfile)
        else:
            return ClassXmlReader(self._inputfile)

    def make_writer(self):
        return GDScriptWriter(self._output_path)
