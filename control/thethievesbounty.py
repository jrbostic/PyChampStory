import copy
from model.protag import Hero

__author__ = 'jessebostic'


class Coupler:

    def __init__(self):
        self.jobs = []
        self.jobs.append({'message': "Welcome to the Realm of PyChamp!", 'board': None, 'hero': Hero('NoneYet')})

    def add_job(self, job):  #jobs are just dictionaries of strings to object refs
        self.jobs.append(job)
        #print (str(job))

    def ________________get_jobs(self):
        jobs = copy.deepcopy(self.jobs)
        self.jobs = []
        return jobs

    def get_a_job(self):
        job = None
        if len(self.jobs) > 0:
            job = self.jobs.pop(0)
        return job

    #Package({component/call:data}, TopLevelEvent)
