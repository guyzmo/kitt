#!/usr/bin/env python

from Xlib import X, XK, protocol, display, Xcursorfont
from Xlib.ext import xtest
from Xlib.protocol import request

import os

def do_mouse_click(buttontype):
    """
    executes mouse button click

    buttontype: X.Button1, X.Button2 or X.Button3 depending on which button to be triggered
    """
    d = display.Display()
    root = d.screen().root
    pointer_info = request.QueryPointer(display = d.display,
                                        window = root)
    root_xpos, root_ypos = (pointer_info._data['root_x'], pointer_info._data['root_y'])
    targetwindow = d.get_input_focus().focus
    if targetwindow.get_wm_name() is None and targetwindow.get_wm_class() is None:
        targetwindow = targetwindow.query_tree().parent
    ret = targetwindow.translate_coords(root, root_xpos, root_ypos)
    target_xpos = ret.x
    target_ypos = ret.y

    myevent_press = protocol.event.ButtonPress(detail = buttontype,
                                            root=root,
                                            root_x=root_xpos,
                                            root_y=root_ypos,
                                            window=targetwindow.id,
                                            event_x=target_xpos,
                                            event_y=target_ypos,
                                            same_screen=1,
                                            state=0,
                                            time=X.CurrentTime,
                                            child=0)
    myevent_release = protocol.event.ButtonRelease(detail = buttontype,
                                                root=root,
                                                root_x=root_xpos,
                                                root_y=root_ypos,
                                                window=targetwindow.id,
                                                event_x=target_xpos,
                                                event_y=target_ypos,
                                                same_screen=1,
                                                state=0,
                                                time=X.CurrentTime,
                                                child=0)

    # use window instead of display (xobject/drawable.py:send_event)
    d.send_event(X.InputFocus,
                myevent_press,
                event_mask=0,
                propagate=1)

    # use window instead of display (xobject/drawable.py:send_event)
    d.send_event(X.InputFocus,
                myevent_release,
                event_mask=0,
                propagate=1)
    d.flush()


def do_key_press(*keys):
    """
    executes a keypress

    keys: argument tuple containing one or several modifier keys, and the key to press

    the key to pass as a parameter has to be taken from Xlib.XK library
    """
    d = display.Display()
    root = d.screen().root

    pointer_info = request.QueryPointer(display = d.display,
                                        window = root)
    root_xpos, root_ypos = (pointer_info._data['root_x'], pointer_info._data['root_y'])
    targetwindow = d.get_input_focus().focus
    if targetwindow.get_wm_name() is None and targetwindow.get_wm_class() is None:
        targetwindow = targetwindow.query_tree().parent
    ret = targetwindow.translate_coords(root, root_xpos, root_ypos)
    target_xpos = ret.x
    target_ypos = ret.y

    def send_key(display, window, keycodes):
        '''Send a KeyPress and KeyRelease event'''
        if not type(keycodes) is tuple:
            keycodes = (keycodes,)
        # send with modifier
        for keycode in keycodes:
            xtest.fake_input(window,
                             X.KeyPress,
                             display.keysym_to_keycode(keycode))
        for keycode in reversed(keycodes):
            xtest.fake_input(window,
                             X.KeyRelease,
                             display.keysym_to_keycode(keycode))
        display.flush()

    send_key(d, root, keys)


def switch_workspace(direction):
    """
    switches workspace

    direction: +1 for next workspace, -1 for previous workspace.
    """
    d = display.Display()
    screen = d.screen()
    root   = screen.root

    def get_property(disp, name):
        atom = disp.intern_atom(name)
        return disp.screen().root.get_full_property(atom, 0)

    def send_event(win, ctype, data, mask=None):
        """ Send a ClientMessage event to the root """
        data = (data+[0]*(5-len(data)))[:5]
        ev = protocol.event.ClientMessage(window=win, client_type=ctype, data=(32,(data)))

        if not mask:
            mask = (X.SubstructureRedirectMask|X.SubstructureNotifyMask)
        root.send_event(ev, event_mask=mask)
        d.flush()

    cur_ws = get_property(d, '_NET_CURRENT_DESKTOP').value[0]

    # switch to previous desktop
    send_event(root,
               display.Display().intern_atom("_NET_CURRENT_DESKTOP"),
               [cur_ws+direction, X.CurrentTime])


if __name__ == "__main__":
    do_mouse_click(X.Button3)
    do_key_press((XK.XK_Alt_L, XK.XK_Tab))
    switch_workspace(+1)

