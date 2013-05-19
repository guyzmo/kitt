#!/usr/bin/env python

import logging
log = logging.getLogger("KiTT")

import os.path
import sys
import imp
import argparse

from kivy.base import EventLoop, runTouchApp

from listener import Listener


def run():
    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description="KiTT: Kivy Touch Tool")
    parser.add_argument("-v", "--verbose",
                        dest="verbose",
                        action="store_true",
                        help="Enable verbose output")
    parser.add_argument("-p", "--plugin",
                        dest="plugin",
                        action="store",
                        default="wmck",
                        help="Select the gesture plugin")
    args = parser.parse_args(sys.argv[1:])

    if args.verbose: level = logging.DEBUG
    else:            level = logging.ERROR

    logging.basicConfig(stream=sys.stdout, level=level)

    plugin = imp.load_source("plugin_%s" % args.plugin,
                             "%s/plugin_%s.py" % (os.path.dirname(__file__), args.plugin))

    EventLoop.add_event_listener(Listener(plugin.Actions))
    runTouchApp()



if __name__ == "__main__":
    run()

