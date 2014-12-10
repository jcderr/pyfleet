import subprocess


class FleetctlResult(object):
    code = None
    output = None

    def __init__(self, code, output):
        self.code = code
        self.output = output


class Fleetctl(object):
    command = 'fleetctl'

    def __init__(self, *args):
        pass

    def call(self, command):
        try:
            return subprocess.check_output(command)
        except TypeError:
            print 'Attempted checkoutput(' + str(command) + ')'
            import sys
            sys.exit(-1)

    def run(self, *args):
        full_command = [self.command]
        full_command.extend(*args)
        try:
            #import ipdb;ipdb.set_trace()
            _out = self.call(full_command)
            return FleetctlResult(code=0, output=_out)
        except subprocess.CalledProcessError, e:
            return FleetctlResult(code=e.returncode, output=e.output)

    def __str__(self):
        return "<Fleetctl>"


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


class Unit(object):
    name = None
    status = None
    machine = None
    sub = None
    unit_hash = None
    loaded = None
    fleet = None

    def __init__(self, fleet, datagram):
        self.fleet = fleet
        self.name = datagram['unit']
        self.status = datagram['active']
        self.machine = datagram['machine']    # TODO: make this a real machine object # noqa
        self.sub = datagram['sub']
        self.unit_hash = datagram['hash']
        self.loaded = datagram['load']


class Fleet(object):
    machines = []
    units = []
    fleetctl = None

    def __init__(self):
        self.fleetctl = Fleetctl()
        self.machines = self._build_machine_list()
        #import ipdb; ipdb.set_trace();

    def _fleetctl_call(self, *args):
        return self.fleetctl.run(args)

    def _list_units(self, *args):
        """ calls ```fleetctl list-units [args]``` """
        return self._fleetctl_call('list-units', *args)

    def _list_machines(self, *args):
        """ calls ```fleetctl list-machines [args] ``` """
        return self._fleetctl_call('list-machines', *args)

    def _build_machine_list(self):
        """ Builds machine list """
        _machines = []
        _resp = self._list_machines('-l', '--no-legend').output.split('\n')

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

    def list_units(self, *args, **kwargs):
        datagram = []
        units = []
        #import ipdb; ipdb.set_trace()
        _out = self._list_units('-no-legend',
                                '-full',
                                '-fields',
                                'active,hash,load,machine,sub,unit').output
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
        for unit in datagram:
            _unit = Unit(self, unit)
            units.append(_unit)

        return units

    def list_machines(self):
        self.machines = self._build_machine_list()
        return self.machines

    def load(self, units):
        """ calls ```fleetctl load [units] ``` """
        return self._fleetctl_call('load', units)

    def unload(self, units):
        """ calls ```fleetctl unload [units]``` """
        return self._fleetctl_call('unload', units)

    def start(self, units):
        """ calls ```fleetctl start [units]``` """
        return self._fleetctl_call('start', units)

    def stop(self, units):
        """ calls ```fleetctl stop [units]``` """
        return self._fleetctl_call('stop', units)
