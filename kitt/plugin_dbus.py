#!/usr/bin/env python

from kivy.logger import Logger
log = Logger.getChild("KiTT")

import gtk
import sys, dbus, subprocess, os

from kitt.actions import Actions

def dbus_message(plugin, action):
    try:
        rootwin = subprocess.Popen(['xwininfo', '-root'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    except OSError:
        raise SystemExit('Error: xwininfo not present')

    try:
        rootwin_id = int(rootwin.split()[3], 0)
    except IndexError:
        raise SystemExit('Error: unexpectedly short output from xwininfo')
    except ValueError:
        raise SystemExit('Error: unable to convert "%s" to int', rootwin.split()[3])

    service = interface = 'org.freedesktop.compiz'
    session_bus = dbus.SessionBus()

    args = ['root', rootwin_id]

    proxy = session_bus.get_object(
        service, '/org/freedesktop/compiz/%s/allscreens/%s' %(plugin, action))
    obj = dbus.Interface(proxy, interface)
    obj.activate(*args)

ACTIONS = dict()


