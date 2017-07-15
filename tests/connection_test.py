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

import pytest

from vdsm2nm import connection


@pytest.mark.unit
class TestDictionaryHelpers(object):

    def test_rget(self):
        source = {'foo': {'bar': 1}}
        value = connection.rget(source, ('foo', 'bar'))
        assert value == 1

    def test_rget_without_default(self):
        source = {'foo': {'shrubbery': 1}}
        with pytest.raises(KeyError):
            connection.rget(source, ('foo', 'bar'))

    def test_rget_with_default(self):
        source = {'foo': {'shrubbery': 1}}
        value = connection.rget(source, ('foo', 'bar'), default=1)
        assert value == 1

    def test_rset(self):
        destination = {'foo': {}}
        connection.rset(destination, ('foo', 'bar'), 1)
        assert destination == {'foo': {'bar': 1}}

    def tests_rset_with_missing_destination_dictionary(self):
        destination = {}
        connection.rset(destination, ('foo', 'bar'), 1)
        assert destination == {'foo': {'bar': 1}}


@pytest.mark.unit
class TestField(object):

    def test_read_and_write(self):
        source = {'foo': 1, 'bar': 2}
        expected_destination = {'foo': 1}
        field = connection.Field(('foo',))

        self._test_read_and_write(source, expected_destination, field)

    def test_read_and_write_with_defaults(self):
        source = {'bar': 2}
        expected_destination = {'foo': 1}
        field = connection.Field(('foo',), 1)

        self._test_read_and_write(source, expected_destination, field)

    def test_read_and_write_with_missing_destination_dictionary(self):
        source = {'foo': {'bar': 1}}
        expected_destination = {'foo': {'bar': 1}}
        field = connection.Field(('foo',))

        self._test_read_and_write(source, expected_destination, field)

    def _test_read_and_write(self, source, expected_destination, field):
        field.from_settings(source)

        destination = {}
        field.to_settings(destination)

        assert destination == expected_destination

    def test_read_and_write_missing_source_value(self):
        source = {'bar': 2}

        field = connection.Field(('foo',))

        with pytest.raises(KeyError):
            field.from_settings(source)

    def test_write_without_reading(self):
        field = connection.Field(('foo',))

        destination = {}

        with pytest.raises(ValueError):
            field.to_settings(destination)


@pytest.mark.unit
class TestBridgeConnection(object):

    def test_read_and_write_settings(self):
        source = {
            'bridge': {
                'forward-delay': 2,
                'interface-name': 'br0'
            },
            'connection': {
                'autoconnect': False,
                'id': 'br0',
                'interface-name': 'br0',
                'permissions': [],
                'secondaries': [],
                'timestamp': 1500130827,
                'type': 'bridge',
                'uuid': '2b7437ec-b57d-4500-9886-31b53fa3628f'
            }
        }
        expected_destination = {
            'connection': {
                'id': 'br0',
                'type': 'bridge',
                'interface-name': 'br0',
                'autoconnect': False,
                'autoconnect-priority': 0,
                'master': None,
                'slave-type': None
            }
        }

        bridge = connection.Bridge.from_settings(source)

        assert bridge.to_settings() == expected_destination
