#!/usr/bin/env python
#    Copyright 2014 Andrei Macavei <andrei.macavei89@gmail.com>
#    Copyright 2014, 2015 Tobias Mueller <muelli@cryptobitch.de>
#    Copyright 2015 Jody Hansen <jobediah.hansen@gmail.com>
#
#    This file is part of GNOME Keysign.
#
#    GNOME Keysign is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    GNOME Keysign is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GNOME Keysign.  If not, see <http://www.gnu.org/licenses/>.

import logging
import signal
import sys

from client_provider import AvahiClientProvider
from network.AvahiPublisher import AvahiPublisher

from gi.repository import Gtk, GLib, Gio
from KeySignSection import KeySignSection
from GetKeySection import GetKeySection

class MainWindow(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(
            self, application_id=None) ### org.gnome.Geysign ###
        self.connect("activate", self.on_activate)
        self.connect("startup", self.on_startup)

        self.log = logging.getLogger()
        self.log = logging



    def on_quit(self, app, param=None):
        self.quit()


    def on_startup(self, app):
        self.log.info("Startup")
        self.window = Gtk.ApplicationWindow(application=app)
        self.window.set_title ("Keysign")

        self.window.set_border_width(10)
        self.window.set_position(Gtk.WindowPosition.CENTER)

        # create notebook container
        notebook = Gtk.Notebook()
        notebook.append_page(KeySignSection(), Gtk.Label('Keys'))
        notebook.append_page(GetKeySection(AvahiClientProvider(service_type='_geysign._tcp')),
                             Gtk.Label('Get Key'))
        self.window.add(notebook)

        quit = Gio.SimpleAction(name="quit", parameter_type=None)
        self.add_action(quit)
        self.add_accelerator("<Primary>q", "app.quit", None)
        quit.connect("activate", self.on_quit)

        ## App menus
        appmenu = Gio.Menu.new()
        section = Gio.Menu.new()
        appmenu.append_section(None, section)

        some_action = Gio.SimpleAction.new("scan-image", None)
        some_action.connect('activate', self.on_scan_image)
        self.add_action(some_action)
        some_item = Gio.MenuItem.new("Scan Image", "app.scan-image")
        section.append_item(some_item)

        quit_item = Gio.MenuItem.new("Quit", "app.quit")
        section.append_item(quit_item)

        self.set_app_menu(appmenu)


    def on_scan_image(self, *args, **kwargs):
        print("scanimage")


    def on_activate(self, app):
        self.log.info("Activate!")
        #self.window = Gtk.ApplicationWindow(application=app)

        self.window.show_all()
        # In case the user runs the application a second time,
        # we raise the existing window.
        # self.window.present()



def main():
    app = MainWindow()

    try:
        GLib.unix_signal_add_full(GLib.PRIORITY_HIGH, signal.SIGINT, lambda *args : app.quit(), None)
    except AttributeError:
        pass

    exit_status = app.run(None)

    return exit_status

if __name__ == '__main__':
    sys.exit(main())
