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

    def _element_or_empty(self, element):
        return element if element is not None else []

    def _extract_arguments(self, arguments):
        result = []
        for argument in arguments:
            result.append(self._extract_argument(argument))

        return sorted(result, key=lambda arg: arg.index)

    def _extract_argument(self, argument):
        obj = Argument()
        obj.name = argument.get('name')
        obj.type = argument.get('type')
        obj.index = argument.get('index')
        return obj

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

    def _extract_constants(self, constants):
        result = []
        for constant in self._element_or_empty(constants):
            result.append(self._extract_constant(constant))
        return result

    def _extract_constant(self, constant):
        obj = Constant()
        obj.name = constant.get('name')
        obj.value = constant.get('value')
        obj.description = self._get_text(constant)
        return obj

    def _extract_signals(self, signals):
        result = []
        for signal in self._element_or_empty(signals):
            result.append(self._extract_signal(signal))
        return result

    def _extract_signal(self, signal):
        obj = Signal()
        obj.name = signal.get('name')
        obj.arguments = self._extract_arguments(signal.findall('argument'))
        obj.description = self._get_text(signal.find('description'))
        return obj

    def _extract_members(self, members):
        result = []
        for member in self._element_or_empty(members):
            result.append(self._extract_member(member))
        return result

    def _extract_member(self, member):
        obj = Member()
        obj.name = member.get('name')
        obj.type = member.get('type')
        obj.description = self._get_text(member)
        return obj

    def _extract_methods(self, element):
        return []

    def read(self):
        tree = ET.parse('classes.xml')

        for child in tree.getroot():
            klass = self._extract_class(child)
            yield klass
