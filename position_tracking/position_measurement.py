#!/usr/bin/env python


from __future__ import absolute_import, print_function, division

import argparse      # to parse CLI options
from functools import reduce  # pylint: disable=redefined-builtin
import operator      # for or_
import os            # for os.environ
import re            # for regular expressions
import struct        # for pack()
import sys

PROG_NAME = 'position_measurement'


try:
    import gps
    import gps.ubx
except ImportError:
    # PEP8 says local imports last
    sys.stderr.write("%s: failed to import gps, check PYTHONPATH\n" %
                     PROG_NAME)
    sys.exit(2)

gps_version = '3.22.1~dev'
if gps.__version__ != gps_version:
    sys.stderr.write("%s: ERROR: need gps module version %s, got %s\n" %
                     (PROG_NAME, gps_version, gps.__version__))
    sys.exit(1)

# instantiate the GPS class
gps_model = gps.ubx.ubx()
options = sys.argv[1:]

#  "m:")

usage = '%(prog)s [OPTIONS] [host[:port[:device]]]'
epilog = ('BSD terms apply: see the file COPYING in the distribution '
          'root for details.')

parser = argparse.ArgumentParser(add_help=False, epilog=epilog, usage=usage)
parser.add_argument(
    '-?', '-h', '--help',
    action="store_true",
    dest='help',
    default=False,
    help='Show this help message and exit. Use -v 2, or -v 3, for extra help'
)
parser.add_argument(
    '--device',
    dest='gpsd_device',
    default=None,
    metavar='DEVICE',
    help='The gpsd device to connect to. [Default %(default)s]',
)
parser.add_argument(
    '-f', '--file',
    dest='input_file_name',
    default=None,
    metavar='FILE',
    help='Read from FILE instead of a gpsd instance.',
)
parser.add_argument(
    '--host',
    dest='gpsd_host',
    default=None,
    metavar='HOST',
    help='The gpsd host to connect to.',
)
parser.add_argument(
    '-i', '-portid',
    dest='port',
    default=None,
    metavar='PORTID',
    help=('Specifies receiver PORTID (interface) for port-related commands. '
          '[Default %(default)s]'),
)
parser.add_argument(
    '--port',
    dest='gpsd_port',
    default=gps.GPSD_PORT,
    metavar='PORT',
    type=int,
    help='The gpsd port to connect to. [Default %(default)s]',
)
parser.add_argument(
    '-P', '--protver',
    dest='protver',
    default=20.30,
    type=float,
    help='Protocol version for sending commands. [Default %(default)s]',
)
parser.add_argument(
    '-r', '--readonly',
    action='store_true',
    dest='read_only',
    default=False,
    help='Read only. Do not send anything to the GPS.',
)
parser.add_argument(
    '-R', '--rawfile',
    dest='raw_file',
    default=None,
    metavar='FILE',
    help='Save raw data from receiver in FILE\n',
)
parser.add_argument(
    '-s', '--inspeed',
    choices=gps_model.speeds,
    dest='input_speed',
    default=9600,
    metavar='SPEED',
    type=int,
    help='Set local serial port speed to SPEED bps.',
)
parser.add_argument(
    '-t', '--timestamp',
    action='count',
    dest='timestamp',
    default=0,
    help='Timestamp messages with seconds since UNIX epoch.  Use -tt for UTC',
)
parser.add_argument(
    '-v', '--verbosity',
    dest='verbosity',
    default=0,
    metavar='VERB',
    type=int,
    help='Set verbosity level to V, 0 to 5. [Default %(default)s]',
)
parser.add_argument(
    '-V', '--version',
    action='version',
    version="%(prog)s: Version " + gps_version + "\n",
    help='Output version to stderr, then exit',
)
parser.add_argument(
    'target',
    nargs='?',
    help='[host[:port[:device]]]',
)

# turn the stupid Namespace into a nice dictionary
opts = vars(parser.parse_args(options))

gps_model.port = opts['port']
gps_model.protver = opts['protver']
gps_model.read_only = opts['read_only']
gps_model.timestamp = opts['timestamp']
gps_model.verbosity = opts['verbosity']

if opts['help']:
    parser.print_help()
    if gps.VERB_DECODE <= opts['verbosity']:
        if gps.VERB_DECODE < opts['verbosity']:
            print('\nITEM for -g/--getitem, -x/--delitem and -z/--setitem '
                  'can be one of:')
            for item in sorted(gps_model.cfgs):
                print("    %s\n"
                      "        %s" % (item[0], item[5]))
            print('\n')
    sys.exit(0)

# done parsing arguments from environment and CLI

try:
    # create the I/O instance
    io_handle = gps.gps_io(
        input_file_name=opts['input_file_name'],
        read_only=opts['read_only'],
        gpsd_host=opts['gpsd_host'],
        gpsd_port=opts['gpsd_port'],
        gpsd_device=opts['gpsd_device'],
        input_speed=opts['input_speed'],
        verbosity_level=opts['verbosity'],
        write_requested= False)
    gps_model.io_handle = io_handle

    sys.stdout.flush()

    exit_code = io_handle.read(gps_model.decode_msg,  # decode function
                              expect_statement_identifier="UBX-NAV-RELPOSNED")    # RELPOSNED data

    if ((gps.VERB_RAW <= opts['verbosity']) and io_handle.out):
        # dump raw left overs
        print("Left over data:")
        print(io_handle.out)

    sys.stdout.flush()
    io_handle.ser.close()

except KeyboardInterrupt:
    print('')
    exit_code = 1

sys.exit(exit_code)
# vim: set expandtab shiftwidth=4
