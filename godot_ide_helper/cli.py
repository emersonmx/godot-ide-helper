#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click

def get_cache_path():
    cache_path = os.path.abspath('cache')
    home_path = os.environ.get('HOME')
    if home_path:
        cache_path = os.path.join(home_path, '.cache/godot_ide_helper')
    os.makedirs(cache_path, exist_ok=True)
    return cache_path

@click.group()
def cli():
    pass

from godot_ide_helper.versions import versions
from godot_ide_helper.build import build
