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
