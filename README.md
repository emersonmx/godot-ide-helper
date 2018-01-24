# gdscript-ide-helper

This tool create stubs from GDScript API (Godot < 3 only). You can use this with ctags or
anything you want.

## Requirements
- Python 3
- Requests
- Click

## Generating GDScripts
- Create a virtualenv with `python -m venv venv` or `virtualenv venv`
- Source venv with `source venv/bin/activate`
- Install the dependencies with `pip install -r requirements.txt`
- Run `pip install --editable .`
- Run `godot_ide_helper build` to build stubs for current stable version

## Setup Ctags

Add the following to your `~/.ctags` file:
```
--langdef=gdscript
--map-gdscript=.gd

--regex-gdscript=/^#![ \t]*class:[ \t]+([a-zA-Z0-9_]+)[ \t]*/\1/c,class/{scope=set}
--regex-gdscript=/^[ \t]*extends[ \t]+([a-zA-Z0-9_]+)[ \t]*/\1/i,inherits/{scope=push}
--regex-gdscript=/^[ \t]*const[ \t]+([a-zA-Z0-9_]+)[ \t]*/\1/C,constant/{scope=ref}
--regex-gdscript=/^[ \t]*export[ \t]*(\([ \t]*[a-zA-Z0-9_, \"\*\.]*\)|[ \t])+var[ \t]+([a-zA-Z0-9_]+)[ \t]*/\2/e,export/{scope=ref}
--regex-gdscript=/^[ \t]*onready[ \t]+var[ \t]+([a-zA-Z0-9_]+)[ \t]*/\1/o,onready-variable/{scope=ref}
--regex-gdscript=/^[ \t]*signal[ \t]+([a-zA-Z0-9_]+)[ \t]*/\1/s,signal/{scope=ref}
--regex-gdscript=/^[ \t]*func[ \t]+([a-zA-Z0-9_]+)[ \t]*/\1/f,function/{scope=ref}
--regex-gdscript=/^[ \t]*var[ \t]+([a-zA-Z0-9_]+)[ \t]=[ \t]*preload*/\1/p,preload/{scope=ref}
```

Follow [this](https://github.com/syskrank/vim-gdscript-ctags) for vim + gdscript + ctags

I create my tags with `ctags -f tags --languages=gdscript --tag-relative=never --fields=+liaS -R api/`

[1]: https://github.com/syskrank/vim-gdscript-ctags#add-the-following-to-your-ctags-file
