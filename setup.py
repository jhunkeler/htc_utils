from os import unlink
from os.path import splitext, basename, relpath, join
from shutil import copy2
from setuptools import setup, find_packages

VERSION = "0.1.2"
CLI = relpath('htc_utils/CLI')
scripts_original = [ join(CLI, 'split.py'),
                        join(CLI, 'wrap.py'),
                        join(CLI, 'batch.py') ]
scripts_renamed = [ splitext(x)[0] for x in scripts_original ]
scripts_renamed = [ 'condor_' + basename(x) for x in scripts_renamed ]

for script, script_renamed in zip(scripts_original, scripts_renamed):
    copy2(script, script_renamed)

with open(join('htc_utils', 'version.py'), 'w+') as fp:
    fp.write("__version__ = '{}'\n".format(VERSION))

setup(
    name="htc_utils",
    version=VERSION,
    packages=find_packages(),
    scripts=scripts_renamed,

    # metadata for upload to PyPI
    author="Joseph Hunkeler",
    author_email="jhunkeler@gmail.com",
    url = "https://github.com/jhunkeler/htc_utils",
    description="Home-rolled Condor utilities",
    license="GPL",
    keywords="condor htcondor util",
)

for script in scripts_renamed:
    unlink(script)

