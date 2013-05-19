#!/usr/bin/env python

from kivy.logger import Logger
log = Logger.getChild("KiTT")

import gtk
import sys, dbus, subprocess, os

from kitt.actions import Actions

def DBusInterface():
    def dbus_message(self, plugin, action):
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


class Actions():
    GESTURES = dict(
        move_down = [
        ],
        move_up = [
        ],
        move_left = [
        ],
        move_right = [
        ]
    )

    def three_swipe_up(self):
        pass

    def three_swipe_down(self):
        pass

    def three_swipe_left(self):
        while gtk.events_pending():
            gtk.main_iteration()
        screen.get_workspace_neighbor(screen.get_active_workspace(), wnck.MOTION_LEFT).activate(0)

    def three_swipe_right(self):
        while gtk.events_pending():
            gtk.main_iteration()
        screen.get_workspace_neighbor(screen.get_active_workspace(), wnck.MOTION_RIGHT).activate(0)

    def two_swipe_up(self):
        pass

    def two_swipe_down(self):
        pass

    def two_swipe_left(self):
        pass

    def two_swipe_right(self):
        pass

    def dispatch(self, gestures, gdb):
        down = up = left = right = 0
        for gesture in gestures:
            if gesture is None:
                log.warning("Undefined touch")
                continue
            gesture = gesture[1]
            if gesture:
                if   gesture.name == 'move_down':
                    down += 1
                elif gesture.name == 'move_up':
                    up += 1
                elif gesture.name == 'move_left':
                    left += 1
                elif gesture.name == 'move_right':
                    right += 1
                else:
                    log.warn("Unknown gesture")
            else:
                log.info("gesture: \t", gdb.gesture_to_str(gesture))
                for gest_n, gest_r in GESTURES.iteritems():
                    s = gest_n, "\t",
                    for g2 in gest_r:
                        g2 = gdb.str_to_gesture(g2)
                        g2.normalize()
                        s += g2.get_score(gesture),
                    log.debug(s)

        if up is 3      and down == left == right == 0:
            self.three_swipe_up()
        elif down is 3  and up == left == right == 0:
            self.three_swipe_down()
        elif left is 3  and up == down == right == 0:
            self.three_swipe_left()
        elif right is 3 and up == down == left == 0:
            self.three_swipe_right()
        elif up is 2    and down == left == right == 0:
            self.two_swipe_up()
        elif down is 2  and up == left == right == 0:
            self.two_swipe_down()
        elif left is 2  and up == down == right == 0:
            self.two_swipe_left()
        elif right is 2 and up == down == left == 0:
            self.two_swipe_right()
        else:
            log.warn("Gesture:\tNot found")



