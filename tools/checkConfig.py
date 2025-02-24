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
from tools.utils import Utils
from fwutech_enum import FwutechEnum


class CheckConfigAndTools():

    def __init__(self, conf_in):
        self.utilsObject = Utils()
        self.scenConfig = conf_in
        self.utils_var = Utils()

    def checkUpdate(self):
        url_param = FwutechEnum.CHECK_UPDATE_URL.value % (self.scenConfig["serverIp"], str(
            self.scenConfig["serverInfoPort"]), str(self.utils_var.getMID()))
        response = self.utils_var.httpRequestGet(url_param)
        print(url_param)
        return response.json()["resp"]

    def checkUpdateWEBPASWD(self):
        url_param = FwutechEnum.CHECK_WEB_PASSWD_URL.value % (self.scenConfig["serverIp"], str(
            self.scenConfig["serverInfoPort"]), str(self.utils_var.getMID()))
        response = self.utils_var.httpRequestGet(url_param)
        print(url_param)
        return response.json()["resp"]

    def syncScenarioFromServer(self):
        try:
            print(FwutechEnum.CHECKING_UPDATE_SCENARIO_MSG.value)
            mid = str(self.utils_var.getMID())
            if self.checkUpdate() == True:
                url_param = FwutechEnum.UPDATE_CONFIG_URL.value % (
                    self.scenConfig["serverIp"], str(self.scenConfig["serverInfoPort"]), mid)
                print(url_param)
                response = self.utils_var.httpRequestGet(url_param)
                if response.status_code == 200 and response != None and response != "" and response != " ":

                    if self.utils_var.updateScenario(response.json()) == False:
                        raise Exception()
                    else:
                        try:
                            url_param = FwutechEnum.UPDATE_COMPLATE_URL.value % (
                                self.scenConfig["serverIp"], str(self.scenConfig["serverInfoPort"]), mid)
                            self.utils_var.httpRequestGet(url_param)
                        except:
                            pass
                        self.utils_var.runCmd(
                            FwutechEnum.RESTART_AGENT_CMD.value)

            else:
                print(FwutechEnum.NOTHING_UPDATE_SCEN_MSG.value)
        except:
            print(FwutechEnum.CHECK_SCENARIO_FAILD_MSG.value)


    def checkWebPassword(self):
        try:
            print(FwutechEnum.CHECKING_CHECK_WEB_PASSWORD.value)
            mid = str(self.utils_var.getMID())
            if self.checkUpdateWEBPASWD() == True:
                url_param = FwutechEnum.UPDATE_WEB_PASSWD_URL.value % (
                    self.scenConfig["serverIp"], str(self.scenConfig["serverInfoPort"]), mid)
                print(url_param)
                response = self.utils_var.httpRequestGet(url_param)
                if response.status_code == 200 and response != None and response != "" and response != " ":

                    if self.utils_var.updateWebPASWD(response.json()) == False:
                        raise Exception()
                    else:
                        try:
                            url_param = FwutechEnum.UPDATE_WEB_PASSWD_COMPLATE_URL.value % (
                                self.scenConfig["serverIp"], str(self.scenConfig["serverInfoPort"]), mid)
                            self.utils_var.httpRequestGet(url_param)
                        except:
                            pass
            else:
                print(FwutechEnum.NOTHING_UPDATE_WEB_SEC_MSG.value)
        except:
            print(FwutechEnum.CHECK_WEB_SEC_FAILD_MSG.value)

    def toolUpgradeComplated(self, mid, toolName):
        url_param = FwutechEnum.UPGRADE_COMPLATE_URL.value % (self.scenConfig["serverIp"], str(
            self.scenConfig["serverInfoPort"]), str(self.utils_var.getMID()), toolName)
        response = self.utils_var.httpRequestGet(url_param)
        print(FwutechEnum.UPGRADE_COMPLATED_SUCCESS_MSG.value % (toolName))

    def checkUpgradeTools(self):
        print(FwutechEnum.CHECKING_UPDATE_TOOLS_MSG.value)
        mid = self.utils_var.getMID()
        url_param = FwutechEnum.UPGRADE_TOOLS_LIST_URL.value % (
            self.scenConfig["serverIp"], str(self.scenConfig["serverInfoPort"]), str(mid))

        dwonload_tool_url = FwutechEnum.DOWNLOAD_TOOL_URL.value % (self.scenConfig["serverIp"], str(
            self.scenConfig["serverInfoPort"]), str(self.utils_var.getMID()))

        response = self.utils_var.httpRequestGet(url_param)

        if response.status_code == 200 and response != None and response != "" and response != " " and len(response.json()) != 0:

            try:
                # mount   writeable /home
                # self.utils_var.runCmd(FwutechEnum.MOUNT_WRITEABLE_CMD.value)

                for toolNameIndex in response.json():
                    self.utils_var.downloadFile(dwonload_tool_url+toolNameIndex, os.path.dirname(
                        repr(__file__)).replace("\'", "")+"/"+toolNameIndex)
                    self.toolUpgradeComplated(mid, toolNameIndex)
            except:
                pass
            finally:
                # mount   writeable /home
                # self.utils_var.runCmd(FwutechEnum.MOUNT_READONLY_CMD.value)
                pass

        else:
            print(FwutechEnum.NOTHING_TO_UPGRADE_TOOLS.value)
