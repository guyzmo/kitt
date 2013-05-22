#!/usr/bin/env python

from kivy.logger import Logger
log = Logger.getChild("KiTT")

import gtk
import sys, dbus, subprocess, os

from kitt.actions import Actions

def dbus_message(service, path, method, parameters):
    """
    sends a dbus message
    :param service: string containing the full service name (with dots)
    :param path: string containing the full path to the object (with slashes)
    :param method: string containing name of the method to call
    :param parameters: list of each parameter
    """
    service = interface = '%s' % (service,)
    session_bus = dbus.SessionBus()
    proxy = session_bus.get_object(service, path)
    obj = dbus.Interface(proxy, interface)
    getattr(method)(*parameters)

ACTIONS = dict(send_dbus=dbus_message)

