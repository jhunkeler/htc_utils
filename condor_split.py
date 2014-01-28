#!/usr/bin/env python
import argparse
import os
import sys
import fnmatch
import shutil
import tempfile

VERBOSE = False

def path_search(p, ext, strip_components):
    filenames = []
    p = os.path.abspath(p)
    index = 1
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
                        # strip_components = strip_max
                        print("Warning: Cannot strip {} components from {} (max {})".format(strip_components, path, strip_max))

                if VERBOSE:
                    print("[{}]:{}".format(index, path))
                filenames.append(path)
                index += 1
    return filenames

def generate_manifest(manifest):
    dest = tempfile.NamedTemporaryFile("w+", delete=False)
    for line in manifest:
        dest.write(line + os.linesep)
    return dest.name

def assign_chunks(manifest, chunks, output_dir, as_jobs=False):
    label = 0
    count = 0
    written = 0
    # max_chunks = 0
    dest = None
    output_dir = os.path.abspath(output_dir)

    if VERBOSE:
        print("Output directory: {}".format(output_dir))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)

    if as_jobs:
        manifest_count = len(file(manifest, 'r').readlines())
        max_chunks = manifest_count / chunks
        chunks = max_chunks


    for line in open(manifest, 'r'):
        line = line.strip(os.linesep)
        line += " "
        if count % chunks == 0:
            if dest:
                dest.close()
                if VERBOSE:
                    print("[{}]: {}, {} entries".format(label, os.path.basename(dest.name), written))
                written = 0
            dest = file(os.path.join(output_dir, "stdin." + str(label)), 'w')
            label += 1
        dest.write(line)
        count += 1
        written += 1
    os.unlink(manifest)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strip-components", default=0, type=int, help="Top-level directories to strip")
    parser.add_argument("--output-dir", default="input")
    parser.add_argument("--extension", default="*.*", type=str, help="Extension of files")
    parser.add_argument("--chunks", default=1, type=int, help="Number of entries per file")
    parser.add_argument("--as-jobs", action="store_true", help="Number of expected jobs")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("search_path", action="store", type=str, help="Directory to search under")
    args = parser.parse_args()

    global VERBOSE
    VERBOSE = args.verbose
    chunks = args.chunks
    if chunks < 1:
        chunks = 1
    index_at = 0

    files = path_search(args.search_path, args.extension, args.strip_components)
    if files:
        index_at = 1

    if VERBOSE:
        print("{} files".format(len(files)))

    if not files:
        exit(0)

    manifest = generate_manifest(files)
    assign_chunks(manifest, chunks, args.output_dir, as_jobs=args.as_jobs)

if __name__ == "__main__":
    main()
