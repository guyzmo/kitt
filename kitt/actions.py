#!/usr/bin/env python

from kivy.logger import Logger
log = Logger.getChild("KiTT")

import gtk
import sys
import imp
import json
import os.path

class Actions():
    """
    This class loads all the actions and gesture, and does the binding between
    them. Then, when a gesture is found by the listener, the gesture gets dispatched.
    """
    def __init__(self, actions_config, gestures_config):
        """
        Build and load actions and gestures from files
        :param actions_config: string containing the path to the actions JSON file
        :param gestures_config: string containing the path to the gestures JSON file
        """
        self._actions = dict(pinch_in=[],
                             pinch_out=[],
                             two_swipe_up=[],
                             two_swipe_down=[],
                             two_swipe_left=[],
                             two_swipe_right=[],
                             three_swipe_up=[],
                             three_swipe_down=[],
                             three_swipe_left=[],
                             three_swipe_right=[],
                             four_swipe_up=[],
                             four_swipe_down=[],
                             four_swipe_left=[],
                             four_swipe_right=[])
        self._functions = dict()
        self._gestures = dict()
        try:
            with open(os.path.expanduser(gestures_config)) as config:
                self._gestures = json.load(config)
            with open(os.path.expanduser(actions_config)) as config:
                config = json.load(config)
                for engine in config['engines']:
                    plugin = imp.load_source("kitt.plugin_%s" % engine,
                                            "%s/plugin_%s.py" % (os.path.dirname(__file__), engine))
                    self._functions.update(plugin.ACTIONS)
                actions = config["actions"]
                for gesture, act_l in self._actions.iteritems():
                    if gesture in actions.keys():
                        for action in actions[gesture]:
                            act_l.append(action)
                    else:
                        log.error("Unable to load gesture: '%s' unknown" % gesture)
        except IOError:
            log.debug("No configuration file found")

    def get_gestures(self):
        """
        :return: the gesture dict
        """
        return self._gestures

    def before(self):
        """
        safeguard function to be called before a touch is defined
        """
        pass

    def after(self):
        """
        safeguard function to be called after a touch is defined
        """
        pass

    def dispatch(self, gestures, gdb):
        """
        dispatches found gestures, matched using the gesture database into
        gesture events.
        :param gestures: list of live gestures
        :param gdb: kivy's gesture database object
        """
        d = u = l = r = 0
        for gesture in gestures:
            if gesture is None:
                log.warning("Undefined touch")
                continue
            gesture = gesture[1]
            if gesture:
                if   gesture.name == 'move_down':  d += 1
                elif gesture.name == 'move_up':    u += 1
                elif gesture.name == 'move_left':  l += 1
                elif gesture.name == 'move_right': r += 1
                else:
                    log.warn("Unknown gesture")
            else:
                log.info("gesture: \t%s" % gdb.gesture_to_str(gesture))
                for gest_n, gest_r in self._gestures.iteritems():
                    s = gest_n, "\t",
                    for g2 in gest_r:
                        g2 = gdb.str_to_gesture(g2)
                        g2.normalize()
                        s += g2.get_score(gesture),
                    log.debug(s)

        if   u is 4 and d == l == r == 0: gesture = "four_swipe_up"
        elif d is 4 and u == l == r == 0: gesture = "four_swipe_down"
        elif l is 4 and u == d == r == 0: gesture = "four_swipe_left"
        elif r is 4 and u == d == l == 0: gesture = "four_swipe_right"
        elif u is 3 and d == l == r == 0: gesture = "three_swipe_up"
        elif d is 3 and u == l == r == 0: gesture = "three_swipe_down"
        elif l is 3 and u == d == r == 0: gesture = "three_swipe_left"
        elif r is 3 and u == d == l == 0: gesture = "three_swipe_right"
        elif u is 2 and d == l == r == 0: gesture = "two_swipe_up"
        elif d is 2 and u == l == r == 0: gesture = "two_swipe_down"
        elif l is 2 and u == d == r == 0: gesture = "two_swipe_left"
        elif r is 2 and u == d == l == 0: gesture = "two_swipe_right"
        else:
            log.warn("Gesture:\tNot found")
            return False

        for act in self._actions[gesture]:
            fun = act["function"]
            prm = act["parameters"]

            if fun in self._functions.keys():
                self._functions[fun](**prm)
            else:
                log.error("Action not found: %s" % fun)

        return True

