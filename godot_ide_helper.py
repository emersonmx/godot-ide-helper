#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import requests
import click

import generators
import downloaders

class GodotVersions:

    def __init__(self):
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        self.url = 'https://api.github.com/repos/godotengine/godot/tags'

    def list(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 403:
            raise click.ClickException('Exceeded github limit')

        tags = response.json()

        # yield 'master'
        for tag in tags:
            yield tag['name']

    def download(self, version):
        downloader = downloaders.ZipDownloader(version)
        downloader.download()
        sys.exit(0)

@cli.command()
@click.option('--generator', default='GDScript', type=click.Choice(['GDScript']),
              help='Generator to build scripts.')
@click.argument('version', default='stable')
def build(generator, version):
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
    godot_versions.download(version)

    click.echo('Generating stubs...')
    class_name = generator + 'Generator'
    cls = getattr(generators, class_name)
    app = cls()
    app.run()
    click.echo('Done.')

@cli.command()
def versions():
    '''List Godot versions.'''
    versions = GodotVersions()
    for version in versions.list():
        click.echo(version)

@cli.command()
def clean():
    '''Clean build files.'''

    click.echo('Cleaning build files...')
    for dirpath, dirs, files in os.walk('scripts'):
        for file in files:
            if file.startswith('.'):
                continue
            os.remove(os.path.join(dirpath, file))

    if os.path.exists('classes.xml'):
        os.remove('classes.xml')

    click.echo('Done.')
