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
import os
import sys
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", help="Be more verbose")
    parser.add_argument("job", action="store", help="Path to executable")
    parser.add_argument("indata", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="Standard input")
    args = parser.parse_args()

    verbose = args.verbose

    job = [os.path.abspath(args.job)]
    indata = args.indata
    output = []
    if isinstance(indata, file):
        for line in indata.readlines():
            line = line.strip()
            line = os.path.abspath(line)
            output.append(line)
    else:
        output = indata

    compiled = job + output
    if verbose:
        print("Job: {0}".format(compiled))

    process = subprocess.Popen(compiled, stdout=sys.stdout, stderr=sys.stderr)
    process.communicate()
    process.wait()


if __name__ == "__main__":
    main()
