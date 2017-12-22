from setuptools import setup

setup(
    name='godot_ide_helper',
    version='0.1',
    py_modules=['godot_ide_helper'],
    install_requires=[
        'Click',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        godot_ide_helper=godot_ide_helper:cli
    ''',
)
