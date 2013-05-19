#!/usr/bin/env python

from kivy.logger import Logger
log = Logger.getChild("KiTT")

from kivy.event import EventDispatcher
from kivy.graphics import Line
from kivy.gesture import Gesture, GestureDatabase


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
    def __init__(self, actions, *args, **kwarg):
        super(EventDispatcher, self).__init__(*args, **kwarg)
        self._gdb = GestureDatabase()
        self._action = actions()
        for gest_n, gest_r in actions.GESTURES.iteritems():
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

        # down = up = left = right = 0

        log.debug("multitouches: \t%d" % len(self._multitouches))

        gestures = map(lambda g: self._gdb.find(make_gesture('',zip(touch.ud['line'].points[::2],
                                            touch.ud['line'].points[1::2])), minscore=0.70), self._multitouches)

        self._action.dispatch(gestures, self._gdb)

        self._multitouches = []

    def on_motion(self, etype, me):
        if etype == "begin":
            self.on_touch_down(me)
        elif etype == "update":
            self.on_touch_move(me)
        elif etype == "end":
            self.on_touch_up(me)
        else:
            log.error("Receive unknown event of type '%r': %s" % (etype, me))

    def dispatch(self, ev_type, ev_action, ev):
        if ev_type == "on_motion":
            self.on_motion(ev_action, ev)
        else:
            log.error("asking to dispatch unknown event: '%r': '%r'" % (ev_type, ev))

