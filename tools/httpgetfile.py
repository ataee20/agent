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


class Httpgetfile(Executor):
    def __init__(self,task):
        super().__init__(task)
        
    def convetColonSytx(self,resultParam):
        print("Bandwidth")
        result=""
        if type(resultParam) == str:
            result=('{"taskName":"%s","toolName":"httpgetfile","reultOFTask":"Error,date="Faild",\'%s\'","command":"http://speedtest.net"}'
            %(self.get_task()["taskName"],datetime.now().strftime('%Y-%m-%d %H:%M:%S'),self.get_task()["command"]))
        else:    
            result=('{"taskName":"%s","toolName":"httpgetfile","reultOFTask":"speed,date=%s,\'%s\'","command":"http://speedtest.net"}'
            %(self.get_task()["taskName"],resultParam,datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        return result;
        
    def executeTask(self):
        cmd=self.get_task()["command"];
        download=-1; 
        a=[]
        start=time.time()
        download = 'wget '+cmd+' --delete-after -O /tmp/test1Mb.db'
        download = Popen(download,stdout=PIPE, stderr=PIPE, shell=True)
        a.append(download.communicate())
        end=time.time()
        download = end-start
        bandSizeBit=self.checkDownloadSize(self.get_task()["taskName"])
#        print(bandSizeBit)
#        print(download)
        download=bandSizeBit/float(download)
        return download*8
    def checkDownloadSize(self,bandWidthSize):
        bandSize=1
        if "M" in bandWidthSize or "m" in bandWidthSize:
           bandSize=1024
        elif "G" in bandWidthSize or "g" in bandWidthSize:
           bandSize=1048576
        bandWidth=bandWidthSize.replace("M","").replace("m","").replace("G","").replace("g","").replace(" ","").replace("B","").replace("b","")
        return(float(bandSize) * float(bandWidth))
        

