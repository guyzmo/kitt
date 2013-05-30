#!/usr/bin/env python

import sys
import argparse

import threading

from daemon import Daemon

import pyudev
import pyudev.glib

class UdevListener(threading.Thread):
    def __init__(self, gobject_loop, el, listener, log):
        threading.Thread.__init__(self)
        self._gobject_loop = gobject_loop
        self._event_loop = el
        self._listener = listener
        self.log = log

    def device_added(self, observer, device):
        for inp in self._event_loop.input_providers:
            if device.sys_name == inp.device:
                self.log.debug("Device '%s'/'%s' added ; starting event loop" % (device.sys_name, device.parent['PRODUCT']))
                self._event_loop.start()
                self._listener.update_devices()

    def device_removed(self, observer, device):
        for inp in self._event_loop.input_providers:
            if device.sys_name == inp.device:
                self.log.debug("Device '%s' removed ; stopping event loop" % (device.sys_name,))
                self._event_loop.stop()

    def run(self):
        self.log.debug("Starting udev listener")
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        observer = pyudev.glib.GUDevMonitorObserver(monitor)

        observer.connect('device-added', self.device_added)
        observer.connect('device-removed', self.device_removed)

        monitor.enable_receiving()

        self._gobject_loop()


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
        from kivy.base import EventLoop, runTouchApp, stopTouchApp
        from kivy.support import install_gobject_iteration
        from listener import Listener

        listener = Listener(args.config, args.gestures, EventLoop)
        EventLoop.add_event_listener(listener)
        UdevListener(install_gobject_iteration, EventLoop, listener, log).start()
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

