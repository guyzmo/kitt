KiTT: Kivy Touch Tool
=====================

This tool is a little Xorg service that provides a way to define gestures for Xorg UI
control. It is based on Kivy for gesture detection and can run a variety of plugins
to control the UI.

Now it only uses the wmck plugin that can handle windows and workspaces through the
gtk enabled window manager.

INSTALL
-------

This application is still not on pipy. Meanwhile:

git clone https://github.com/guyzmo/kitt.git
cd kitt
python setup.py install

DEVELOP
-------

for development, you'll need zc.buildout (`apt-get install python-zc.buildout` or `pip install zc.buildout`)

git clone https://github.com/guyzmo/kitt.git
cd kitt
buildout

EXTEND
------

to add new gestures, or new way to interact, you can edit `$SRC/kitt/plugin_wmck.py`
as a base. `plugin_dbus.py` has a basic dbus interaction function. I also have planned
to support directly XLib communication.

LICENSE
-------

This whole software is released under the GPLv3.

