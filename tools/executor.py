#!/usr/bin/python3

#requirment phantomjs,ntpdate,requests
from __future__ import print_function
from abc import ABC, abstractmethod



class Executor(ABC):

    def set_task(self,task):
        self.task=task
    
    
    def get_task(self):
        return self.task

    def __init__(self,task):
       self.set_task(task)

    @abstractmethod
    def convetColonSytx(resultParam) -> str:
        pass
    
    @abstractmethod
    def executeTask(cmd) -> str:
        pass

    

  