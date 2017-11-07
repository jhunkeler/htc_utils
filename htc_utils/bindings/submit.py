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
import subprocess
from . import htcondor_path


class Submit(object):
    def __init__(self, job, **kwargs):
        self._htcondor_path = None
        if 'install_prefix' in kwargs:
            self._htcondor_path = htcondor_path(kwargs['install_prefix'])
        else:
            self._htcondor_path = htcondor_path()

        self.job = job
        self.cluster = []
        self.environ = os.environ
        self._prefix = ':'.join([self.environ['PATH'], self._htcondor_path])
        self.environ['PATH'] = self._prefix

        if 'CONDOR_CONFIG' not in self.environ:
            self.environ['CONDOR_CONFIG'] = os.path.abspath(self._htcondor_path.split(':')[0] +
                                                '/../../etc/condor/condor_config')

        self.cli_args = []

        print("Received job: {}".format(self.job.filename))

    def sendto_name(self, schedd_name):
        self.cli_args.append(['-name', schedd_name])

    def sendto_remote(self, schedd_name):
        self.cli_args.append(['-remote', schedd_name])

    def sendto_addr(self, ip, port):
        addr = ':'.join([ip, str(port)])
        addr = '<' + addr + '>'
        self.cli_args.append(['-addr', addr])

    def sendto_pool(self, pool_name):
        self.cli_args.append(['-pool', pool_name])

    def toggle_verbose(self):
        self.cli_args.append(['-verbose'])

    def toggle_unused_variables(self):
        self.cli_args.append(['-unused'])

    def execute(self):
        condor_submit_args = ' '.join([str(arg) for record in self.cli_args for arg in record])
        condor_submit = ' '.join(['condor_submit', condor_submit_args, self.job.filename])
        proc = subprocess.Popen(condor_submit.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=self.environ)
        stdout, stderr = proc.communicate()

        if isinstance(stdout, bytes):
            stdout = stdout.decode()
        if isinstance(stderr, bytes):
            stderr = stderr.decode()

        print(stdout)
        print(stderr)
        proc.wait()

        if not stderr:
            if 'cluster' in stdout:
                for line in stdout.split(os.linesep):
                    if 'cluster' in line:
                        self.cluster.append(line.split()[-1].strip('.'))

    def monitor(self):
        if not self.cluster:
            print('No cluster data for job.')
            return False
        print('Monitoring cluster {}'.format(self.cluster))
        self.environ['PATH'] = self._prefix
        '''
        proc = subprocess.Popen('condor_q -analyze:summary'.split(), env=self.environ)
        proc.communicate()
        proc.wait()
        '''
        print('NOT IMPLEMENTED')
        return True
