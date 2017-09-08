#!/usr/bin/env python
# encoding: utf-8

import sys
import textwrap

from xml.dom import *
from xml.dom.minidom import parse
from urllib.parse import quote


class GodotXmlReader(object):

    def __init__(self, klass):
        self._klass = klass

    def _getAttr(self, el, attr, default=None):
        return el.getAttribute(attr) if el.hasAttribute(attr) else default

    def extract_name(self):
        return self._getAttr(self._klass, 'name')

    def extract_inherits(self):
        return self._getAttr(self._klass, 'inherits')

    def _wrapped_comment(self, text):
        result = ''
        for line in textwrap.wrap(text, 80):
            result += '# {}\n'.format(line)
        return result

    def extract_element_text(self, nodes):
        text = ''
        for node in nodes:
            if node.nodeType != Node.ELEMENT_NODE:
                continue
            for child in node.childNodes:
                if child.nodeType != Node.TEXT_NODE:
                    continue
                text += child.data.strip()
        return text

    def extract_brief_description(self):
        return self.extract_element_text(self._klass.getElementsByTagName('brief_description'))

    def extract(self):
        raw_class = {}
        raw_class['name'] = self.extract_name()
        raw_class['inherits'] = self.extract_inherits()
        raw_class['brief_description'] = self.extract_brief_description()

        return raw_class


class GDScriptWriter(object):

    GODOT_ONLINE_API_URL = 'http://docs.godotengine.org/en/stable/classes/'

    def __init__(self, klass):
        self._klass = klass

    def _write_brief_description(self, file):
        if 'brief_description' not in self._klass:
            return
        if not self._klass['brief_description']:
            return
        file.write('# {}\n'.format(self._klass['brief_description']))

    def _write_description_url(self, file):
        if 'brief_description' in self._klass and self._klass['brief_description']:
            file.write('#\n')
        url = '{}class_{}.html'.format(self.GODOT_ONLINE_API_URL,
            quote(self._klass['name'].lower()))
        file.write('# {}\n'.format(url))

    def _write_inherits(self, file):
        if 'inherits' not in self._klass:
            return
        if not self._klass['inherits']:
            return
        file.write('\n')
        file.write('extends {}\n'.format(self._klass['inherits']))

    def _write_constants(self, file):
        pass

    def _write_signals(self, file):
        pass

    def _write_members(self, file):
        pass

    def _write_methods(self, file):
        pass

    def write_class(self):
        with open('scripts/{}.gd'.format(self._klass['name']), 'w+') as file:
            self._write_brief_description(file)
            self._write_description_url(file)
            self._write_inherits(file)
            self._write_constants(file)
            self._write_signals(file)
            self._write_members(file)
            self._write_methods(file)


class XmlToGDScripts(object):

    def __init__(self):
        super(XmlToGDScripts, self).__init__()

        self.dom = self.load_dom()
        self.doc = self.dom.documentElement

    def load_dom(self):
        return parse('classes.xml')

    def run(self):
        count = 0
        for klass in self.doc.childNodes:
            if klass.nodeType != Node.ELEMENT_NODE:
                continue
            reader = GodotXmlReader(klass)
            raw_class = reader.extract()
            writer = GDScriptWriter(raw_class)
            writer.write_class()
            count += 1
            if count > 5:
                break

def main():
    converter = XmlToGDScripts()
    sys.exit(converter.run())

if __name__ == "__main__":
    main()
