import unittest
import mock

from pyfleet.fleet import Fleet
from pyfleet.fleet import FleetctlResult


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

    @mock.patch('pyfleet.fleet.Fleetctl.call')
    def setUp(self, mock_call):
        mock_call.return_value = read_fleetctl_list_machines()
        self.fleet = Fleet()

    @mock.patch('pyfleet.fleet.Fleetctl.call')
    def test_fleetctl_list_units(self, mock_call):
        mock_call.return_value = read_fleetctl_list_units()

        units = self.fleet.list_units()
        self.assertEqual(len(units), 26)
        self.assertEqual(units[0].name, 'api.blue@production.service')
        self.assertTrue('active' in [unit.status for unit in units])
        self.assertTrue('inactive' in [unit.status for unit in units])

    @mock.patch('pyfleet.fleet.Fleetctl.call')
    def test_fleetctl_list_machines(self, mock_call):
        mock_call.return_value = read_fleetctl_list_machines()
        machines = self.fleet.list_machines()
        self.assertEqual(len(machines), 10)
        self.assertEqual(machines[0].ip, '172.31.49.159')
        self.assertEqual(machines[0].metadata['environment'], 'production')

