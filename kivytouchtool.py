#!/usr/bin/env python

import gtk
import sys, dbus, subprocess, os

import wnck


screen = wnck.screen_get_default()
if not screen:
    sys.exit(1)

from kivy.base import EventLoop, runTouchApp
from kivy.event import EventDispatcher
from kivy.graphics import Line
from kivy.gesture import Gesture, GestureDatabase

####
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
####

gestures = dict(
    move_down = [
        "eNq1l01uGzkQhfd9EWszBuufdYFkG8AHGDi2YAvJ2IKkzExuP1UlqdWLREIm4KIgqfX4kc1HsoqrzZfN39/vX9b7w7fdevp4+ty2afW8henh7u3xr/XdtMX4Gh807R/u9ofd+5f1Pn7ytPq6lWn1Q8hDyaatJsqi/fZ983bIZj2b+U+afUrVtIXjCHII36MJ4PSh3TOaNGWVzgJIUsP5N/+m/LsJAQl37uLuhNP+8+P1Trg6kenlyKfuoNabqXeQrtP+5f+S663BZnI0F2FhoGCRym+ge6F9ABpr0hHOaOTWjBpqAxGw3yFjkWkAuTzE2UMQ6gAtFkgwWNUuaPYuAIZELbrVfptdLqINYZeN6CPYVD7S7GNTDSY0ULRuwLxgsyNbi70k0U8M5ya7nCQawi4vSYawy0s6eflHIGKLsxgYYcy34GLCURB6xx4bK9xguA0vM8mHwLncZBgDLzuZxsDLT5YZjhyntrTurcVKVz2fsNlvHLjhpXVUFwrdbXo5yjaIXpayj6FLeSowiF6mCg2il6syyFUpV+XiKjcCZdamhhxpYQE3UO3kgOYQJyTfhpep4kPgWp4qjIGXpUpj4OWoyhh4GaoXQwUyoQmrEzN2u8AhqIjo5o26ut3OdFqGqg+BWxlqMAZehhqNgZehdjFUwkePZMlxuHdTWcJN85FGzRtb1SXhWeU/7dbrt7lmN82i3WxaVR0eMI2xmEYesCiU46FxZuI5psM2Bvr4K3K/JqeYn36J0Pd2TY/uuIjUwzV9FFa4iNTjFb265gaZI/U061ukSWjEZhJHY+mNaRGcej7rMXKuZ9JVa96O+kixcIkav5z0YIbaoyByFNJWyVmjau46R41HT/rYs8jawYl6dJbyWA9tETWddpSTo7WoMqPkwgbxNOVxtcB+iZSfzKXFmxLmWZH6KNkWYan3s751AgTsnu9dk8kxt76I5PvJXTL3To2ULa9k8FN9uHtcua/rzcvrIdasH68a0jGS0znqzvjP5vnwmoq5mIybkzR0jR5iqYfk8P51vXt8e8rbr3NV6Pn4tN/+3O7en789VS/xxnTPWRTF5SUvp3kv/Xz/H5Ij87w="
    ],
    move_up = [
        "eNq1l9tuIzcMhu/nRZKbBuJZfIH0tkAeoEgTIwl2mxixt+2+fX/R9ngCtPG2wFwQ4wP1i9Inccjrly8vf3y/edrs9t/eN9PPx+e2TdePW5rurl7vf99cTVvGRzxk2t1d7fbvb182O3zV6frr1qbrfxS5K7dp60MqMH779vK6H8P6GJb/MuyX4TVt6RDBCOE7hhBPtz+1G4nWpGUPclYnr3j+Gv/LdNtuGpM1ikhSTs/EqN1v95/PozWPTU+nKRb67C4+7Z6O6pRNVYXTjPEl5LJ6LZ5iVucuGcbUeKyE2M7qTQU/mXXuluLxA7H3Us9ZnXqSqaaQdLPA2g7q+AvK2BnqQmGeyqoX5bkQMK0lzyUva8kXWD6DpYGzqSeLUoDuQt5ENTjSgAchmF2WL7Ica8kXWs6V5KXQyhEtJDR7TxEyZ5fovlQ3HHtni6BgtvYD6kVWZCX1Aiu2knpxlVhJvbBKrqOuRVVnqoSj0Lw7IWkRfTwySHKJiSWdumu7fJ+0oKqsI15M1dYRL6Q6IxVRMdKOPB7N23iJzOrk1qN1Dw8VZfPL6oVUcx11K6RGK6kXU5OV1Auq2UrqRdVWompF1c5UO147yMEqSYIUvHw3NQ9c0oaSANUCtx9Iv15UnVZSL6o+U9VjeumC6kL9g7g0lDqdQzSokV7eGC+oPkO1036rSxNfVkucjRC9douO0ulyteSF1GMV7QLquYZ2FM6YcWKXGcVKGztLS+UPx7DJ5dQVhTJmlM6JuhYhdgmTrmdtZenJTIFH9nYZZBTIsP8nPdqAh/fN5nUu6sNHVR8xXY8D7XDUJJRqgkKsDiGO9cJk2m+jT/f/wTuP3rgMQNTCcZ47NA7+450wW8C/t8/81ZY23Okz9+hLK38+Bd/TBtDW+FB8jQEo1CjPNvzl5B/eUa9hm0ezgjpy+BsWvrCaQE8DpC/HlL8LLc2Hvx39raH5wbszUBTW4sYAFIehs1VAfvRH1kFiQM2djLbkAN2YOWK2sf89Zv/WA7kIBbmMqYc7QkPfMttwP8FdrBViXuE4ocb32XT4n/Ca45pQ12zYCpAc7uG2sEE3T3S9oSTo2awbozKucJBNgxY2/E94fWRYQgeHFq9XMCPz8cKG9wzXO/YfzR7maBZ1OME60aUcbcSeM9tOrZ8XcHBHXAsbaPOEFokdJQ4aH/Sqhvam/FEGNp6tggfaw6V73rw8Pe9x3bIWCrpkORuPdvjPl8f98/CorWu4Deg1bST5Dr40XPZvXzfv968Po7PPOuH18zFR/Lp9f3v89lCz5HQrNzjhvU4mgb2MvvTmb/HSIV4=",
    ],
    move_left = [
        "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",
    ],
    move_right = [
        "eNq1l01uIzcQhfd9EXsTo35ZrAs42wA+QODYgi3MxBYkTZK5fR5LrR8g0SgI0AtClvX4is2Pxaq+X39Z//H94W2123/brqaf588NTfevG56e7j6ef1/dTRvBn/jQafd0t9tvP7+sdvhq0/3XjU/3/2ryVLJp04ZVYP7mc/2xH9P6mJZXpv0yVNOGDysYS/iOKSzTIz0QNxUyb9qdkzjbWM9f43edHn+iB1OjTtqpcXey7tPut+cfx7GK49PbMUSYxwiSzKI9EOJtdh/fJHt27y5Ecdu8np3jP5lz15RTCLtt3ss8FzGX2n7hs/k/d/5oLu4yTD0zw1Jvb7pIuetC7oVULpByhFpTb2zucfbmzi1I2CgjqY+wt7yLqMQi3gVUcglvLZ565knsJiEZyBdsMI19PdoTaSAmaWvd8Ml5+8BoIVVdLkBRVV8uQKHVWC5A8dVcLIAVZJshl4kFJZLKxLwLk8wB8FO6RHYEF1WiJrfdi7DpQu6F13wh92JrcXZnS0OCpQScLLOf3JW8CS4kZw9Wup1bVlwtFzH3Yuq8jHkhdV3GvIi6L2NeQH0ZoF5AfRmgrYC2S6CtmYux99Y7auDZO5ADuOedm/e0drv0tQLadBnzAtougIqRGpOluCFP0Usd3R0XF2r1uLaoud5ulVoBbbGMeQFtuYh5FNDgZcwLaFwAldbDM9yMBETlwryh88vGuDRxXm/zjOIZ/j+9x5vAy3a1+jj19eg40dhHTPeP1XImm2IjOjshY4ZL4qHtPKb9Jvr0XHIx1ELrlNwISXVNnrNcUR4De+umreM1oeQopHYaUHea1caaTCgnkrXzV+Q8y7GO1ESuW2DmNXM5qI3AuMOZEpWK5drSu856HA3nGM04khN7XPKxU6dhQ24HOUodGyOJrYngrik5loeG/jhK7rM8nJo2VlFG5zzLcT+dR8nbQd4C7YVF1wAklgMlIKaLMeRxkOPZRULxftEp0Jke5ORdT6MN+Qw1AieqB+5N14brpuS4dOg8hnpm2mlUddR17qjtflg6miCV84A86YdyvRhj6Qmoh9P6vlq/ve9xTvPQfgkH9vY4Gso4RH+uX/fvQ1PPZl072i8cS2qBVmQo9p9fV9vnj5fxWpxFj8e/5xz7dbP9fP32UmFwEhQvjdlbJsjhFOZoVR7+BgO2+GU="
    ]
);

def make_gesture(name, point_list):
    """
    A simple helper function
    """
    g = Gesture()
    g.add_stroke(point_list)
    g.normalize()
    g.name = name
    return g

class Listener(EventDispatcher):
    def __init__(self, *args, **kwarg):
        super(EventDispatcher, self).__init__(*args, **kwarg)
        self._gdb = GestureDatabase()
        for gest_n, gest_r in gestures.iteritems():
            for g in gest_r:
                g = self._gdb.str_to_gesture(g)
                g.normalize()
                g.name = gest_n
                self._gdb.add_gesture(g)
        self._multitouches = []

    def on_touch_down(self, touch):
        self._multitouches.append(touch)
        touch.ud['line'] = Line(points=(touch.sx, touch.sy))
        return True

    def on_touch_move(self, touch):
        # store points of the touch movement
        try:
            touch.ud['line'].points += [touch.sx, touch.sy]
            return True
        except (KeyError), e:
            pass

    def on_touch_up(self, touch):
        # touch is over, display informations, and check if it matches some
        # known gesture.
        if len(self._multitouches) is 0:
            return True

        down = up = left = right = 0

        print "multitouches: ", len(self._multitouches)
        for touch in self._multitouches:
            g = make_gesture(
                    '',
                    zip(touch.ud['line'].points[::2], touch.ud['line'].points[1::2])
                    )

            # print the gesture representation, you can use that to add
            # gestures to my_gestures.py
            #print "gesture representation:", self._gdb.gesture_to_str(g)
            g2 = self._gdb.find(g, minscore=0.70)
            if g2:
                if   g2[1].name == 'move_down':
                    down += 1
                elif g2[1].name == 'move_up':
                    up += 1
                elif g2[1].name == 'move_left':
                    left += 1
                elif g2[1].name == 'move_right':
                    right += 1
                else:
                    print "Unknown gesture"
            else:
                print self._gdb.gesture_to_str(g)
                for gest_n, gest_r in gestures.iteritems():
                    for g2 in gest_r:
                        g2 = self._gdb.str_to_gesture(g2)
                        g2.normalize()
                        g2.name = gest_n
                        print g2.get_score(g)

        if up is 3 and down == left == right == 0:
            print "up 3 touches"
        elif down is 3 and up == left == right == 0:
            print "down 3 touches"
        elif left is 3 and up == down == right == 0:
            print "left 3 touches"
            while gtk.events_pending():
                gtk.main_iteration()
            screen.get_workspace_neighbor(screen.get_active_workspace(), wnck.MOTION_LEFT).activate(0)
        elif right is 3 and up == down == left == 0:
            print "right 3 touches"
            while gtk.events_pending():
                gtk.main_iteration()
            screen.get_workspace_neighbor(screen.get_active_workspace(), wnck.MOTION_RIGHT).activate(0)
        elif up is 2 and down == left == right == 0:
            print "up 2 touches"
        elif down is 2 and up == left == right == 0:
            print "down 2 touches"
        elif left is 2 and up == down == right == 0:
            print "left 2 touches"
        elif right is 2 and up == down == left == 0:
            print "right 2 touches"
        else:
            print "Not found"

        self._multitouches = []

    def on_motion(self, etype, me):
        if etype == "begin":
            self.on_touch_down(me)
        elif etype == "update":
            self.on_touch_move(me)
        elif etype == "end":
            self.on_touch_up(me)
        else:
            print "Receive unknown event of type '%r': %s" % (etype, me)

    def dispatch(self, ev_type, ev_action, ev):
        if ev_type == "on_motion":
            self.on_motion(ev_action, ev)
        else:
            print "asking to dispatch unknown event: '%r': '%r'" % (ev_type, ev)

EventLoop.add_event_listener(Listener())
runTouchApp()

