KiTT: Kivy Touch Tool
=====================

This tool is a little Xorg service that provides a way to define multitouch gestures
for Xorg UI control. It is based on Kivy for gesture detection and can run a variety
of plugins to control the UI. You can easily configure your gestures using a json 
configuration file.

INSTALL
-------

This application is still not on pipy. Meanwhile:

git clone https://github.com/guyzmo/kitt.git
cd kitt
python setup.py install

CONFIGURE
---------

To add a new gesture and bind actions, you shall create a configuration file, either in the default
path: `~/.kivy/kitt.json` or a file you can specify using a command line option.

To configure, the file shall match the following format, be careful, every comma, quote or bracket is important:

    {
        "engines": [],
        "gestures": {
            "move_down" : [],
            "move_up"   : [],
            "move_left" : [],
            "move_right": []
        },
        "actions": {
            "pinch_in"          : [],
            "pinch_out"         : [],
            "two_swipe_up"      : [],
            "two_swipe_down"    : [],
            "two_swipe_left"    : [],
            "two_swipe_right"   : [],
            "three_swipe_up"    : [],
            "three_swipe_down"  : [],
            "three_swipe_left"  : [],
            "three_swipe_right" : [],
            "four_swipe_up"     : [],
            "four_swipe_down"   : [],
            "four_swipe_left"   : [],
            "four_swipe_right"  : []
        }
    }

 * The `engines` key can contain three plugins: `xlib`, `wmck` and `dbus`.
 * The `gestures` key contains the specific gestures for your touch device. To record them, 
   you have to execute kitt as follows, and copy the long ununderstandable strings that it outputs
   for each gesture you want to record.

    kitt foreground -v

 * The `action` key contains for each known common multitouch gesture the action to trigger,
   that depends on the engine you use.

Here are the different actions available:

 * `xlib` engine:
    * `{ "function": "workspace", parameters: ["N"] }` switch current worskpace, N being the number of workspaces to jump over (can be a positive or negative number)
    * `{ "function": "keypress", parameters: ["KEY1", "KEY2"] }` executes a key stroke, which can be a combination of several keys (modifier keys, or input keys)
    * `{ "function": "mouseclick", parameters: ["Button1"] }` executes a click (can be either `Button1`, `Button2`, `Button3`, `button4`, `Button5`)
 * `wmck` engine:
   * `{ "function": "workspace_up", parameters: [] }` switch to previous workspace
   * `{ "function": "workspace_down", parameters: [] }` switch to next workspace
 * `dbus` engine:
   * still has to be implemented, but I expect to code a `send_message` function that will take a full dbus message as parameter.

For the keys to be implemented in keypress function, I will add a documentation in the wiki, but for the time being, you
can take their name from the Xlib.XK package, without the `XK_` prefix.

DEVELOP
-------

For development, you'll need zc.buildout (`apt-get install python-zc.buildout` or `pip install zc.buildout`)

git clone https://github.com/guyzmo/kitt.git
cd kitt
buildout

EXTEND
------

To add a new gesture, or new way to interact, you can copy and base your work upon
`$SRC/kitt/plugin_wmck.py` or `plugin_xlib.py`. The engine `plugin_dbus.py` has a 
basic dbus interaction function.

Please fork the project, and send me back patches!

LICENSE
-------

This whole software is released under the GPLv3.

