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

"""This monkeypatches avahi to provide a txt_array_to_dict function.
This should probably be upstreamed.
Unfortunately, upstream seems rather inactive.
"""
import avahi

if getattr(avahi, 'txt_array_to_dict', None) is None:
    # This has been taken from Gajim
    # http://hg.gajim.org/gajim/file/4a3f896130ad/src/common/zeroconf/zeroconf_avahi.py
    # it is licensed under the GPLv3.
    def txt_array_to_dict(txt_array):
        txt_dict = {}
        for els in txt_array:
            key, val = '', None
            for c in els:
                    #FIXME: remove when outdated, this is for avahi < 0.6.14
                    if c < 0 or c > 255:
                        c = '.'
                    else:
                        c = chr(c)
                    if val is None:
                        if c == '=':
                            val = ''
                        else:
                            key += c
                    else:
                        val += c
            if val is None: # missing '='
                val = ''
            txt_dict[key] = val.decode('utf-8')
        return txt_dict

    setattr(avahi, 'txt_array_to_dict', txt_array_to_dict)
