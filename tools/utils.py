#!/usr/bin/python3
import json
import re
from os import listdir
from os.path import isfile, join
from datetime import datetime
from subprocess import Popen, PIPE
import sys
import os
import requests
import urllib.request
import shutil
import subprocess
from fwutech_enum import FwutechEnum


class Utils():

    def __init__(self):
        self.relative_path = os.path.dirname(
            repr(__file__)).replace("\'", "")+"/../"
        self.config_path = FwutechEnum.CONFIG_PATH.value % (self.relative_path)
        self.info_path = FwutechEnum.INFO_PATH.value % (self.relative_path)
        self.usr_sec_path = FwutechEnum.USR_SEC_PATH.value % (self.relative_path)
      

    
    def readUsr_sec(self):
        data = None
        with open(self.usr_sec_path) as json_file:
            return json.load(json_file)


    def readConf(self):

        data = None
        with open(self.config_path) as json_file:
            return json.load(json_file)

    def getInfo(self):

        data = None
        with open(self.info_path) as json_file:
            return json.load(json_file)

    def updateScenario(self, conf):

        status = False
        try:
            # MOUNT WRITEABLE /home
            # self.runCmd(FwutechEnum.MOUNT_WRITEABLE_CMD.value)

            with open(self.config_path, 'w') as outfile:
                json.dump(conf, outfile)
            print(FwutechEnum.SAVE_SCENARIO_SUCC_MSG.value)
            status = True
        except:
            pass
        finally:
            # MOUNT READONLY /home
            # self.runCmd(FwutechEnum.MOUNT_READONLY_CMD.value)
            pass
            

        return status


    def updateWebPASWD(self, conf):

        status = False
        try:
            # MOUNT WRITEABLE /home
            # self.runCmd(FwutechEnum.MOUNT_WRITEABLE_CMD.value)

            with open(self.usr_sec_path, 'w') as outfile:
                json.dump(conf, outfile)
            print(FwutechEnum.SAVE_WEB_SEC_SUCC_MSG.value)
            status = True
        except:
            pass
        finally:
            # MOUNT READONLY /home
            # self.runCmd(FwutechEnum.MOUNT_READONLY_CMD.value)
            pass
            

        return status

    def updateInfo(self, info):
        status = False
        with open(self.info_path, 'w') as outfile:
            json.dump(info, outfile)
        print(FwutechEnum.SAVE_INFO_SUCC_MSG.value)
        status = True
        return status

    def runCmd(self, cmd):
        print("CMD: "+cmd)
        try:
            return (subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8"))
        except:
            return "Exception"

    def sortTasks(self, tasks):
        tasks.sort(key=lambda x: x["taskPriority"], reverse=False)
        return tasks

    def integratePingTask(self, pingTasks):
        if len(pingTasks) > 1:
            for counter in range(1, len(pingTasks)):
                dest_addr = ""
                if "www" in pingTasks[counter]["command"] or "com" in pingTasks[counter]["command"] or "ir" in pingTasks[counter]["command"] or "org" in pingTasks[counter]["command"]:
                    dest_addr = re.findall(
                        '[ ][a-zA-Z][.]?(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', pingTasks[counter]["command"])[0].replace(" ", "")
                else:
                    dest_addr = re.findall(
                        r'[0-9]+(?:\.[0-9]+){3}', pingTasks[counter]["command"])[0]
                pingTasks[0]["command"] = pingTasks[0]["command"]+" "+dest_addr
                pingTasks[0]["taskName"] = pingTasks[0]["taskName"] + \
                    ","+pingTasks[counter]["taskName"]
            return pingTasks[0]
        else:
            return {}

    def get_pingTask(self, tasks):
        tempTask = []
        for task in tasks:
            if task["toolName"] == "ping" or task["toolName"] == "fping":
                tempTask.append(task)
        return tempTask

    def integrateTasks(self, tasks, reformatedTask):
        tempTask = []
        for taskIndex in tasks:
            if len(reformatedTask) == 0 or taskIndex["toolName"] != reformatedTask["toolName"]:
                tempTask.append(taskIndex)
        if len(reformatedTask) != 0:
            tempTask.append(reformatedTask)
        return tempTask

    def prepareResult(self, result):

        results = [{
            "content": result,
            "fileName": ""
        }]
        if not os.path.exists(FwutechEnum.RESULT_DIR_PATH.value):
            os.makedirs(FwutechEnum.RESULT_DIR_PATH.value)
        result_files = [f for f in listdir(FwutechEnum.RESULT_DIR_PATH.value) if isfile(
            join(FwutechEnum.RESULT_DIR_PATH.value, f))]
        # print(result_files)
        for resultFileName in result_files:
            with open(FwutechEnum.RESULT_DIR_PATH.value+resultFileName) as json_file:
                results.append({"fileName": resultFileName,
                                "content": json.load(json_file)})
        return results

    def saveToTMP(self, result):
        status = False
        try:

            with open(FwutechEnum.RESULT_DIR_PATH.value+datetime.now().strftime('%Y%m%d%H%M%S'), 'w') as outfile:
                json.dump(result["content"], outfile)
            print(FwutechEnum.SAVE_RSLT_TO_TEMP_SUCC_MSG.value)
            status = True
        except:
            print(FwutechEnum.SAVE_RSLT_TO_TEMP_FAILD_MSG.value)
        return status

    def removeFile(self, fileName):
        if fileName != "":
            try:
                os.remove(FwutechEnum.RESULT_DIR_PATH.value+fileName)
                print(FwutechEnum.SUCCESS_REMOVE_RSLT_MSG.value % (fileName))
            except:
                print(FwutechEnum.FAILD_REMOVE_RSLT_MSG.value % (fileName))

    def sendResultToServer(self, serverUrl, result):
        status = False
        try:
            headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}
            r = requests.post(serverUrl, data=json.dumps(
                result), headers=headers, timeout=(20, 30))
            status = True
        except:
            pass
        return status

    def send(self, serverAddr, results):
        # print(results)
        for result in results:
            if self.sendResultToServer(serverAddr, result["content"]) == True:
                print(FwutechEnum.RESULT_SEND_SUCCESS_MSG.value)
                self.removeFile(result["fileName"])
            else:
                self.saveToTMP(result)
                print(FwutechEnum.RESULT_SEND_FAILD_MSG.value)

    def getMID(self):

        mac = Popen(FwutechEnum.IP_LINK_CMD.value,
                    stdout=PIPE, stderr=PIPE, shell=True)
        stdout01, string = mac.communicate()
        mac = '0x'+stdout01.decode().split('link/ether ')[1][0:2]+stdout01.decode().split('link/ether ')[1][3:5]+stdout01.decode().split('link/ether ')[
            1][6:8]+stdout01.decode().split('link/ether ')[1][9:11]+stdout01.decode().split('link/ether ')[1][12:14]+stdout01.decode().split('link/ether ')[1][15:17]
        MID = int(mac, 0)
        resp = str(MID)
        if(self.getMidParent() != "" and self.getMidParent() != "None"):
            resp = self.getMidParent()+"_"+self.getInfo()["mid"]
        return resp

    def get_dns(self):
        pass

    def httpRequestGet(self, url_param):
        response = None
        try:
            response = requests.get(url_param, timeout=5)
        except:
            pass

        return response

    def httpRequestPost(self, url_param, data_param):
        response = None
        try:
            response = requests.post(url_param, data=data_param, timeout=5)
        except:
            pass

        return response

    def downloadFile(self, url_in, outPath):
        print(url_in)
        with urllib.request.urlopen(url_in) as response, open(outPath, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

    def post_form(self, url_in, data_in):
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        r = requests.post(url_in, data=data_in, headers=headers, timeout=4)
        resp = r.json()
        return resp

    def getMidParent(self):
        resp = "None"
        try:
            resp = str(self.httpRequestGet(FwutechEnum.GET_PARENT_MID_URL.value % (
                self.getInfo()["host_parent"])).json())
        except:
            pass
        return resp
