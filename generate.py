#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import requests

import generators

def download_classes_xml():
    headers = {'Accept': 'application/vnd.github.v3+json'}
    url = 'https://api.github.com/repos/godotengine/godot/releases'
    dl_url_base = 'https://github.com/godotengine/godot/raw/{}/doc/base/classes.xml'

    r = requests.get(url, headers=headers)
    releases = r.json()
    for i, release in enumerate(releases):
        print('[{}] {}'.format((i + 1), release['tag_name']))

    version = input('Select version [empty to master]: ')
    dl_url = ''
    if version == '':
        dl_url = dl_url_base.format('master')
    else:
        if 1 <= int(version) <= len(releases):
            dl_url = dl_url_base.format(releases[int(version) - 1]['tag_name'])
        else:
            print('Invalid tag')
            sys.exit(1)

    print('Downloading "{}"...'.format(dl_url))
    rfile = requests.get(dl_url)
    with open('classes.xml', 'w+') as f:
        f.write(rfile.text)

def select_generator():
    generators_list = [
        'GDScript'
    ]

    for idx, generator in enumerate(generators_list):
        print('[{}] {}'.format((idx + 1), generator))
    selection = input('Select generator [empty to GDScript]: ')
    if selection == '':
        return generators.GDScriptGenerator()

    if 1 <= int(selection) <= len(generators_list):
        class_name = generators_list[int(selection) - 1] + 'Generator'
        cls = getattr(generators, class_name)
        return cls()
    else:
        print('Invalid generator')
        sys.exit(1)

def main():
    if not os.path.exists('classes.xml'):
        download_classes_xml()

    generator = select_generator()
    generator.run()

if __name__ == "__main__":
    main()
