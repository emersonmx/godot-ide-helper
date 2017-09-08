#!/usr/bin/env python
# encoding: utf-8

from xml.dom import *


class XmlReader(object):

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
