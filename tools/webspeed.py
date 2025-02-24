#!/usr/bin/python3
# requirment phantomjs,ntpdate,requests
from abc import ABC, abstractmethod
from tools.executor import Executor
import subprocess
from subprocess import Popen, PIPE
from subprocess import STDOUT, check_output
import json
import sys
import os
import time
from datetime import datetime
from urllib.parse import urlparse
import shlex


class Webspeed(Executor):

    def __init__(self, task):
        super().__init__(task)

    def convetColonSytx(self, resultParam):
        print("Pageload")
        result = ""
        if type(resultParam['plt_time']) == str:
            result = ('{"taskName":"%s","toolName":"webspeed","reultOFTask":"Error,date=\'page load faild\',\'%s\'","command":"%s"}'
                      % (self.get_task()["taskName"], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.get_task()["command"]))
        else:
            # result=('{"taskName":"%s","toolName":"webspeed","reultOFTask":"TIME,siteLocat,date=%s,\'%s\',\'%s\'","command":"%s"}'
            # %(self.get_task()["taskName"],str(resultParam["plt_time"]),self.get_task()["siteLocat"],datetime.now().strftime('%Y-%m-%d %H:%M:%S'),self.get_task()["command"]))
            result = ('{"taskName":"%s","toolName":"webspeed","reultOFTask":"TIME,date=%s,\'%s\'","command":"%s"}'
                      % (self.get_task()["taskName"], str(resultParam["plt_time"]), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.get_task()["command"]))
        return result

    def executeTask(self):
        response = {}
        siteAddress = self.get_task()["command"]
        try:
            speed_test_path = os.path.dirname(repr(__file__)).replace(
                "\'", "")+"/../lateral_tools/loadspeed.js "
            plt = 'phantomjs '+speed_test_path+siteAddress
            stdout3 = check_output(shlex.split(plt), stderr=STDOUT, timeout=100,shell=False)
            respStr = stdout3.decode().replace(
                "TypeError: Attempting to change the setter of an unconfigurable property.", "").replace("\n", "")
            plt_time = int(respStr.split('TIME=')[1].replace(" ", ""))
        except Exception as ex:
            plt_time = "ERROR=FAIL to load the address"
        response["plt_time"] = plt_time
        # metaData={};
        # try:
        #     # get Meta Data's
        #     metaData=self.getMetadata(siteAddress)
        # except:
        #     pass
        # try:
        #     response["dns_resolution"]=metaData["dns_resolution"];
        # except:
        #     response["dns_resolution"]=0
        # try:
        #     response["tcp_established"]=metaData["tcp_established"];
        # except:
        #     response["tcp_established"]=0
        # try:
        #     response["ssl_handshake_done"]=metaData["ssl_handshake_done"];
        # except:
        #     response["ssl_handshake_done"]=0
        # try:
        #     response["TTFB"]=metaData["TTFB"];
        # except:
        #     response["TTFB"]=0;

        # get nsLookup Data
        # try:
        #     response["siteArres"]=self.nskLookupOfSite(self.getReturnHostDomain(siteAddress))
        # except:
        #     response["siteArres"]=""

        return response

    def getMetadata(self, url_param):
        cmd = 'curl -w "{\\"dns_resolution\\": %{time_namelookup}, \\"tcp_established\\": %{time_connect}, \\"ssl_handshake_done\\": %{time_appconnect}, \\"TTFB\\": %{time_starttransfer}}" -o /dev/null -s "'+url_param+'"'
        # print(cmd)
        p3 = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout3, string = p3.communicate()

        return json.loads(stdout3.decode())

    def nskLookupOfSite(self, siteAddr):
        cmd = 'nslookup '+siteAddr
        p3 = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout3, string = p3.communicate()
        return stdout3.decode().replace("\'", "").replace("\"", "").replace(" ", "").replace("\n", "").replace("\t", "")

    def getReturnHostDomain(self, host_param):
        parsed_uri = urlparse(host_param)
        result = '{uri.netloc}'.format(uri=parsed_uri)
        return result