#!/usr/bin/env python
# encoding: utf-8

from writer.common import Writer


class GDScriptWriter(Writer):

    def __init__(self):
        super(GDScriptWriter, self).__init__()

    def write(self, class_object):
        print(class_object)
