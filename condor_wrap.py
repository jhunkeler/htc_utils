#!/usr/bin/env python
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

    job = [os.path.normpath(args.job)]
    indata = args.indata
    data = []
    if verbose:
        print("Job: {}".format(job))
        if isinstance(indata, file):
            print("Input:"),
            for line in indata.readlines():
                data.append(line)
                print(data)
        else:
            print("Data: {}".format(indata))
            data = indata

    compiled = job + data
    # print(compiled)
    process = subprocess.Popen(compiled)


if __name__ == "__main__":
    main()
