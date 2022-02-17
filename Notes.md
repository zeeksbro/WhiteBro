# WhiteBro

Browser with White list

## Trobleshooting

In case
`qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.`
do
`export QT_DEBUG_PLUGINS=1`
`python3 WhiteBro.py`

`Cannot load library /home/fil/.local/lib/python3.9/site-packages/PySide6/Qt/plugins/platforms/libqxcb.so: (libxcb-icccm.so.4: невозможно открыть разделяемый объектный файл: Нет такого файла или каталога)`

So `sudo apt install libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0`

## TODO

- хоткеи
- поиск на странице
- поиск по разрешенным сайтам

## Installation

sudo apt install git python3-venv
python3 -m venv env
. env/bin/activate
pip3 install pyside6 adblockparser
