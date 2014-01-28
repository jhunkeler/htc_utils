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
                    head, tail = os.path.split(path)
                    strip_max = len(head.split(os.path.sep))
                    if strip_components <= strip_max:
                        components = head.split(os.path.sep)[strip_components:]
                        path = os.path.join(os.path.sep.join(components), tail)
                    else:
                        #strip_components = strip_max
                        print("Warning: Cannot strip {} components from {} (max {})".format(strip_components, path, strip_max))
                filenames.append(path)
    return filenames

def assign_chunk():
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("search_path", action="store", help="Directory to search under")
    parser.add_argument("--strip-components", default=0, type=int, help="Top-level directories to strip")
    parser.add_argument("--output-dir", default="input")
    parser.add_argument("--extension", default="*.*", help="Extension of files")
    parser.add_argument("--chunks", default=4, help="Number of entries per file")
    args = parser.parse_args()

    paths = path_dive(args.search_path, args.extension, args.strip_components):
    print("{} files".format(len(paths)))
    if not paths:
        exit(0)



if __name__ == "__main__":
    main()
