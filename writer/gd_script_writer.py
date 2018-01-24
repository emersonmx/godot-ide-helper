#!/usr/bin/env python
# encoding: utf-8

import textwrap

from writer.common import Writer

from urllib.parse import quote

class GDScriptWriter(Writer):

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
        with open('scripts/{}.gd'.format(klass.name), 'w+') as file:
            self._write_class_def(file, klass)
            self._write_newline(file)
            self._write_brief_description(file, klass)
            self._write_newline(file, '#')
            self._write_description(file, klass)
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

    def _write_class_def(self, file, klass):
        file.write('#! class: {}\n'.format(klass.name))
        self._add_empty_line = True

    def _write_brief_description(self, file, klass):
        if not klass.brief_description.strip():
            return
        file.write('# {}\n'.format(klass.brief_description.strip()))
        self._add_empty_line = True

    def _write_description(self, file, klass):
        result = ''
        for line in klass.description.split('\n'):
            result += '\n# '.join(textwrap.wrap(line, 78)).strip()
        result += '\n#'
        result += '\n# {}'.format(klass.get_doc_link())
        if result.strip():
            result = '# ' + result + '\n'
        file.write(result)
        if klass.description.strip():
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
