#!/usr/bin/env python
#    Copyright 2015 Tobias Mueller <muelli@cryptobitch.de>
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

import avahi

# These are local imports
from network import avahi_txt_dict # for the txt_array_to_dict function
from network.AvahiBrowser import AvahiBrowser


class AvahiListener(AvahiBrowser):
    "This class saves the discovered services in a list"
    
    def __init__(self, service_type, *args, **kwargs):
        '''Initialises the listener with an empty list of discovered
        services
        '''
        self.log = logging.getLogger()
        self._discovered_services = []
        self.log.debug('Starting Browser')
        ## We could also think of a design of a class
        ## which is not a subclass of AvahiBrowser.
        ## In that case, we'd need to create a browser
        ## like this:
        #self.browser = AvahiBrowser(service_type=service_type)
        #self.browser.connect('new_service', self.on_service_resolved)
        #self.browser.connect('remove_service', self.on_service_removed)
        super(AvahiListener, self).__init__(
            service_type=service_type, *args, **kwargs)
    

    def on_service_resolved(self, #browser,
        #name, address, port, txt):
        interface, protocol, name, \
        stype, domain,host, aprotocol, address, port, txt, flags):
        '''This overloads the parent class and appends the discovered
        service to the internal list of discovered services.
        '''
        txt = avahi.txt_array_to_dict(txt)
        service = (interface, protocol, name,
            stype, domain, host, aprotocol, address, port, txt, flags)
        self.log.debug('Adding to the list of services: %s', service)
        self._discovered_services.append(service)

        super(AvahiListener, self).on_service_resolved(
            #name, address, port, txt)
            interface, protocol, name,
            stype, domain, host, aprotocol, address, port, txt, flags)
    
    
    def on_service_removed(self, #browser, service_type, name):
        interface, protocol, name, stype, domain, flags):
        '''Removes the service from the internal list'''
        self.log.debug('Attempting to remove from list: %s', name)
        for service in self._discovered_services:
            if service[2] == name:
                self._discovered_services.remove(service)
        super(AvahiListener, self).on_service_removed(#browser,
            #service_type, name)
            interface, protocol, name, stype, domain, flags)


    def get_discovered_services(self):
        '''Returns the internal list of discovered services'''
        return self._discovered_services


    discovered_services = property(fget=get_discovered_services)


class AvahiClientProvider(AvahiListener):
    '''This class provides the clients suitable for
    being consumed by a GNOME Keysign client,
    i.e. it only returns certain fields of the
    discovered services.
    '''
    def get_discovered_services(self):
        '''Returns the internal list of discovered services'''
        #service = (interface, protocol, name,
        #    stype, domain, host, aprotocol, address, port, txt, flags)
        l = [(s[2], s[7], s[8], s[9]['fingerprint'])
                for s in self._discovered_services]
        self.log.debug('Returning discovered clients: %s', l)
        return l

    discovered_services = property(fget=get_discovered_services)


def main(args=None):
    from gi.repository import GLib
    a = args and args[0] or '_geysign._tcp'
    al = AvahiListener(service_type=a)
    GLib.MainLoop().run()


if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main(sys.argv[1:]))    
