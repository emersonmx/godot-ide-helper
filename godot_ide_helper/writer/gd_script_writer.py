#!/usr/bin/env python
# encoding: utf-8

import os
import textwrap

from godot_ide_helper.writer.common import Writer

from urllib.parse import quote

class GDScriptWriter(Writer):

    def __init__(self, output_path):
        super(GDScriptWriter, self).__init__()

        self._output_path = output_path
        self._add_empty_line = False
        self._indent_level = 0
        self._indent_char = ' ' * 4

    def _get_wrapped_lines(self, lines, columns=78):
        return textwrap.wrap(lines, columns)

    def _indent_line(self, line):
        return (self._indent_char * self._indent_level) + line

    def _make_line(self, line='', nl=True):
        result = self._indent_line(line)
        result += '\n' if nl else ''
        return result

    def _write_newline(self, file, prefix=''):
        if self._add_empty_line:
            file.write(prefix + '\n')
        self._add_empty_line = False

    def _get_description_text(self, text):
        result = ''
        count_empty_lines = 0
        for line in [line.strip() for line in text.split('\n')]:
            for l in self._get_wrapped_lines(line):
                line_stripped = l.strip()
                if line_stripped:
                    result += '# ' + line_stripped + '\n'
                else:
                    result += '\n'
        return result

    def _get_arguments_text(self, arguments, force_empty=False):
        result = ''
        argument_list = []
        for arg in arguments:
            argument_list.append('{} {}'.format(arg.type, arg.name))
        if argument_list:
            result += '({})'.format(', '.join(argument_list))
        else:
            result += '()' if force_empty else ''
        return result

    def _write_class(self, klass):
        output_path = os.path.join(self._output_path, '{}.gd'.format(klass.name))
        os.makedirs(self._output_path, exist_ok=True)
        with open(output_path, 'w+') as file:
            self._write_brief_description(file, klass)
            self._write_description(file, klass)
            self._write_class_def(file, klass)
            self._write_constants(file, klass)
            self._write_signals(file, klass)
            self._write_members(file, klass)
            self._write_methods(file, klass)

    def _write_brief_description(self, file, klass):
        if not klass.brief_description.strip():
            return

        raw_text = ''
        description_text = self._get_description_text(klass.brief_description)
        if description_text.strip():
            raw_text += '#\n' + description_text
        file.write(raw_text)

    def _write_description(self, file, klass):
        if not klass.description.strip():
            return

        raw_text = ''
        description_text = self._get_description_text(klass.description)
        if description_text.strip():
            raw_text += '#\n' + description_text
        file.write(raw_text)

    def _write_class_def(self, file, klass):
        raw_line = ''
        if klass.brief_description.strip() or klass.description.strip():
            raw_line += '#\n'
        raw_line += 'class {}'.format(klass.name)
        if klass.inherits:
            raw_line += ' extends {}'.format(klass.inherits)
        raw_line += ':\n'
        file.write(raw_line)
        self._indent_level += 1

    def _write_constants(self, file, klass):
        for idx, constant in enumerate(klass.constants):
            self._write_constant(file, constant, idx == 0)
        if klass.constants:
            self._add_empty_line = True

    def _write_constant(self, file, constant, first):
        raw_text = '\n'
        if constant.description:
            description_text = self._get_description_text(constant.description)
            if description_text.strip():
                raw_text += '#\n' + description_text
                raw_text += '#\n'
        raw_text += 'const ' + constant.name
        raw_text += ' = ' + constant.value if constant.value else ''
        indented_text = ''
        for line in raw_text.split('\n'):
            indented_text += self._make_line(line)
        file.write(indented_text)

    def _write_signals(self, file, klass):
        for idx, signal in enumerate(klass.signals):
            self._write_signal(file, signal, idx == 0)
        if klass.signals:
            self._add_empty_line = True

    def _write_signal(self, file, signal, first):
        raw_text = '\n'
        if signal.description:
            description_text = self._get_description_text(signal.description)
            if description_text.strip():
                raw_text += '#\n' + description_text
                raw_text += '#\n'
        raw_text += 'signal ' + signal.name
        indented_text = ''
        for line in raw_text.split('\n'):
            indented_text += self._make_line(line)
        file.write(indented_text)

    def _write_members(self, file, klass):
        for idx, member in enumerate(klass.members):
            self._write_member(file, member, idx == 0)
        if klass.members:
            self._add_empty_line = True

    def _write_member(self, file, member, first):
        raw_text = '\n'
        if member.description:
            description_text = self._get_description_text(member.description)
            if description_text.strip():
                raw_text += '#\n' + description_text
                raw_text += '#\n'
        raw_text += 'var {} # type: {}'.format(member.name, member.type)
        indented_text = ''
        for line in raw_text.split('\n'):
            indented_text += self._make_line(line)
        file.write(indented_text)

    def _write_methods(self, file, klass):
        for idx, method in enumerate(klass.methods):
            self._write_method(file, method, idx == 0)
        if klass.methods:
            self._add_empty_line = True

    def _write_method(self, file, method, first):
        raw_text = '\n'
        if method.description:
            description_text = self._get_description_text(method.description)
            if description_text.strip():
                raw_text += '#\n' + description_text
                raw_text += '#\n'
            else:
                raw_text += '#\n'
        raw_text += '# {}\n'.format(method.get_doc_link())
        raw_text += '#\n'
        raw_text += 'func ' + method.name
        raw_text += self._get_arguments_text(method.arguments, True)
        raw_text += ':'
        if method.return_type:
            raw_text += ' # returns: {}'.format(method.return_type)
        raw_text += '\n'
        raw_text += self._indent_line('pass')
        indented_text = ''
        for line in raw_text.split('\n'):
            indented_text += self._make_line(line)
        file.write(indented_text)

    def write(self, klass):
        self._write_class(klass)
