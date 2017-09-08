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

    def _get_attr(self, el, attr, default=None):
        return el.getAttribute(attr) if el.hasAttribute(attr) else default

    def _get_text_from_element(self, el):
        text = ''
        for node in el.childNodes:
            if node.nodeType != Node.TEXT_NODE:
                continue
            text += node.data.strip()
        return text

    def _get_text_from_elements(self, nodes):
        text = ''
        for node in nodes:
            if node.nodeType != Node.ELEMENT_NODE:
                continue
            for child in node.childNodes:
                if child.nodeType != Node.TEXT_NODE:
                    continue
                text += child.data.strip()
        return text

    def extract_name(self):
        return self._get_attr(self._klass, 'name')

    def extract_inherits(self):
        return self._get_attr(self._klass, 'inherits')

    def _wrapped_comment(self, text):
        result = ''
        for line in textwrap.wrap(text, 80):
            result += '# {}\n'.format(line)
        return result

    def extract_brief_description(self):
        return self._get_text_from_elements(
            self._klass.getElementsByTagName('brief_description'))

    def extract_constants(self):
        constants = []
        for e in self._klass.getElementsByTagName('constants'):
            for c in e.childNodes:
                if c.nodeType != Node.ELEMENT_NODE:
                    continue
                constants.append(self.extract_constant(c))
        return constants

    def extract_constant(self, c):
        constant = {}
        constant['name'] = self._get_attr(c, 'name')
        constant['value'] = self._get_attr(c, 'value')
        constant['description'] = self._get_text_from_element(c)
        return constant

    def extract_signals(self):
        signals = []
        for e in self._klass.getElementsByTagName('signals'):
            for s in e.childNodes:
                if s.nodeType != Node.ELEMENT_NODE:
                    continue
                signals.append(self.extract_signal(s))
        return signals

    def extract_signal(self, s):
        signal = {}
        signal['name'] = self._get_attr(s, 'name')
        signal['arguments'] = self._extract_signal_arguments(s.getElementsByTagName('argument'))
        signal['description'] = self._get_text_from_elements(s.getElementsByTagName('description'))
        return signal

    def _extract_signal_arguments(self, arguments):
        result = []
        for a in arguments:
            if a.nodeType != Node.ELEMENT_NODE:
                continue
            result.append(self._extract_signal_argument(a))
        return sorted(result, key=lambda arg: arg['index'])

    def _extract_signal_argument(self, a):
        argument = {}
        argument['name'] = self._get_attr(a, 'name')
        argument['index'] = self._get_attr(a, 'index')
        argument['type'] = self._get_attr(a, 'type')
        return argument

    def extract(self):
        raw_class = {}
        raw_class['name'] = self.extract_name()
        raw_class['inherits'] = self.extract_inherits()
        raw_class['brief_description'] = self.extract_brief_description()
        raw_class['constants'] = self.extract_constants()
        raw_class['signals'] = self.extract_signals()

        return raw_class


class GDScriptWriter(object):

    GODOT_ONLINE_API_URL = 'http://docs.godotengine.org/en/stable/classes/'

    def __init__(self, klass):
        self._klass = klass
        self._add_empty_line = False

    def _write_newline(self, file, prefix=''):
        if self._add_empty_line:
            file.write(prefix + '\n')
        self._add_empty_line = False

    def _write_brief_description(self, file):
        if 'brief_description' not in self._klass:
            return
        if not self._klass['brief_description']:
            return
        file.write('# {}\n'.format(self._klass['brief_description']))
        self._add_empty_line = True

    def _write_description_url(self, file):
        url = '{}class_{}.html'.format(self.GODOT_ONLINE_API_URL,
            quote(self._klass['name'].lower()))
        file.write('# {}\n'.format(url))
        self._add_empty_line = True

    def _write_inherits(self, file):
        if 'inherits' not in self._klass:
            return
        if not self._klass['inherits']:
            return
        file.write('extends {}\n'.format(self._klass['inherits']))
        self._add_empty_line = True

    def _write_constants(self, file):
        for constant in self._klass['constants']:
            self._write_constant(file, constant)
        if self._klass['constants']:
            self._add_empty_line = True

    def _write_constant(self, file, constant):
        name = constant['name']
        value = constant['value']
        description = constant['description']
        text = 'const ' + name
        if value:
            text += ' = ' + value
        if description:
            text += ' # ' + description
        text += '\n'
        file.write(text)

    def _write_signals(self, file):
        for signal in self._klass['signals']:
            self._write_signal(file, signal)
        if self._klass['signals']:
            self._add_empty_line = True

    def _write_signal(self, file, signal):
        name = signal['name']
        arguments = signal['arguments']
        description = signal['description']
        text = 'signal ' + name

        argument_list = []
        for arg in arguments:
            argument_list.append('{} {}'.format(arg['type'], arg['name']))
        if argument_list:
            text += '({})'.format(', '.join(argument_list))

        if description:
            text += ' # {}'.format(description)

        text += '\n'
        file.write(text)

    def _write_members(self, file):
        pass

    def _write_methods(self, file):
        pass

    def write_class(self):
        with open('scripts/{}.gd'.format(self._klass['name']), 'w+') as file:
            self._write_brief_description(file)
            self._write_newline(file, '#')
            self._write_description_url(file)
            self._write_newline(file)
            self._write_inherits(file)
            self._write_newline(file)
            self._write_constants(file)
            self._write_newline(file)
            self._write_signals(file)
            self._write_newline(file)
            self._write_members(file)
            self._write_newline(file)
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
            if count > 10:
                break

def main():
    converter = XmlToGDScripts()
    sys.exit(converter.run())

if __name__ == "__main__":
    main()
