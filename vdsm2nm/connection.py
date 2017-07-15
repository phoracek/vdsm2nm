# Copyright (C) 2017 Petr Horacek <phoracek@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import


class NoValue(object):
    pass


def rget(dictionary, keys, default=NoValue):
    if dictionary is NoValue:
        if default is not NoValue:
            return default
        raise KeyError()
    elif len(keys) == 0:
        return dictionary
    return rget(dictionary.get(keys[0], NoValue), keys[1:], default)


def rset(dictionary, keys, value):
    if len(keys) == 1:
        dictionary[keys[0]] = value
    else:
        rset(dictionary.setdefault(keys[0], {}), keys[1:], value)
