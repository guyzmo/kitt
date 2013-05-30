#!/usr/bin/env python

from kivy.logger import Logger
log = Logger.getChild("KiTT")

from kivy.event import EventDispatcher
from kivy.graphics import Line
from kivy.gesture import Gesture, GestureDatabase

import pyudev

from actions import Actions

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
    """
    listener function that queries kivy for touch events, builds the gesture
    and dispatch it through the actions singleton.
    """
    def __init__(self, config, gestures, el, *args, **kwarg):
        """
        :param config: string containing the path to the action configuration
        :param gestures: string containing the path to the gestures configuration
        """
        super(EventDispatcher, self).__init__(*args, **kwarg)
        self._event_loop = el
        self._gdb = GestureDatabase()
        self._actions = Actions(config, gestures)
        self.update_devices()
        self._multitouches = []

    def update_devices(self):
        log.debug('update_devices()')
        context = pyudev.Context()
        for device in context.list_devices(subsystem='input', ID_INPUT_MOUSE=True):
            if device.sys_name.startswith('event'):
                if 'PRODUCT' in device.parent.keys():
                    self._actions.update_gestures(device.parent['PRODUCT'])
        for gest_n, gest_r in self._actions.get_gestures().iteritems():
            for g in gest_r:
                g = self._gdb.str_to_gesture(g)
                g.normalize()
                g.name = gest_n
                self._gdb.add_gesture(g)

    def on_touch_down(self, touch):
        """
        listening function executed at begining of touch event
        builds the gesture
        """
        self._multitouches.append(touch)
        touch.ud['line'] = Line(points=(touch.sx, touch.sy))
        return True

    def on_touch_move(self, touch):
        """
        listening function executed during touch event
        store points of the gesture
        """
        # store points of the touch movement
        try:
            touch.ud['line'].points += [touch.sx, touch.sy]
            return True
        except (KeyError), e:
            pass

    def on_touch_up(self, touch):
        """
        touch is over, display informations, and check if it matches some
        known gesture.
        """
        if len(self._multitouches) is 0:
            return True

        log.debug("multitouches: \t%d" % len(self._multitouches))
        gestures = map(lambda g: self._gdb.find(make_gesture('',zip(touch.ud['line'].points[::2],
                                            touch.ud['line'].points[1::2])), minscore=0.70), self._multitouches)

        if not self._actions.dispatch(gestures, self._gdb):
            for touch in self._multitouches:
                log.debug("Touch:\t%s" % self._gdb.gesture_to_str(make_gesture('',zip(touch.ud['line'].points[::2],
                                                                                      touch.ud['line'].points[1::2]))))

        self._multitouches = []

    def on_motion(self, etype, me):
        """
        dispatches motion events
        """
        if etype == "begin":
            self.on_touch_down(me)
        elif etype == "update":
            self.on_touch_move(me)
        elif etype == "end":
            self.on_touch_up(me)
        else:
            log.error("Receive unknown event of type '%r': %s" % (etype, me))

    def dispatch(self, ev_type, ev_action, ev):
        """
        dispatches motion events
        """
        if ev_type == "on_motion":
            self.on_motion(ev_action, ev)
        else:
            log.error("asking to dispatch unknown event: '%r': '%r'" % (ev_type, ev))

