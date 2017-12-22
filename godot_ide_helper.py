#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import requests
import click

import generators

CLASSES_PATH = os.path.abspath('classes.xml')


class GodotVersions:

    def __init__(self):
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        self.url = 'https://api.github.com/repos/godotengine/godot/releases'
        self.dl_url_base = 'https://github.com/godotengine/godot/raw/{}/doc/base/classes.xml'

    def get_download_url(self, version):
        return self.dl_url_base.format(version)

    def list(self):
        response = requests.get(self.url, headers=self.headers)
        releases = response.json()

        # yield 'master'
        for release in releases:
            yield release['tag_name']

    def download(self, version):
        dl_url = self.get_download_url(version)
        rfile = requests.get(dl_url)
        with open(CLASSES_PATH, 'w+') as f:
            f.write(rfile.text)

@click.group()
def cli():
    pass

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

    dl_url = godot_versions.get_download_url(version)
    if os.path.exists(CLASSES_PATH):
        os.remove(CLASSES_PATH)

    click.echo('Downloading "{}"...'.format(dl_url))
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
