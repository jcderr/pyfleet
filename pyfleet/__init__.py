import sys
import os

from . import fleet as _fleet


# Ensure that fleetctl is available on the path
_fleetctl = None
for pth in os.environ.get('PATH', None).split(':'):
    if os.path.exists(os.path.join(pth, 'fleetctl')):
        _fleetctl = os.path.join(pth, 'fleetctl')

if not _fleetctl:
    print "The fleetctl binary is not on your PATH."
    sys.exit(-1)
