import unittest
import mock

from pyfleet.fleet import Fleet


def read_fleetctl_list_units():
    _data = None
    with open('tests/fleetctl_list_output.txt', 'r') as _fd:
        _data = _fd.read()
    return _data


def read_fleetctl_list_machines():
    _data = None
    with open('tests/fleetctl_list_machines_full.txt', 'r') as _fd:
        _data = _fd.read()
    return _data


class TestFleet(unittest.TestCase):
    fleet = None

    @mock.patch('pyfleet.fleet.Fleet._list_machines')
    def setUp(self, mock__list_machines):
        mock__list_machines.return_value = read_fleetctl_list_machines()
        self.fleet = Fleet()

    @mock.patch('pyfleet.fleet.Fleet._list_units')
    def test_fleetctl_list_units(self, mock__list_units):
        mock__list_units.return_value = read_fleetctl_list_units()

        units = self.fleet.list_units()
        self.assertTrue(len(units) > 0)
        self.assertTrue(units[0]['unit'] == 'api.blue@production.service')
        self.assertTrue('active' in [unit['active'] for unit in units])
        self.assertTrue('inactive' in [unit['active'] for unit in units])
