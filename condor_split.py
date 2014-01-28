#!/usr/bin/env python
import argparse
import os
import sys
import fnmatch

def path_dive(p, ext, strip_components):
    filenames = []
    p = os.path.abspath(p)
    for root, _, files in os.walk(p):
        for f in files:
            path = os.path.join(root, f)
            if not os.path.isfile(path):
                continue
            if fnmatch.fnmatch(path, ext):
                if strip_components:
                    print("stripping {}".format(strip_components))
                    try:
                        head, tail = os.path.split(path)
                        components = head.split(os.path.sep)[strip_components:]
                        path = os.path.join(os.path.sep.join(components), tail)
                    except IndexError:
                        print("Depth exceeded!  Cannot strip {} components from {}".format(strip_components, path))
                        exit(1)
                filenames.append(path)
    return filenames


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("search_path", nargs="+", help="Directory to search under")
    parser.add_argument("--strip-components", default=0, help="Top-level directories to strip")
    parser.add_argument("--output-dir", default="input")
    parser.add_argument("--extension", default="*.*", help="Extension of files")
    parser.add_argument("--chunks", default=4, help="Number of entries per file")
    args = parser.parse_args()

    for path in args.search_path:
        print("Searching {} for {}".format(path, args.extension))
        print(path_dive(path, args.extension, args.strip_components))



if __name__ == "__main__":
    main()
