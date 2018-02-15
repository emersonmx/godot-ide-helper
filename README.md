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

--regex-gdscript=/^#![[:blank:]]*class:[[:blank:]]+([a-zA-Z0-9_]+)[[:blank:]]*/\1/c,class,classes/{scope=push}
--regex-gdscript=/^[[:blank:]]*const[[:blank:]]+([a-zA-Z0-9_]+)[[:blank:]]*/\1/C,constant,constants/{scope=ref}
--regex-gdscript=/^[[:blank:]]*signal[[:blank:]]+([a-zA-Z0-9_]+)[[:blank:]]*/\1/s,signal,signals/{scope=ref}
--regex-gdscript=/^[[:blank:]]*export[[:blank:]]*(\([a-zA-Z0-9_, \"\*\.]*\)|[[:blank:]]*)+(onready[[:blank:]]+)?var[[:blank:]]+([a-zA-Z0-9_]+)[[:blank:]]*/\3/e,export,exports/{scope=ref}
--regex-gdscript=/^[[:blank:]]*onready[[:blank:]]+var[[:blank:]]+([a-zA-Z0-9_]+)[[:blank:]]*/\1/o,onready/{scope=ref}
--regex-gdscript=/^[[:blank:]]*var[[:blank:]]+([a-zA-Z0-9_]+)[[:blank:]]*/\1/a,attribute,attributes/{scope=ref}
--regex-gdscript=/^[[:blank:]]*func[[:blank:]]+([a-zA-Z0-9_]+)[[:blank:]]*/\1/m,method,methods/{scope=ref}
```

Follow [this](https://github.com/syskrank/vim-gdscript-ctags) for vim + gdscript + ctags

I create my tags with `ctags -f tags --languages=gdscript --tag-relative=never --fields=+liaS -R api/`

[1]: https://github.com/syskrank/vim-gdscript-ctags#add-the-following-to-your-ctags-file
