#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import requests

from godot_ide_helper.cli import cli


class GodotVersions:

    def __init__(self):
        self._headers = {'Accept': 'application/vnd.github.v3+json'}
        self._url = 'https://api.github.com/repos/godotengine/godot/tags'

    def list(self):
        response = requests.get(self._url, headers=self._headers)
        if response.status_code == 403:
            raise click.ClickException('Exceeded github limit.')

        tags = response.json()

        yield 'master'
        for tag in tags:
            yield tag['name']

@cli.command()
def versions():
    '''List Godot versions.'''
    versions = GodotVersions()
    for version in versions.list():
        click.echo(version)
