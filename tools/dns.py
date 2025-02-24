
#!/usr/bin/python3

from abc import ABC, abstractmethod
from tools.executor import Executor
from abc import ABC, abstractmethod
from tools.executor import Executor
import subprocess
from subprocess import Popen, PIPE
import json
import sys
import os
import time
from datetime import datetime
import time
import re
import telnetlib


class Dns(Executor):

    def __init__(self, task):
        super().__init__(task)
        self.host = "192.168.1.1"
        self.port = "23"
        self.username = "fwutech"
        self.password = "F@rafanQ03#tc!"
        self.telnet_timeout = 15
        self.read_until_timeout = 5
        self.dns_ips_date = []

    def convetColonSytx(self, resultParam):
        print("this is dns")
        result = ""
        if type(resultParam) == str or resultParam == -1:
            result = ('{"taskName":"%s","toolName":"dns","reultOFTask":"Error,date=\'dns faild\',\'%s\'","command":"%s"}'
                      % (self.get_task()["taskName"], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.replaceADDR(self.get_task()["command"])))
        else:
            result = ('{"taskName":"%s","toolName":"dns","reultOFTask":"Time,date=%s,\'%s\'","command":"%s"}'
                      % (self.get_task()["taskName"], str(resultParam), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.replaceADDR(self.get_task()["command"])))
        print(result)
        return result

    def executeTask(self):

        self.prepareDnsIps()

        # set daynamic dns
        cmd = self.get_task()["command"]
#        print(cmd)
        cmd = self.replaceADDR(cmd)

#        print("dig "+cmd)
        p2 = Popen("dig "+cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout2, string = p2.communicate()
        dnsTime = -1
        try:

            for line in stdout2.decode().split('\n'):
                if "Query time" in line:
                    dnsTime = int(line.split(":")[1].replace(
                        "msec", "").replace("sec", "").replace(" ", ""))
                    break
        except:
            dnsTime = "Error=Dns faild"
        return dnsTime

    def findDNS(self):
        try:
            print(datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S') + " READ DNS FROM MODEM !")
            dns_ips_var = []
            tn = telnetlib.Telnet(self.host, self.port,
                                  timeout=self.telnet_timeout)
            if b'Username:' in tn.read_until(b'Username:', timeout=self.read_until_timeout):
                tn.write(bytes(self.username, 'ascii') + b"\r\n")
                if b'Password:' in tn.read_until(b'Password:', timeout=self.read_until_timeout):
                    time.sleep(0.2)
                    tn.write(bytes(self.password, 'ascii') + b"\r\n")
                    time.sleep(1)
                    tn.write(bytes("sh", 'ascii') + b"\r\n")
                    time.sleep(1)
                    tn.write(bytes("pppoe show", 'ascii') + b"\r\n")
                    time.sleep(1)
                    tn.write(bytes("exit", 'ascii') + b"\r\n")
                    result_tmp = tn.read_all().decode('ascii').splitlines()
                    re_ip = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
                    ips = re.findall(re_ip, result_tmp[len(result_tmp)-2])
                    self.dns_ips_date = ips
                    self.dns_ips_date.append(
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        except:
            print(datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S') + " Find DNS Failed !")

    def writeDNSToTemp(self):
        try:
            with open("/tmp/daynamic_dns", 'w') as outfile:
                json.dump(self.dns_ips_date, outfile)
        except:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') +
                  " Cant write DNS TO /tmp/daynamic_dns !")

    def readDNSFromTemp(self):
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') +
              " READING DNS from DSIK: /tmp/daynamic_dns !")
        dns_ips_date_tmp = []
        try:
            with open("/tmp/daynamic_dns") as json_file:
                dns_ips_date_tmp = json.load(json_file)
        except:
            pass
        self.dns_ips_date = dns_ips_date_tmp

    def prepareDnsIps(self):
        try:
            self.readDNSFromTemp()
            if not self.dns_ips_date:
                self.findDNS()
                self.writeDNSToTemp()
            else:
                dns_readed_date = datetime.strptime(
                    self.dns_ips_date[2], '%Y-%m-%d %H:%M:%S')
                diff_dates = (
                    (datetime.now() - dns_readed_date).total_seconds())/60.0
                if diff_dates >= 120:
                    self.findDNS()
                    self.writeDNSToTemp()
        except:
            print(datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S') + "Can not prepare DNS !")

    def replaceADDR(self, cmd_param):
        try:
            if 'dns1' in self.get_task()["taskName"].lower():
                cmd_param = cmd_param.replace("@addr", self.dns_ips_date[0])

            elif 'dns2' in self.get_task()["taskName"].lower():
                cmd_param = cmd_param.replace("@addr", self.dns_ips_date[1])
        except:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') +
                  " ERROR CANT CHANGE THE @addr !")

        return cmd_param
