#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import click
import requests

from zipfile import ZipFile

from godot_ide_helper.cli import cli
from godot_ide_helper.utils import *
from godot_ide_helper.versions import GodotVersions
from godot_ide_helper import generators
from godot_ide_helper.reader import *


class Downloader:

    def __init__(self, version, cache=True):
        self._dl_url_base = 'https://github.com/godotengine/godot/archive/'
        self._version = version
        self._cache = cache

    def get_download_url(self):
        return os.path.join(self._dl_url_base, get_zip_filename(self._version))

    def run(self):
        output_path = get_zip_filepath(self._version)
        if os.path.exists(output_path) and self._cache:
            click.echo('Using cached version.')
            return

        dl_url = self.get_download_url()
        response = requests.get(dl_url, stream=True)
        with open(output_path, 'wb') as f:
            for chunk in response:
                f.write(chunk)


class Extractor:

    def __init__(self, version):
        self._version = version

    def run(self):
        zip_extract_path = get_zip_extraction_path(self._version)
        if os.path.exists(zip_extract_path):
            shutil.rmtree(zip_extract_path)

        with ZipFile(get_zip_filepath(self._version)) as zp:
            doc_path = get_zip_doc_relpath(self._version)
            for file in zp.namelist():
                if not file.startswith(doc_path):
                    continue
                zp.extract(file, get_cache_path())


class Builder:

    def __init__(self, generator, version):
        self._generator = generator
        self._version = version

    def make_generator(self):
        class_name = self._generator + 'Generator'
        return getattr(generators, class_name)

    def build_legacy(self):
        cls = self.make_generator()
        inputfile = os.path.join(get_zip_doc_path(self._version), 'base/classes.xml')
        output_path = get_scripts_path(self._version)
        app = cls(inputfile, output_path)
        app.run()

    def build(self):
        classes_path = os.path.join(get_zip_doc_path(self._version), 'classes')
        for class_file in os.listdir(classes_path):
            cls = self.make_generator()
            inputfile = os.path.join(classes_path, class_file)
            output_path = get_scripts_path(self._version)
            app = cls(inputfile, output_path, False)
            app.run()

    def run(self):
        if self._version < '3.0-stable':
            self.build_legacy()
        else:
            self.build()


class Packer:

    def __init__(self, version):
        self._version = version

    def run(self):
        script_path = get_scripts_path(self._version)
        with ZipFile('godot-{}-scripts.zip'.format(self._version), mode='w') as zp:
            for file in os.listdir(script_path):
                zp.write(os.path.join(script_path, file), file)

@cli.command()
@click.option('--generator', default='GDScript', type=click.Choice(['GDScript']),
              help='Generator to build scripts.')
@click.option('--cache/--no-cache', default=True, help='Enable / Disable build cache.')
@click.argument('version', default='stable')
def build(generator, cache, version):
    '''Build IDE helper files.

    VERSION can be [stable|x.y.z-stable]
    '''
    godot_versions = GodotVersions()
    versions = godot_versions.list()
    if version == 'stable':
        version = next(x for x in versions if 'stable' in x)
    elif version not in versions:
        raise click.UsageError('Invalid version.')

    click.echo('Downloading version "{}"...'.format(version))
    downloader = Downloader(version, cache)
    downloader.run()

    click.echo('Extracting files...')
    extractor = Extractor(version)
    extractor.run()

    click.echo('Building stubs...')
    builder = Builder(generator, version)
    builder.run()

    click.echo('Packing scripts...')
    packer = Packer(version)
    packer.run()

    click.echo('Done.')
