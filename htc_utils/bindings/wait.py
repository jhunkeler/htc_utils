import os
import subprocess


class Wait(object):
    '''
    -debug            Show extra debugging info
    -status           Show job start and terminate info
    -echo             Echo log events relevant to [job-number]
    -num <number>     Wait for this many jobs to end
                       (default is all jobs)
    -wait <seconds>   Wait no more than this time
                       (default is unlimited)
    '''
    def __init__(self, submit, **kwargs):
        self.submit = submit
        self.cli_args = []
    
    def toggle_debug(self):
        self.cli_args.append(['-debug'])
        
    def toggle_status(self):
        self.cli_args.append(['-status'])    

    def toggle_echo(self):
        self.cli_args.append(['-echo'])
    
    def num(self, num_jobs):
        self.cli_args.append(['-num', num_jobs])
        
    def timeout(self, seconds):
        self.cli_args.append(['-wait', seconds])
        
    def execute(self):
        logfile = self.submit.job.logs['log'].replace('$(Cluster)', self.submit.cluster)
        print("logfile: {0}".format(logfile))
        condor_wait_args = ' '.join([str(arg) for record in self.cli_args for arg in record])
        condor_wait = ' '.join(['condor_wait', condor_wait_args, logfile])
        proc = subprocess.Popen(condor_wait.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=self.submit.environ)
        stdout, stderr = proc.communicate()
        print(stdout)
        print(stderr)
        proc.wait()
        
        '''
        if not stderr:
            if 'cluster' in stdout:
                for line in stdout.split(os.linesep):
                    if 'cluster' in line:
                        self.cluster = line.split()[-1].strip('.')
        '''
