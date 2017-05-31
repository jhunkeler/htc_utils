from os import unlink
from os.path import splitext, basename, relpath, join
from shutil import copy2
from setuptools import setup, find_packages

CLI = relpath('htc_utils/CLI')
scripts_original = [ join(CLI, 'split.py'),
                        join(CLI, 'wrap.py'),
                        join(CLI, 'batch.py') ]
scripts_renamed = [ splitext(x)[0] for x in scripts_original ]
scripts_renamed = [ 'condor_' + basename(x) for x in scripts_renamed ]

for script, script_renamed in zip(scripts_original, scripts_renamed):
    copy2(script, script_renamed)

setup(
    name="htc_utils",
    version="0.1.0",
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

