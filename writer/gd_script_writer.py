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
        for constant in klass.constants:
            self._write_constant(file, constant)
        if klass.constants:
            self._add_empty_line = True

    def _write_constant(self, file, constant):
        name = constant.name
        value = constant.value
        description = constant.description
        text = 'const ' + name
        if value:
            text += ' = ' + value
        if description:
            text += ' # ' + description
        text += '\n'
        file.write(text)

    def _write_signals(self, file, klass):
        pass

    def _write_members(self, file, klass):
        pass

    def _write_methods(self, file, klass):
        pass

    def write(self, klass):
        self._write_class(klass)
