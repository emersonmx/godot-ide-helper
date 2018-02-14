from setuptools import setup, find_packages

setup(
    name='godot_ide_helper',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        godot_ide_helper=godot_ide_helper.cli:cli
    ''',
)
