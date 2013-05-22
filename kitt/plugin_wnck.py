#!/usr/bin/env python

from kivy.logger import Logger
log = Logger.getChild("KiTT")

import gtk
import sys, dbus, subprocess, os

import wnck

from actions import Actions

def workspace_up():
    while gtk.events_pending():
        gtk.main_iteration()
    self.screen.get_workspace_neighbor(self.screen.get_active_workspace(), wnck.MOTION_LEFT).activate(0)
    return True

def workspace_down():
    while gtk.events_pending():
        gtk.main_iteration()
    self.screen.get_workspace_neighbor(self.screen.get_active_workspace(), wnck.MOTION_RIGHT).activate(0)
    return True

ACTIONS = dict(
    workspace_up = workspace_up,
    workspace_down = workspace_down
)

