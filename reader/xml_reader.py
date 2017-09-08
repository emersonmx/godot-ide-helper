#!/usr/bin/env python
# encoding: utf-8

from reader.common import Reader

import xml.etree.ElementTree as ET

from objects import *


class XmlReader(Reader):

    def __init__(self):
        super(XmlReader, self).__init__()

    def _get_text(self, el, default=''):
        return el.text if el is not None else default

    def _extract_class(self, element):
        klass = Class()
        klass.name = element.get('name')
        klass.inherits = element.get('inherits')
        klass.brief_description = self._get_text(element.find('brief_description'))
        klass.description = self._get_text(element.find('description'))
        klass.constants = self._extract_constants(element.find('constants'))
        klass.signals = self._extract_signals(element.find('signals'))
        klass.members = self._extract_members(element.find('members'))
        klass.methods = self._extract_methods(element.find('methods'))
        return klass

    def _extract_constants(self, element):
        return []

    def _extract_signals(self, element):
        return []

    def _extract_members(self, element):
        return []

    def _extract_methods(self, element):
        return []

    def read(self):
        tree = ET.parse('classes.xml')
        root = tree.getroot()
        result = []

        i = 0
        for child in root:
            klass = self._extract_class(child)
            result.append(klass)
            i+=1
            if i > 10:
                break

        return result
