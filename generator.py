#!/usr/bin/env python
# encoding: utf-8

import sys
import textwrap

from xml.dom import *
from xml.dom.minidom import parse

from reader import XmlReader
from writer import GDScriptWriter



class Generator(object):

    def __init__(self):
        super(Generator, self).__init__()

        self.dom = self.load_dom()
        self.doc = self.dom.documentElement

    def load_dom(self):
        return parse('classes.xml')

    def run(self):
        count = 0
        for klass in self.doc.childNodes:
            if klass.nodeType != Node.ELEMENT_NODE:
                continue
            reader = XmlReader(klass)
            raw_class = reader.extract()
            writer = GDScriptWriter(raw_class)
            writer.write_class()
            count += 1
            if count > 10:
                break

def main():
    generator = Generator()
    sys.exit(generator.run())

if __name__ == "__main__":
    main()
