#!/usr/bin/env python
# encoding: utf-8

from xml.dom import *
from urllib.parse import quote

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
