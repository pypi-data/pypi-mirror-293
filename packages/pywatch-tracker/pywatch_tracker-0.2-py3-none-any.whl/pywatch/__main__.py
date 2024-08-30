import sys

from .readout.measurement import measurement_from_script
from .readout.port_access import input_ports_from_commandline
from .server import start_webapp


if len(sys.argv) > 1:
    path = sys.argv[2]
    if sys.argv[1] == "--measurement":
        measurement_from_script(path)
    elif sys.argv[1] == "--webapp":
        start_webapp(path)
    elif sys.argv[2] == "--set-ports":
        input_ports_from_commandline()
