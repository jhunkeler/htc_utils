#!/usr/bin/env python
from os import unlink
from os.path import splitext
from shutil import copy2
from setuptools import setup, find_packages

scripts_original = ['condor_split.py', 'condor_wrap.py']
scripts_renamed = [ splitext(x)[0] for x in scripts_original ]

for script, script_renamed in zip(scripts_original, scripts_renamed):
    copy2(script, script_renamed)

setup(
    name="htcondor_utils",
    version="0.1",
    packages=find_packages(),
    scripts=scripts_renamed,

    # metadata for upload to PyPI
    author="Joseph Hunkeler",
    author_email="jhunkeler@gmail.com",
    description="Home-rolled Condor utilities",
    license="GPL",
    keywords="condor htcondor util",
)

for script in scripts_renamed:
	unlink(script)

