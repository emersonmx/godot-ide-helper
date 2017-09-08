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
        class_object = Class()
        class_object.name = element.get('name')
        class_object.inherits = element.get('inherits')
        class_object.brief_description = self._get_text(element.find('brief_description'))
        class_object.description = self._get_text(element.find('description'))
        return class_object

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

        return []
