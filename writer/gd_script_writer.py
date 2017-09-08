#!/usr/bin/env python
# encoding: utf-8

from writer.common import Writer

from urllib.parse import quote

class GDScriptWriter(Writer):

    GODOT_ONLINE_API_URL = 'http://docs.godotengine.org/en/stable/classes/'

    def __init__(self):
        super(GDScriptWriter, self).__init__()

        self._add_empty_line = False

    def _write_newline(self, file, prefix=''):
        if self._add_empty_line:
            file.write(prefix + '\n')
        self._add_empty_line = False

    def _get_description_text(self, text, newline_spaced=True):
        texts = text.split('\n')
        result = ''
        if newline_spaced:
            result += '\n'
        for line in texts:
            result += '# {}\n'.format(line.strip())
        return result

    def _get_arguments_text(self, arguments):
        result = ''
        argument_list = []
        for arg in arguments:
            argument_list.append('{} {}'.format(arg.type, arg.name))
        if argument_list:
            result += '({})'.format(', '.join(argument_list))
        return result

    def _write_class(self, klass):
        with open('scripts/{}.gd'.format(klass.name), 'w+') as file:
            self._write_brief_description(file, klass)
            self._write_newline(file, '#')
            self._write_description_url(file, klass)
            self._write_newline(file)
            self._write_inherits(file, klass)
            self._write_newline(file)
            self._write_constants(file, klass)
            self._write_newline(file)
            self._write_signals(file, klass)
            self._write_newline(file)
            self._write_members(file, klass)
            self._write_newline(file)
            self._write_methods(file, klass)

    def _write_brief_description(self, file, klass):
        if not klass.brief_description.strip():
            return
        file.write('# {}\n'.format(klass.brief_description.strip()))
        self._add_empty_line = True

    def _write_description_url(self, file, klass):
        url = '{}class_{}.html'.format(self.GODOT_ONLINE_API_URL,
            quote(klass.name.lower()))
        file.write('# {}\n'.format(url))
        self._add_empty_line = True

    def _write_inherits(self, file, klass):
        if not klass.inherits:
            return
        file.write('extends {}\n'.format(klass.inherits))
        self._add_empty_line = True

    def _write_constants(self, file, klass):
        for idx, constant in enumerate(klass.constants):
            self._write_constant(file, constant, idx == 0)
        if klass.constants:
            self._add_empty_line = True

    def _write_constant(self, file, constant, first):
        text = ''
        if constant.description:
            text += self._get_description_text(constant.description, not first)
        text += 'const ' + constant.name
        if constant.value:
            text += ' = ' + constant.value
        text += '\n'
        file.write(text)

    def _write_signals(self, file, klass):
        for idx, signal in enumerate(klass.signals):
            self._write_signal(file, signal, idx == 0)
        if klass.signals:
            self._add_empty_line = True

    def _write_signal(self, file, signal, first):
        text = ''
        if signal.description:
            text += self._get_description_text(signal.description, not first)
        text += 'signal ' + signal.name
        text += self._get_arguments_text(signal.arguments)
        text += '\n'
        file.write(text)

    def _write_members(self, file, klass):
        for idx, member in enumerate(klass.members):
            self._write_member(file, member, idx == 0)
        if klass.members:
            self._add_empty_line = True

    def _write_member(self, file, member, first):
        text = ''
        if member.description:
            text += self._get_description_text(member.description, not first)
        text += 'var {} # {}'.format(member.name, member.type)
        text += '\n'
        file.write(text)

    def _write_methods(self, file, klass):
        pass

    def write(self, klass):
        self._write_class(klass)
