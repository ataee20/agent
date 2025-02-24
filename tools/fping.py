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


class Fping(Executor):
    
    def __init__(self,task):
        super().__init__(task)

    def convetColonSytx(self,resultParam):
        print("this is ping")
        result=''
        jsonResult=eval(resultParam)
        taskNames=self.get_task()["taskName"].split(",")
        for index in range(0,len(jsonResult)):
            rs=jsonResult[index];
            avg=('null' if rs["loss"] == 100 else rs["avg"]);
            jitter=('null' if rs["loss"] == 100 else rs["jitter"])
            min_var=('null' if rs["loss"] == 100 else rs["min"])
            max_var=('null' if rs["loss"] == 100 else rs["max"])
            if jitter != 'null' and jitter > 1000 :
                jitter=jitter/100
            result =result+('{"taskName":"%s","toolName":"ping","reultOFTask":"AVG,MIN,MAX,SENT,RECIVE,LOST,jitter,date=%s,%s,%s,%s,%s,%s,%s,\'%s\'","command":"%s"},'
            %(taskNames[index],str(avg),str(min_var),str(max_var),str(rs["xmt"]),str(rs["rcv"]),str(rs["loss"]),str(jitter),datetime.now().strftime('%Y-%m-%d %H:%M:%S'),self.get_task()["command"]))
        return "["+result[0:len(result)-1]+"]";
        
    def executeTask(self):
        
        cmd=self.get_task()["command"];
        cmd=cmd.replace("ping", "");
        print(cmd)
        cmd=os.path.dirname(repr(__file__)).replace("\'","")+"/../lateral_tools/fping "+cmd;
        return (subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8"))
        # pingResp = json.loads();
        # return pingResp;

    

