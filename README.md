# gdscript-ide-helper

## Requirements
- Python 3
- Requests

## Generating gdscripts
- Create a virtualenv with `python -m venv venv`
- Install the dependencies with `pip install -r requirements.txt`
- Run generate.py with `python generate.py`

## Setup Ctags

Add the following to your ~/.ctags file: <sup>[1]</sup>
```
--langdef=gdscript
--langmap=gdscript:.gd

--regex-gdscript=/^[ \t]*const[ \t]+([a-zA-Z0-9_]+)[ \t]*/\1/c,constant/i
--regex-gdscript=/^[ \t]*export[ \t]*(\([ \t]*[a-zA-Z0-9_, \"\*\.]*\)|[ \t])+var[ \t]+([a-zA-Z0-9_]+)[ \t]*/\2/e,export/i
--regex-gdscript=/^[ \t]*onready[ \t]+var[ \t]+([a-zA-Z0-9_]+)[ \t]*/\1/o,onready-variable/i
--regex-gdscript=/^[ \t]*signal[ \t]+([a-zA-Z0-9_]+)[ \t]*/\1/s,signal/i
--regex-gdscript=/^[ \t]*func[ \t]+([a-zA-Z0-9_]+)[ \t]*/\1/f,function/i
--regex-gdscript=/^[ \t]*var[ \t]+([a-zA-Z0-9_]+)[ \t]=[ \t]*preload*/\1/p,preload/i
```

Follow [this](https://github.com/syskrank/vim-gdscript-ctags) for vim + gdscript + ctags

[1]: https://github.com/syskrank/vim-gdscript-ctags#add-the-following-to-your-ctags-file
