#!/usr/bin/env python

from kivy.logger import Logger, logging
log = Logger.getChild("KiTT")
# Logger.setLevel(logging.ERROR)

import sys
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
    parser.add_argument("-c", "--config",
                        dest="config",
                        action="store",
                        default="~/.kivy/kitt.json",
                        help="Select the gesture plugin")
    args = parser.parse_args(sys.argv[1:])

    if args.verbose:
        Logger.setLevel(logging.DEBUG)

    EventLoop.add_event_listener(Listener(args.config))
    runTouchApp()



if __name__ == "__main__":
    run()

