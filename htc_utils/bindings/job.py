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


import os
from . import recast
from collections import OrderedDict


class Job(object):
    def __init__(self, filename, ext='job', * args, **kwargs):
        ''' Example usage
        import random
        from condor_batch import Job, Submit

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
        '''


        self.filename = os.path.abspath('.'.join([filename, ext]))
        self.shebang = '#!/usr/bin/env condor_submit'

        self.config_ext = []
        self.config = OrderedDict()

        self.default_config = [
            self.attr('universe', 'vanilla'),
            self.attr('getenv', True),
            self.attr('environment', ''),
            self.attr('executable', ''),
            self.attr('arguments', ''),
            self.attr('notification', 'Never'),
            self.attr('notify_user', ''),
            self.attr('priority', 0),
            self.attr('rank', ''),
            self.attr('input', ''),
            self.attr('request_cpus', ''),
            self.attr('request_disk', ''),
            self.attr('request_memory', ''),
            self.attr('requirements', ''),
            self.attr('transfer_executable', True),
            self.attr('transfer_input_files', []),
            self.attr('transfer_output_files', ''),
            self.attr('transfer_output_remaps', ''),
            self.attr('should_transfer_files', 'IF_NEEDED'),
            self.attr('when_to_transfer_output', 'ON_EXIT'),
            self.attr('hold', False),
            self.attr('initialdir', ''),
            self.attr('remote_initialdir', ''),
            self.attr('run_as_owner', ''),
            self.attr('nice_user', ''),
            self.attr('stack_size', ''),
            ]

        self.logs = {}

        for key, value in kwargs.items():
            self.attr(key, value)


    def generate(self):
        '''Return a
        '''
        if not self.config:
            print("Warning: No attributes defined!")
        output = ''

        # Parse initial job attributes
        for key, value in self.config.items():
            if value and key != 'queue':
                output += ' = '.join([key, value])
                output += os.linesep
            if key == 'queue':
                output += ' '.join([key, value])
                output += os.linesep

        # Parse job sub-attributes
        for sub in self.config_ext:
            output += os.linesep
            for key, value in sub.items():
                if value and key != 'queue':
                    output += ' = '.join([key, value])
                    # output += os.linesep
                if key == 'queue':
                    output += ' '.join([key, value])
                    output += os.linesep

        return output

    def logging(self, path, ext='log', create=False):
        if create and not os.path.exists(path):
            os.mkdir(os.path.abspath(path))

        self.logs['log'] = os.path.normpath(os.path.join(path, '.'.join(['condor_$(Cluster)', ext])))
        self.logs['output'] = os.path.normpath(os.path.join(path, '.'.join(['stdout_$(Cluster)_$(Process)', ext])))
        self.logs['error'] = os.path.normpath(os.path.join(path, '.'.join(['stderr_$(Cluster)_$(Process)', ext])))

        self.attr('log', self.logs['log'])
        self.attr('output', self.logs['output'])
        self.attr('error', self.logs['error'])

    def attr(self, key, *args):
        value = ' '.join([recast(x) for x in args])
        self.config[key] = recast(value)

    def subattr(self, key, *args):
        value = ' '.join([recast(x) for x in args])
        self.config_ext.append(OrderedDict([(key, recast(value))]))

    def commit(self, ext='job'):
        with open(self.filename, 'w+') as submit_file:
            submit_file.write(self.generate())

    def reset(self):
        self.config = OrderedDict()
        self.config_ext = OrderedDict()
