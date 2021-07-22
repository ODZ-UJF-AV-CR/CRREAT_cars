"""
Simple command line utility to initialize and stream the parsed UBX output of a u-blox GNSS based moving-baseline measurement.

Usage (all args are optional):
ubxdump.py base_port="/dev/ttyACM0" rover1_port="/dev/ttyACM1" rover2_port="/dev/ttyACM2" baud=9600 timeout=5 ubx_only=0 raw=0

If ubxonly=True (1), streaming will terminate on any non-UBX data (e.g. NMEA).
"""

import sys
from serial import Serial
from pyubx2 import UBXReader

base_port = "/dev/ttyACM0"
rover1_port = "/dev/ttyACM1"
rover2_port = "/dev/ttyACM2"
BAUD = 9600
TIMEOUT = 5


def stream_ubx(**kwargs):
    """
    Stream output
    """

    rover1 = kwargs.get("rover1_port", rover1_port).strip('"')
    baud = int(kwargs.get("baud", BAUD))
    timeout = int(kwargs.get("timeout", TIMEOUT))
    ubxonly = int(kwargs.get("ubxonly", 0))
    rawformat = int(kwargs.get("raw", 0))
    print(
        f"\nStreaming from {rover1_port} at {baud} baud in",
        f"{'raw' if rawformat else 'parsed'} format...\n",
    )

    rover2 = kwargs.get("rover2_port", rover2_port).strip('"')
    baud = int(kwargs.get("baud", BAUD))
    timeout = int(kwargs.get("timeout", TIMEOUT))
    ubxonly = int(kwargs.get("ubxonly", 0))
    rawformat = int(kwargs.get("raw", 0))
    print(
        f"\nStreaming from {rover2_port} at {baud} baud in",
        f"{'raw' if rawformat else 'parsed'} format...\n",
    )

    stream1 = Serial(rover1, baud, timeout=timeout)
    stream2 = Serial(rover2, baud, timeout=timeout)

    try:
        while(True):

            ubr = UBXReader(stream1, ubxonly=ubxonly)
            for (raw, rover1_parsed) in ubr:
                if rover1_parsed.identity == 'NAV-RELPOSNED':
                    break

            ubr = UBXReader(stream2, ubxonly=ubxonly)
            for (raw, rover2_parsed) in ubr:
                if rover2_parsed.identity == 'NAV-RELPOSNED':
                    break


            rover1_N = (rover1_parsed.relPosN + rover1_parsed.relPosHPN/100)/100  # Nord coordinates in meters
            rover1_E = (rover1_parsed.relPosE + rover1_parsed.relPosHPE/100)/100
            rover1_D = (rover1_parsed.relPosD + rover1_parsed.relPosHPD/100)/100

            rover1_accN = rover1_parsed.accN/10000
            rover1_accE = rover1_parsed.accE/10000
            rover1_accD = rover1_parsed.accD/10000

            rover2_N = (rover2_parsed.relPosN + rover2_parsed.relPosHPN/100)/100  # Nord coordinates in meters
            rover2_E = (rover2_parsed.relPosE + rover2_parsed.relPosHPE/100)/100
            rover2_D = (rover2_parsed.relPosD + rover2_parsed.relPosHPD/100)/100

            rover2_accN = rover2_parsed.accN/10000
            rover2_accE = rover2_parsed.accE/10000
            rover2_accD = rover2_parsed.accD/10000


            print("       Rover 1         " + "Rover 2")
            print("N: " + "{:.4f}".format(rover1_N) + "±{:.4f}".format(rover1_accN) + " {:.4f}".format(rover2_N) + "±{:.4f}".format(rover2_accN))
            print("E: " + "{:.4f}".format(rover1_E) + "±{:.4f}".format(rover1_accE) + " {:.4f}".format(rover2_E) + "±{:.4f}".format(rover2_accE))
            print("D: " + "{:.4f}".format(rover1_D) + "±{:.4f}".format(rover1_accD) + " {:.4f}".format(rover2_D) + "±{:.4f}".format(rover2_accD))

    except KeyboardInterrupt:
        print("\nStreaming terminated by user\n")


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] in {"-h", "--h", "help", "-help", "--help", "-H"}:
            print(
                " ubxdump.py is a simple command line utility to stream",
                "the parsed UBX output of a u-blox GNSS device.\n\n",
                "Usage (all args are optional): ubxdump.py",
                'port="COM13" baud=9600 timeout=5',
                "ubxonly=0 raw=0\n\n Type Ctrl-C to terminate.",
            )
            sys.exit()

    stream_ubx(**dict(arg.split("=") for arg in sys.argv[1:]))
