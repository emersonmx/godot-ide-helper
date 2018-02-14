#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click
import requests

from godot_ide_helper.cli import cli, get_cache_path
from godot_ide_helper.versions import GodotVersions

class Downloader:

    def __init__(self, version, use_cache=True):
        self.dl_url_base = 'https://github.com/godotengine/godot/archive/'
        self.version = version
        self.use_cache = use_cache

    def get_download_url(self):
        return os.path.join(self.dl_url_base, self.zip_filename())

    def zip_filename(self):
        return '{}.zip'.format(self.version)

    def get_output_path(self):
        cache_path = get_cache_path()
        return os.path.join(cache_path, self.zip_filename())

    def run(self):
        output_path = self.get_output_path()
        if os.path.exists(output_path) and self.use_cache:
            return

        dl_url = self.get_download_url()
        response = requests.get(dl_url, stream=True)
        with open(output_path, 'wb') as f:
            for chunk in response:
                f.write(chunk)

class Extractor:

    def __init__(self):
        pass

    def run(self):
        pass

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
    extractor = Extractor()
    extractor.run()

    click.echo('Building stubs...')
    builder = Builder()
    builder.run()

    click.echo('Done.')
