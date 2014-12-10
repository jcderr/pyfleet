import subprocess


class Machine(object):
    fleet = None
    machine = None
    ip = None
    metadata = {}

    def __init__(self, fleet, datagram):
        self.fleet = fleet
        self.machine = datagram['machine_id']
        self.ip = datagram['ip_address']
        self.metadata = self._set_metadata(datagram['metadata'])

    def _set_metadata(self, md):
        _metadata = {}
        for _var in md.split(','):
            _k, _v = _var.split('=')
            _metadata[_k] = _v
        return _metadata

    def __repr__(self):
        return "<Machine %s>" % self.machine


class Fleet(object):
    machines = []
    units = []

    def __init__(self):
        self.machines = self._get_machines()

    def _list_units(*args):
        _cmd = ['fleetctl', 'list-units']
        _cmd.extend(args)
        return subprocess.check_output(_cmd)

    def _list_machines(*args):
        _cmd = ['fleetctl', 'list-machines']
        _cmd.extend(args)
        return subprocess.check_output(_cmd)

    def _get_machines(self):
        _machines = []
        _resp = self._list_machines('-l', '--no-legend').split("\n")

        for _line in _resp:
            if len(_line):
                _mid, _ip, _md = _line.split()
                _machine = Machine(self, {
                    'machine_id': _mid,
                    'ip_address': _ip,
                    'metadata': _md,
                })
                _machines.append(_machine)
        return _machines

    def machines_matching(self, metadata):
        """
        return a list of machines only matching specific metadata
        """
        _k, _v = metadata.split('=')
        _machines = []
        for machine in self.machines:
            if _k in machine.metadata.keys():
                if machine.metadata[_k] == _v:
                    _machines.append(machine)

        return _machines

    def load(self, units):
        _cmd = ['fleetctl', 'load']
        if isinstance(units, basestring):
            units = [units]
        _cmd.extend(units)
        print subprocess.check_output(_cmd)

    def unload(self, units):
        _cmd = ['fleetctl', 'unload']
        if isinstance(units, basestring):
            units = [units]
        _cmd.extend(units)
        print subprocess.check_output(_cmd)

    def start(self, units):
        _cmd = ['fleetctl', 'start']
        if isinstance(units, basestring):
            units = [units]
        _cmd.extend(units)
        print subprocess.check_output(_cmd)

    def stop(self, units):
        _cmd = ['fleetctl', 'stop']
        if isinstance(units, basestring):
            units = [units]
        _cmd.extend(units)
        print subprocess.check_output(_cmd)

    def list_units(self, *args, **kwargs):
        datagram = []
        _out = self._list_units('fleetctl',
                                'list-units',
                                '-no-legend',
                                '-full',
                                '-fields',
                                'active,hash,load,machine,sub,unit')
        for _line in _out.split('\n'):
            if len(_line.split()) > 0:
                _active, _hash, _load, _machine_ip, _sub, _unit = _line.split()
                _datagram = {
                    'active': _active,
                    'hash': _hash,
                    'load': _load,
                    'machine': _machine_ip.split('/')[0],
                    'ip': _machine_ip.split('/')[1],
                    'sub': _sub,
                    'unit': _unit,
                }
                datagram.append(_datagram)
        return datagram
