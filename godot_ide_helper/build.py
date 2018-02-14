#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import zipfile
import click
import requests

from godot_ide_helper.cli import cli
from godot_ide_helper.utils import *
from godot_ide_helper.versions import GodotVersions

class Downloader:

    def __init__(self, version, cache=True):
        self.dl_url_base = 'https://github.com/godotengine/godot/archive/'
        self.version = version
        self.cache = cache

    def get_download_url(self):
        return os.path.join(self.dl_url_base, get_zip_filename(self.version))

    def run(self):
        output_path = get_zip_filepath(self.version)
        if os.path.exists(output_path) and self.cache:
            click.echo('Using cached version.')
            return

        dl_url = self.get_download_url()
        response = requests.get(dl_url, stream=True)
        with open(output_path, 'wb') as f:
            for chunk in response:
                f.write(chunk)

class Extractor:

    def __init__(self, version):
        self.version = version
        self.cache = cache

    def run(self):
        dl_url = self.get_download_url()
        response = requests.get(dl_url, stream=True)
        with open(output_path, 'wb') as f:
            for chunk in response:
                f.write(chunk)

class Extractor:

    def __init__(self, version):
        self.version = version

    def run(self):
        with zipfile.ZipFile(get_zip_filepath(self.version)) as zp:
            doc_path = get_zip_doc_path(self.version)
            for file in zp.namelist():
                if not file.startswith(doc_path):
                    continue
                zp.extract(file, get_cache_path())

class Builder:

    def __init__(self):
        pass

    def run(self):
        pass

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
        raise click.UsageError('Invalid version')

    click.echo('Downloading version "{}"...'.format(version))
    downloader = Downloader(version, cache)
    downloader.run()

    click.echo('Extracting files...')
    extractor = Extractor(version)
    extractor.run()

    click.echo('Building stubs...')
    builder = Builder()
    builder.run()

    click.echo('Done.')
