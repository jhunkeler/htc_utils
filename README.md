# Requirements

The `htc_utils.bindings` package requires a working HTCondor installation in your `PATH` in order to function properly.

### Python 2.6.x:

* `argparse` >= 1.2
* `multiprocessing` >= 2.6

### Python 2.7.x ~ 3.x.x:

All dependencies are satisfied by default.


# Installation

### At the system level
```
python setup.py install
```

### Or at the user level
```
python setup.py install --user
```

# HTCondor Bindings

## Job & Submit Classes

This is an example of how to generate and submit simple jobs to a HTCondor cluster using htc_utils.

```
#!python
import random
from htc_utils.bindings import Job, Submit

# Create job object (filename will be "my_neato_condor.job")
job = Job('my_neato_condor')

# Populate initial job attributes
job.attr('getenv', True)
job.attr('executable', '/bin/sleep')
job.attr('arguments', 1)
job.logging('logs', create=True)
job.attr('queue')

# Populate additional sub-attributes (i.e. re-execute job with
# a different set of arguments.
for fileno in range(5):
    x = random.Random().randint(2, 5)
    job.subattr('arguments', x)
    job.subattr('queue')

# Write job file to disk
job.commit()

# Pass our job to the Submit class
submit = Submit(job)

# Send our job to the cluster
submit.execute()
```

### Contents of `my_neato_condor.job`

```
universe = vanilla
getenv = true
executable = /bin/sleep
arguments = 1
notification = Never
priority = 0
transfer_executable = true
should_transfer_files = IF_NEEDED
when_to_transfer_output = ON_EXIT
hold = false
log = logs/condor_$(Cluster).log
output = logs/stdout_$(Cluster)_$(Process).log
error = logs/stderr_$(Cluster)_$(Process).log
queue 

arguments = 5
queue 

arguments = 2
queue 

arguments = 2
queue 

arguments = 4
queue 

arguments = 4
queue 

```

## CLI Components

`htc_utils` provides a wrapper to the `Job` class to aid job creation outside of Python.

### Job example rewritten using `condor_batch`

```
#!bash
condor_batch -n my_neato_condor \
--logging logs \
--getenv true \
--subarg 5 \
--subarg 2 \
--subarg 2 \
--subarg 4 \
--subarg 4 \
/bin/sleep 1
```