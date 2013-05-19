#!/usr/bin/env python

import logging
log = logging.getLogger("KiTT")

import gtk
import sys

import wnck

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
    def __init__(self):
        screen = wnck.screen_get_default()
        if not screen:
            raise Exception("Default screen not found!")

    def three_swipe_up(self):
        pass

    def three_swipe_down(self):
        pass

    def three_swipe_left(self):
        pass

    def three_swipe_right(self):
        pass

    def two_swipe_up(self):
        pass

    def two_swipe_down(self):
        pass

    def two_swipe_left(self):
        pass

    def two_swipe_right(self):
        pass

    def dispatch(self, gestures, gdb):
        pass


