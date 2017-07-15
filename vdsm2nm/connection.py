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

import abc
import itertools

import six


@six.add_metaclass(abc.ABCMeta)
class Connection(object):

    @staticmethod
    def _fields():
        pass

    @classmethod
    def from_settings(cls, settings):
        connection = Connection()
        fields = cls._fields()
        for field in fields:
            field.from_settings(settings)
        connection._fields = fields
        return connection

    def to_settings(self):
        settings = {}
        for field in self._fields:
            field.to_settings(settings)
        return settings


class Bridge(Connection):

    @staticmethod
    def _fields():
        return list(itertools.chain.from_iterable([
            _connection_fields()
        ]))


class Ethernet(Connection):

    @staticmethod
    def _fields():
        return list(itertools.chain.from_iterable([
            _connection_fields()
        ]))


def _connection_fields():
    return [
        Field(('connection', 'id')),
        Field(('connection', 'type')),
        Field(('connection', 'interface-name')),
        Field(('connection', 'autoconnect'), True),
        Field(('connection', 'autoconnect-priority'), 0),
        Field(('connection', 'master'), None),
        Field(('connection', 'slave-type'), None)
    ]


class NoValue(object):
    pass


class Field(object):

    def __init__(self, keys, default=NoValue):
        self._keys = keys
        self._default = default
        self._value = NoValue

    def from_settings(self, settings):
        self._value = rget(settings, self._keys, self._default)
        if self._value == NoValue:
            raise KeyError('Value not found.')

    def to_settings(self, settings):
        if self._value == NoValue:
            raise ValueError('Value not set.')
        rset(settings, self._keys, self._value)


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
