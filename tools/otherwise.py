 
#!/usr/bin/python3
#requirment phantomjs,ntpdate,requests
from abc import ABC, abstractmethod
from tools.executor import Executor


class Nothing(Executor):

    def __init__(self,task):
        super().__init__(task)

    def convetColonSytx(self,resultParam):
        return "{}";
        
    def executeTask(self):
        cmd=self.get_task()["command"];
        return "{}";

    

