#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def get_cache_path():
    cache_path = os.path.abspath('cache')
    home_path = os.environ.get('HOME')
    if home_path:
        cache_path = os.path.join(home_path, '.cache/godot_ide_helper')
    os.makedirs(cache_path, exist_ok=True)
    return cache_path

def get_zip_extraction_path(version):
    cache_path = get_cache_path()
    return os.path.join(cache_path, 'godot-{}'.format(version))

def get_zip_filename(version):
    return '{}.zip'.format(version)

def get_zip_filepath(version):
    cache_path = get_cache_path()
    return os.path.join(cache_path, get_zip_filename(version))

def get_zip_doc_relpath(version):
    return 'godot-{}/doc/'.format(version)

def get_zip_doc_path(version):
    cache_path = get_cache_path()
    return os.path.join(cache_path, get_zip_doc_relpath(version))
