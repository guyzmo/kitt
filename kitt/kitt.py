#!/usr/bin/env python

import sys
import argparse

from daemon import Daemon

def run():
    """
    main function that parses the cli arguments and starts the application
    """
    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description="KiTT: Kivy Touch Tool")
    parser.add_argument("-v", "--verbose",
                        dest="verbose",
                        action="store_true",
                        help="Enable verbose output")
    parser.add_argument("-c", "--config",
                        dest="config",
                        action="store",
                        default="~/.kivy/kitt_config.json",
                        help="Select the gesture plugin")
    parser.add_argument("-g", "--gestures",
                        dest="gestures",
                        action="store",
                        default="~/.kivy/kitt_gestures.json",
                        help="Select the gesture plugin")
    parser.add_argument("-p", "--pid",
                        dest="pid",
                        action="store",
                        default="/tmp/kitt.pid",
                        help="Where to store PID file")

    subparsers = parser.add_subparsers(
                        help='Daemon commands',
                        dest='commands')

    def main(args):
        """
        subfunction that launches the application
        """
        sys.argv = sys.argv[0:1]
        from kivy.logger import Logger, logging
        log = Logger.getChild("KiTT")
        if args.verbose:
            Logger.setLevel(logging.DEBUG)
        else:
            Logger.setLevel(logging.ERROR)
        from kivy.base import EventLoop, runTouchApp
        from listener import Listener

        EventLoop.add_event_listener(Listener(args.config, args.gestures))
        runTouchApp()

    class Main(Daemon):
        """
        Daemonification class
        """
        def run(self):
            main(self.args)

    def do_start(args):
        Main(args.pid, args=args).start()

    def do_stop(args):
        Main(args.pid, args=args).stop()

    def do_foreground(args):
        main(args)

    subparsers.add_parser('start',
                          help = "Start daemon").set_defaults(func=do_start)
    subparsers.add_parser('stop',
                          help = "Stop daemon").set_defaults(func=do_stop)
    subparsers.add_parser('foreground',
                          help = "Start in foreground").set_defaults(func=do_foreground)

    args = parser.parse_args(sys.argv[1:])
    args.func(args)

if __name__ == "__main__":
    run()

