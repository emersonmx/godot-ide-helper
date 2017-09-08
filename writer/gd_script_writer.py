#!/usr/bin/env python
# encoding: utf-8

from writer.common import Writer


class GDScriptWriter(Writer):

    def __init__(self):
        super(GDScriptWriter, self).__init__()

    def _write_class(self, klass):
        self._write_constants(klass)
        self._write_signals(klass)
        self._write_members(klass)
        self._write_methods(klass)

    def _write_constants(self, klass):
        pass

    def _write_signals(self, klass):
        pass

    def _write_members(self, klass):
        pass

    def _write_methods(self, klass):
        pass

    def write(self, klass):
        self._write_class(klass)
