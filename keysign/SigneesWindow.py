#!/usr/bin/env python
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

from gi.repository import Gdk, Gtk, GdkPixbuf

log = logging.getLogger()

class SigneesWindow(Gtk.Window):
    '''Displays the number of signees available on the network
    in a seperate window.'''

    def __init__(self, data = "Default"):
        '''The data will be passed to the widget'''
        self.log = logging.getLogger()
        Gtk.Window.__init__(self, title="")
        self.connect("delete-event", Gtk.main_quit)
        self.data = str(len(data))
        self.label = Gtk.Label()
        self.label.set_line_wrap(True)
        self.label.set_markup("<b><big>The number of signees on network are: %s</big></b>"%self.data)
        self.set_default_size(200,50)
        self.add(self.label)
        self.show_all()

    def reset_label(self,data):
        data = str(data)
        self.label.set_markup("<b><big>The number of signees on network are: %s</big></b>"%data)
