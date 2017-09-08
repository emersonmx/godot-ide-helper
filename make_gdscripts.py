#!/usr/bin/env python
# encoding: utf-8

import sys
import textwrap

from xml.dom import *
from xml.dom.minidom import parse


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

    def extract(self):
        raw_class = {}
        raw_class['name'] = self.extract_name()
        raw_class['inherits'] = self.extract_inherits()
        brief_description = self.extract_element_text(
            self._klass.getElementsByTagName('brief_description'))
        if len(brief_description.strip()) > 0:
            raw_class['brief_description'] = brief_description

        return raw_class


class GDScriptWriter(object):

    GODOT_ONLINE_API_URL = 'http://docs.godotengine.org/en/stable/classes/'

    def __init__(self):
        pass

    def write_brief_description(self, file, klass):
        if 'brief_description' not in klass:
            return
        file.write('# {}\n'.format(klass['brief_description']))

    def write_description_url(self, file, klass):
        if 'brief_description' not in klass:
            file.write('#\n')
        url = '{}class_{}.html'.format(self.GODOT_ONLINE_API_URL, klass['name'].lower())
        file.write('# {}\n'.format(url))

    def write_inherits(self, file, klass):
        if 'inherits' not in klass:
            return
        if not klass['inherits']:
            return
        file.write('extends {}\n'.format(klass['inherits']))

    def write_file(self, klass):
        with open('scripts/{}.gd'.format(klass['name']), 'w+') as file:
            self.write_brief_description(file, klass)
            self.write_description_url(file, klass)
            self.write_inherits(file, klass)


class XmlToGDScripts(object):

    def __init__(self):
        super(XmlToGDScripts, self).__init__()

        self.dom = self.load_dom()
        self.doc = self.dom.documentElement
        self.writer = GDScriptWriter()

    def load_dom(self):
        return parse('classes.xml')

    def run(self):
        count = 0
        for klass in self.doc.childNodes:
            if klass.nodeType != Node.ELEMENT_NODE:
                continue
            reader = GodotXmlReader(klass)
            raw_class = reader.extract()
            self.writer.write_file(raw_class)
            count += 1
            if count > 5:
                break

def main():
    converter = XmlToGDScripts()
    sys.exit(converter.run())

if __name__ == "__main__":
    main()
