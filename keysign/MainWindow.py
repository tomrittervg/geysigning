#!/usr/bin/env python
#    Copyright 2014 Andrei Macavei <andrei.macavei89@gmail.com>
#    Copyright 2014 Tobias Mueller <muelli@cryptobitch.de>
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

from network.AvahiPublisher import AvahiPublisher

from gi.repository import Gtk, GLib, Gio
from Sections import KeySignSection, GetKeySection

import SigneesWindow

import Keyserver

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
        notebook.append_page(KeySignSection(self), Gtk.Label('Keys'))
        notebook.append_page(GetKeySection(self), Gtk.Label('Get Key'))
        self.window.add(notebook)

        quit = Gio.SimpleAction(name="quit", parameter_type=None)
        self.add_action(quit)
        self.add_accelerator("<Primary>q", "app.quit", None)
        quit.connect("activate", self.on_quit)

        # Avahi services
        self.avahi_browser = None
        self.avahi_service_type = '_geysign._tcp'
        self.discovered_services = []
        GLib.idle_add(self.setup_avahi_browser)

        self.keyserver = None
        self.port = 9001

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
        self.signeeswindow = SigneesWindow.SigneesWindow(self.discovered_services)
        # In case the user runs the application a second time,
        # we raise the existing window.
        # self.window.present()


    def setup_server(self, keydata, fingerprint):
        """
        Starts the key-server which serves the provided keydata and
        announces the fingerprint as TXT record using Avahi
        """
        self.log.info('Serving now')
        self.log.debug('About to call %r', Keyserver.ServeKeyThread)
        self.keyserver = Keyserver.ServeKeyThread(str(keydata), fingerprint)
        self.log.info('Starting thread %r', self.keyserver)
        self.keyserver.start()
        self.log.info('Finsihed serving')
        return False

    def stop_server(self):
        self.keyserver.shutdown()
        self.setup_avahi_browser()
        #self.setup_server("New string", None)
        #keyserver is shut down when key is removed from list.


    def update_signees_window(self, discovered_services):
        '''Creates a new list of fpr signatures from discovered services and counts the number
        of unique fprs. Passes this argument to the SigneesWindow widget'''
        fpr_list = []
        [fpr_list.append(clients[3]) for clients in discovered_services if clients[3] != "None"]
        unique_fpr = len(set(fpr_list))
        self.signeeswindow.reset_label(unique_fpr)

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
