#!/usr/bin/env python

from kivy.logger import Logger
log = Logger.getChild("KiTT")

import gtk
import sys, dbus, subprocess, os

from kitt.actions import Actions

def dbus_message(service, obj_path, method, *parameters):
    service = interface = '%s' % (service,)
    session_bus = dbus.SessionBus()
    proxy = session_bus.get_object(service, obj_path)
    obj = dbus.Interface(proxy, interface)
    getattr(method)(*parameters)

ACTIONS = dict(send_dbus=dbus_message)

