#!/usr/bin/env python
#
# This file is part of htc_utils.
#
# htc_utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# htc_utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with htc_utils.  If not, see <http://www.gnu.org/licenses/>.


import argparse
import htc_utils
import os
import time


# We create a reference Job object to make a copy of the initial class state
nulljob = htc_utils.Job('NULL')

parser = argparse.ArgumentParser()
parser.add_argument('--infile', nargs='?', type=argparse.FileType('r'))
parser.add_argument('--stdout', action='store_true', help='Output job to stdout instead of a file')
parser.add_argument('--logging', action='store', default='logs')
parser.add_argument('-n', '--jobname', action='store', default=str(int(time.time())), help='Output filename without extension (Default: {Unix Epoch}.job')
parser.add_argument('-q', '--queue', action='store', default='', help='Queue main job N times')
parser.add_argument('-b', '--subqueue', action='store', default='', help='Queue sub-job N times')
parser.add_argument('-s', '--subarg', action='append')

# Sort by key, then by value
sorted_args = sorted(nulljob.config.items(), key=lambda record: record[0], reverse=False)
sorted_args = sorted(sorted_args, key=lambda record: record[1], reverse=True)

# nulljob is no longer required
del nulljob

# Proccess argument list and assign default values to the argument parser
for attr, value in sorted_args:
    if attr == 'executable':
        continue
    elif attr == 'arguments':
        continue

    default_value = '(Default: {0})'.format(value) if value else ''
    parser.add_argument('--' + attr, default=value, help=default_value)

args = parser.parse_args()

if not args.infile:
    parser.add_argument('executable')
    parser.add_argument('args', nargs='*')

args = parser.parse_args()

# Let's begin writing our HTCondor job
job = htc_utils.Job(args.jobname)

# Populate job attributes based on argparse input
for key, value in vars(args).items():
    # Ignore foreign keys
    if key not in job.config:
        continue
    job.attr(key, value)

if args.logging:
    job.logging(args.logging, create=True)

if args.infile:
    warnings = []
    for index, line in enumerate(args.infile.readlines()):
        in_args = line.rstrip()
        in_args = line.split()
        if len(in_args) < 2:
            warnings.append('# Warning: No argument(s) defined for: "{0}", in "{1}", line {2}'.format(''.join(in_args), args.infile.name, index + 1))
        job.subattr('executable', in_args[0])
        job.subattr('arguments', in_args[1:])
        job.subattr('queue')

    for warning in warnings:
        print(warning)

else:
    # Manually assign important variables
    job.attr('executable', args.executable)
    job.attr('arguments', args.args)
    job.attr('queue', args.queue)

    # Process any sub-attributes we may have
    if args.subarg is not None:
        for subarg in args.subarg:
            job.subattr('arguments', subarg)
            job.subattr('queue', args.subqueue)

if args.stdout:
    print(job.generate())
else:
    job.commit()
    print('Wrote: {0}'.format(job.filename))

