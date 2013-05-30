KiTT: Kivy Touch Tool
=====================

This tool is a little Xorg service that provides a way to define multitouch gestures
for Xorg UI control. It is based on Kivy for gesture detection and can run a variety
of plugins to control the UI. You can easily configure your gestures using a json 
configuration file.

KiTT takes advantage of the awesome work done by the [Kivy](http://kivy.org) team on
touch and gesture detection framework. Your mouse has to be detected by Kivy in order
to work with KiTT, and thus shall exists as a known `/dev/input/event?` device.

And [here](http://nothing.to/blog/2013/05/22/kitt:-a-multitouch-gesture-tool-based-on-kivy) I wrote a blog post about it!

INSTALL
-------

To install the application, just get it from pipy:

    pip install kitt

To run it at startup of Xorg, don't forget to add `kitt start` in your `.xinitrc` or `.xsession` file!


CONFIGURE
---------

Have a look at kivy specific [configuration options](http://kivy.org/docs/guide/config.html)

 * actions configuration file: `config_actions.json`

To add a new gesture and bind actions, you shall create a configuration file, either in the default
path: `~/.kivy/kitt.json` or a file you can specify using a command line option.

To configure, the file shall match the following format, be careful, every comma, quote or bracket is important:

    {
        "engines": [],
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

    * The `engines` key can contain three plugins: `xlib`, `wnck` and `dbus`.
    * The `action` key contains for each known common multitouch gesture the action to trigger,
    that depends on the engine you use.

 * gestures configuration file: `config_gestures.json`:

        {
            "move_down" : [],
            "move_up"   : [],
            "move_left" : [],
            "move_right": []
        }

    * The `gestures` key contains the specific gestures for your touch device. To record them, 
    you have to execute kitt as follows, and copy the long ununderstandable strings that it outputs
    for each gesture you want to record.

        kitt foreground -v


Here are the different actions available:

 * `xlib` engine:
    { 
      "function": "workspace",
      "parameters": {
        "direction": "N"
      } 
    } 

switch current worskpace, N being the number of workspaces to jump over (can be a positive or negative number)

    { 
      "function": "keypress", 
      "parameters": {
        "target": ["app1", "app2"],
        "keys": ["KEY1", "KEY2"]
      } 
    } 

executes a key stroke, which can be a combination of several keys (modifier keys, or input keys from the list below)
the "target" attribute is one of the `wm-class` property of the window. It can be found when triggering the action on
an unknown window, when in `foreground` mode.


    { "function": "mouseclick", 
      "parameters": {
        "button": "ButtonN"
      } 
    }

executes a click (can be either `Button1`, `Button2`, `Button3`, `button4`, `Button5`)


 * `wnck` engine:

    { "function": "workspace_up", parameters: {} }

switch to previous workspace

    { "function": "workspace_down", parameters: {} }

switch to next workspace

 * `dbus` engine:

    { 
      "function": "send_dbus",
      "parameters": { 
        "service": "name.of.the.service", 
        "path": "/path/to/the/object",
        "method": "methodName"
        "parameters": ["param1", "param2"...]
      }
    } 

call method on service `service`, object path `object` with all needed parameters

DEVELOP
-------

For development, you'll need zc.buildout (`apt-get install python-zc.buildout` or `pip install zc.buildout`)

    % git clone https://github.com/guyzmo/kitt.git
    % cd kitt
    % buildout

EXTEND
------

To add a new gesture, or new way to interact, you can copy and base your work upon
`$SRC/kitt/plugin_wnck.py` or `plugin_xlib.py`. The engine `plugin_dbus.py` has a 
basic dbus interaction function.

Please fork the project, and send me back patches!

TODO
----

 * implement pinch\_in/pinch\_out features and other weird gestures ;
 * create a GUI, like BTT's

LICENSE
-------

This whole software is released under the GPLv3.

LIST OF KEYS
------------

    0                  F33                L2                 Touroku            idiaeresis
    1                  F34                L3                 U                  igrave
    2                  F35                L4                 Uacute             j
    3                  F4                 L5                 Ucircumflex        k
    4                  F5                 L6                 Udiaeresis         l
    5                  F6                 L7                 Ugrave             less
    6                  F7                 L8                 Undo               m
    7                  F8                 L9                 Up                 macron
    8                  F9                 Left               V                  masculine
    9                  Find               Linefeed           W                  minus
    A                  G                  M                  X                  mu
    AE                 H                  Mae_Koho           Y                  multiply
    Aacute             Hankaku            Massyo             Yacute             n
    Acircumflex        Help               Menu               Z                  nobreakspace
    Adiaeresis         Henkan             Meta_L             Zen_Koho           notsign
    Agrave             Henkan_Mode        Meta_R             Zenkaku            ntilde
    Alt_L              Hiragana           Mode_switch        Zenkaku_Hankaku    numbersign
    Alt_R              Hiragana_Katakana  Muhenkan           a                  o
    Aring              Home               Multi_key          aacute             oacute
    Atilde             Hyper_L            MultipleCandidate  acircumflex        ocircumflex
    B                  Hyper_R            N                  acute              odiaeresis
    BackSpace          I                  Next               adiaeresis         ograve
    Begin              Iacute             Ntilde             ae                 onehalf
    Break              Icircumflex        Num_Lock           agrave             onequarter
    C                  Idiaeresis         O                  ampersand          onesuperior
    Cancel             Igrave             Oacute             apostrophe         ordfeminine
    Caps_Lock          Insert             Ocircumflex        aring              oslash
    Ccedilla           J                  Odiaeresis         asciicircum        otilde
    Clear              K                  Ograve             asciitilde         p
    Control_L          KP_0               Ooblique           asterisk           paragraph
    Control_R          KP_1               Otilde             at                 parenleft
    D                  KP_2               P                  atilde             parenright
    Delete             KP_3               Page_Down          b                  percent
    Down               KP_4               Page_Up            backslash          period
    E                  KP_5               Pause              bar                periodcentered
    ETH                KP_6               PreviousCandidate  braceleft          plus
    Eacute             KP_7               Print              braceright         plusminus
    Ecircumflex        KP_8               Prior              bracketleft        q
    Ediaeresis         KP_9               Q                  bracketright       question
    Egrave             KP_Add             R                  brokenbar          questiondown
    Eisu_Shift         KP_Begin           R1                 c                  quotedbl
    Eisu_toggle        KP_Decimal         R10                ccedilla           quoteleft
    End                KP_Delete          R11                cedilla            quoteright
    Escape             KP_Divide          R12                cent               r
    Eth                KP_Down            R13                colon              registered
    Execute            KP_End             R14                comma              s
    F                  KP_Enter           R15                copyright          script_switch
    F1                 KP_Equal           R2                 currency           section
    F10                KP_F1              R3                 d                  semicolon
    F11                KP_F2              R4                 degree             slash
    F12                KP_F3              R5                 diaeresis          space
    F13                KP_F4              R6                 division           ssharp
    F14                KP_Home            R7                 dollar             sterling
    F15                KP_Insert          R8                 e                  t
    F16                KP_Left            R9                 eacute             thorn
    F17                KP_Multiply        Redo               ecircumflex        threequarters
    F18                KP_Next            Return             ediaeresis         threesuperior
    F19                KP_Page_Down       Right              egrave             twosuperior
    F2                 KP_Page_Up         Romaji             equal              u
    F20                KP_Prior           S                  eth                uacute
    F21                KP_Right           Scroll_Lock        exclam             ucircumflex
    F22                KP_Separator       Select             exclamdown         udiaeresis
    F23                KP_Space           Shift_L            f                  ugrave
    F24                KP_Subtract        Shift_Lock         g                  underscore
    F25                KP_Tab             Shift_R            grave              v
    F26                KP_Up              SingleCandidate    greater            w
    F27                Kana_Lock          Super_L            guillemotleft      x
    F28                Kana_Shift         Super_R            guillemotright     y
    F29                Kanji              Sys_Req            h                  yacute
    F3                 Katakana           T                  hyphen             ydiaeresis
    F30                L                  THORN              i                  yen
    F31                L1                 Tab                iacute             z
    F32                L10                Thorn              icircumflex        

