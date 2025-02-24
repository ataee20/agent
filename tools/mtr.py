 
#!/usr/bin/python3
#requirment phantomjs,ntpdate,requests
from abc import ABC, abstractmethod
from tools.executor import Executor
import subprocess
from subprocess import Popen, PIPE
import json
import sys, os
import time
from datetime import datetime


class Mtr(Executor):
    def __init__(self,task):
        super().__init__(task)
        
    def convetColonSytx(self,resultParam):
        print("MTR")
        result="";
        for hub in resultParam["report"]["hubs"]:
            result=result+("loss,snt,drop,last,best,avg,wrst,javg,jmax,order,hopIp,date=%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s','%s'&&"
            %(hub["Loss%"],hub["Snt"],hub["Drop"],hub["Last"],hub["Best"],hub["Avg"],hub["Wrst"],hub["Javg"],hub["Jmax"],hub["count"],hub["host"],datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        result=result[0:-2]

        finalResult=('{"taskName":"%s","toolName":"mtr","reultOFTask":"%s","command":"%s"}'
        %(self.get_task()["taskName"],result,self.get_task()["command"]))
        return finalResult;
        
    def executeTask(self):
        cmd=self.get_task()["command"];
        cmd=self.get_task()["command"];
        cmd=os.path.dirname(repr(__file__)).replace("\'","")+"/../lateral_tools/"+cmd;
        parsedict={}
        try:
            p1 = Popen(cmd,stdout=PIPE, stderr=PIPE, shell=True)
            stdout8, string = p1.communicate()
            parsedict = json.loads(stdout8.decode())
        except:
            print('fail mtr test')

        return parsedict;

    

