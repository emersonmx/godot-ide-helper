#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click

@click.group()
def cli():
    pass

from godot_ide_helper.versions import versions
from godot_ide_helper.build import build
