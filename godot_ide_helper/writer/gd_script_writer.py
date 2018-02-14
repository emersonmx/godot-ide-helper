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

    def _make_line(self, line='', nl=True):
        result = (self._indent_char * self._indent_level) + line
        result += '\n' if nl else ''
        return result

    def _write_newline(self, file, prefix=''):
        if self._add_empty_line:
            file.write(prefix + '\n')
        self._add_empty_line = False

    def _get_description_text(self, text, newline_spaced=True):
        texts = text.split('\n')
        result = ''
        if newline_spaced:
            result += '\n'

        count_empty_lines = 0
        for line in texts:
            if len(line.strip()) == 0:
                count_empty_lines += 1
            wrapped_text = '\n# '.join(textwrap.wrap(line, 78))
            new_line = '# {}'.format(wrapped_text.strip())
            result += new_line.strip() + '\n'

        if count_empty_lines == len(texts):
            return '\n' if newline_spaced else ''

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
            # self._write_newline(file)
            # self._write_signals(file, klass)
            # self._write_newline(file)
            # self._write_members(file, klass)
            # self._write_newline(file)
            # self._write_methods(file, klass)

    def _write_brief_description(self, file, klass):
        if not klass.brief_description.strip():
            return
        wlines = self._get_wrapped_lines(klass.brief_description.strip())
        raw_text = ''
        raw_text += '\n'.join(['# ' + line.strip() for line in wlines])
        if raw_text.strip():
            raw_text = '#\n' + raw_text + '\n'
            file.write(raw_text)

    def _write_description(self, file, klass):
        result = ''
        raw_text = ''
        for line in klass.description.split('\n'):
            wlines = self._get_wrapped_lines(line)
            raw_text += '\n'.join(['# ' + line.strip() for line in wlines])
        if raw_text.strip():
            result += '#\n' + raw_text + '\n'
            result += '#\n'
        file.write(result)

    def _write_class_def(self, file, klass):
        raw_line = 'class {}'.format(klass.name)
        if klass.inherits:
            raw_line += ' extends {}'.format(klass.inherits)
        raw_line += ':\n'
        file.write(self._make_line(raw_line))
        self._indent_level += 1

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
        text += 'var {} # type: {}'.format(member.name, member.type)
        text += '\n'
        file.write(text)

    def _write_methods(self, file, klass):
        for idx, method in enumerate(klass.methods):
            self._write_method(file, method, idx == 0)
        if klass.methods:
            self._add_empty_line = True

    def _write_method(self, file, method, first):
        text = ''
        if method.description:
            text += self._get_description_text(method.description, not first)
        text += '# {}\n'.format(method.get_doc_link())
        text += '#\n'
        text += 'func ' + method.name
        text += self._get_arguments_text(method.arguments, True)
        text += ':'
        if method.return_type:
            text += ' # returns: {}'.format(method.return_type)
        text += '\n'
        text += '    pass\n'
        file.write(text)

    def write(self, klass):
        self._write_class(klass)
